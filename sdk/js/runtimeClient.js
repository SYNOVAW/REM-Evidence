// Minimal JS SDK for REM Verified Inference Runtime
// Node >=18 (global fetch) or browsers

export class RuntimeClient {
  constructor({ baseUrl, apiKey, byoKey } = {}) {
    if (!baseUrl) throw new Error("baseUrl required");
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.apiKey = apiKey || process.env.API_KEY || undefined;
    this.byoKey = byoKey || process.env.BYO_KEY || undefined;
  }

  _headers(extra = {}) {
    const h = { "Content-Type": "application/json", ...extra };
    if (this.apiKey) h["x-api-key"] = this.apiKey;
    if (this.byoKey) h["x-byo-key"] = this.byoKey; // upstream key
    return h;
  }

  // Non-streaming chat completions (OpenAI-compatible payload)
  async chatCompletions(payload) {
    const url = `${this.baseUrl}/proxy/openai/v1/chat/completions`;
    const resp = await fetch(url, {
      method: "POST",
      headers: this._headers(),
      body: JSON.stringify({ ...payload, stream: false }),
    });
    if (!resp.ok) {
      const msg = await safeText(resp);
      throw new Error(`Proxy error ${resp.status}: ${msg}`);
    }
    return resp.json();
  }

  // Streaming chat completions (SSE). onEvent receives { event, data, raw }
  async chatCompletionsStream(payload, onEvent) {
    const url = `${this.baseUrl}/proxy/openai/v1/chat/completions`;
    const resp = await fetch(url, {
      method: "POST",
      headers: this._headers(),
      body: JSON.stringify({ ...payload, stream: true }),
    });
    if (!resp.ok || !resp.body) {
      const msg = await safeText(resp);
      throw new Error(`Proxy error ${resp.status}: ${msg}`);
    }
    await parseEventStream(resp.body, onEvent);
  }
}

async function safeText(resp) {
  try {
    return await resp.text();
  } catch {
    return "";
  }
}

// Minimal SSE parser for ReadableStream
async function parseEventStream(stream, onEvent) {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  // Basic SSE framing: lines with optional 'event:' and 'data:'; events separated by blank line
  let cur = { event: "message", data: [] };
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let idx;
    while ((idx = buf.indexOf("\n")) >= 0) {
      const line = buf.slice(0, idx);
      buf = buf.slice(idx + 1);
      const s = line.replace(/\r$/, "");
      if (s === "") {
        // dispatch
        if (cur.data.length > 0) {
          const raw = cur.data.join("\n");
          let parsed = raw;
          try { parsed = JSON.parse(raw); } catch {}
          onEvent && onEvent({ event: cur.event || "message", data: parsed, raw });
        }
        cur = { event: "message", data: [] };
        continue;
      }
      if (s.startsWith(":")) continue; // comment
      if (s.startsWith("event:")) {
        cur.event = s.slice(6).trim();
        continue;
      }
      if (s.startsWith("data:")) {
        cur.data.push(s.slice(5).trimStart());
        continue;
      }
      // ignore other fields for MVP
    }
  }
}

export default RuntimeClient;


