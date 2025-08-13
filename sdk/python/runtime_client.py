"""
Python SDK middleware for REM Verified Inference Runtime.

Features (MVP):
- Non-streaming and streaming chat completions via OpenAI-compatible proxy
- Header management (x-api-key, x-byo-key, x-purpose, x-request-id)
- Basic replay artifacts: replay_stub.json lines and replay.sh script

Usage:
  from mvp.sdk.python.runtime_client import RuntimeClient
  rc = RuntimeClient(base_url="http://localhost:8080", api_key=..., byo_key=..., purpose="regulatory_filing")
  # non-streaming
  res = anyio.run(rc.chat_completions, {"model":"gpt-4o-mini","messages":[{"role":"user","content":"hi"}]})
  # streaming
  async def on_evt(evt):
      print(evt["event"], evt.get("data"))
  await rc.chat_completions({"model":"gpt-4o-mini","messages":[...] , "stream": True}, on_event=on_evt)
"""
from __future__ import annotations

import os
import json
import time
import uuid
from typing import Any, Dict, Optional, Callable, Awaitable

import httpx


class RuntimeClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None, byo_key: Optional[str] = None, purpose: Optional[str] = None) -> None:
        if not base_url:
            raise ValueError("base_url required")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.getenv("API_KEY")
        self.byo_key = byo_key or os.getenv("BYO_KEY")
        self.purpose = purpose or os.getenv("RUNTIME_PURPOSE")

    def _headers(self, req_id: Optional[str] = None) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if req_id:
            h["x-request-id"] = req_id
        if self.api_key:
            h["x-api-key"] = self.api_key
        if self.byo_key:
            h["x-byo-key"] = self.byo_key
        if self.purpose:
            h["x-purpose"] = self.purpose
        return h

    async def chat_completions(self, payload: Dict[str, Any], on_event: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None) -> Optional[Dict[str, Any]]:
        """If payload.stream is True, invoke streaming and call on_event for SSE frames; otherwise return JSON.
        on_event receives dict: {event, data, raw}
        """
        stream = bool(payload.get("stream"))
        rid = str(uuid.uuid4())
        url = f"{self.base_url}/proxy/openai/v1/chat/completions"
        headers = self._headers(rid)
        if not stream:
            async with httpx.AsyncClient(timeout=60) as hc:
                resp = await hc.post(url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
            self._write_replay_stub(rid, payload, headers, streamed=False)
            return data

        # streaming path
        async with httpx.AsyncClient(timeout=None) as hc:
            async with hc.stream("POST", url, headers=headers, json=payload) as resp:
                resp.raise_for_status()
                chunk_hashes = []
                async for event in _iter_sse(resp):
                    # collect chunk hashes for manifest/chunk
                    if event.get("event") == "rem.chunk":
                        try:
                            chunk_hashes.append(event.get("data", {}).get("sha256"))
                        except Exception:
                            pass
                    if on_event:
                        await on_event(event)
        self._write_replay_stub(rid, payload, headers, streamed=True, chunk_hashes=[h for h in chunk_hashes if h])
        return None

    def _write_replay_stub(self, request_id: str, payload: Dict[str, Any], headers: Dict[str, str], streamed: bool, chunk_hashes: Optional[list[str]] = None) -> None:
        record = {
            "ts": time.time(),
            "request_id": request_id,
            "endpoint": "/proxy/openai/v1/chat/completions",
            "payload": {k: payload.get(k) for k in ("model", "messages", "temperature", "seed", "tools", "stream")},
            "headers": {k: headers.get(k) for k in ("x-request-id", "x-purpose") if headers.get(k)},
            "streamed": streamed,
            "chunk_hashes": chunk_hashes or [],
        }
        try:
            os.makedirs("audit/repro", exist_ok=True)
            # append line
            with open("audit/repro/replay_stub.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            # ensure replay.sh exists
            sh = (
                "#!/usr/bin/env bash\n"
                "# Minimal replay helper (placeholder)\n"
                "echo 'Provide an audit JSONL line to audit/repro/inference_replay.py'\n"
            )
            p = "audit/repro/replay.sh"
            if not os.path.exists(p):
                with open(p, "w", encoding="utf-8") as f:
                    f.write(sh)
        except Exception:
            return


async def _iter_sse(resp: httpx.Response):
    """Parse a server-sent-events stream from httpx response.
    Yields dicts: {event, data, raw}
    """
    event = "message"
    data_lines = []
    async for line in resp.aiter_lines():
        if line is None:
            continue
        raw = line
        s = line.rstrip("\r")
        if s == "":
            if data_lines:
                raw_data = "\n".join(data_lines)
                try:
                    parsed = json.loads(raw_data)
                except Exception:
                    parsed = raw_data
                yield {"event": event or "message", "data": parsed, "raw": raw_data}
            event = "message"
            data_lines = []
            continue
        if s.startswith(":"):
            continue
        if s.startswith("event:"):
            event = s[6:].strip()
            continue
        if s.startswith("data:"):
            data_lines.append(s[5:].lstrip())
            continue
        # ignore other fields


