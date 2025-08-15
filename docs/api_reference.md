# API Reference (MVP)

Auth
- Header: `x-api-key: <API_KEY>` (if configured)

Health & Runtime
- GET `/` → `{ ok, service, version }`
- GET `/status` → `{ ok, ... }` (also audited)
- GET `/healthz` / `/readyz` → liveness/readiness
- GET `/metrics` → latency p50/p90/p95/p99; runtime counters; SR summary
- GET `/runtime/info` → features, SLA targets, `env`, `sse_chunk_signing`, `policy_sha256`
- GET `/runtime/selfcheck` → runs `/status` → `/sr` → `/audit/verify`
- GET `/config` / PUT `/config` → PolicyConfig (JSON)
- GET `/runtime/policy/show` → `{ path, present, sha256, doc }`

SR & Sandbox
- POST `/sr` → `{ sr }`
- POST `/execute` → `{ accepted, sr, reason?, output? }` (sr_threshold gate; policy deny/review)
- POST `/runtime/policy/evaluate` → `{ action, sr, reason? }`

Audit & Evidence
- GET `/audit/cards`
- POST `/audit/incidents`; GET `/audit/incidents?limit=`
- GET `/audit/roi?format=json|csv`
- POST `/audit/ingest?kind=roi|incidents` (CSV/JSON)
- GET `/audit/verify?days=&request_id=&since_ts=` → `{ ok, checked, first_error?, files?, from_ts?, to_ts? }`
- GET `/audit/pack?pack_type=audit|litigation&days=` → ZIP
  - Headers: `Content-Length`, `X-Manifest-Sha`, `X-Signer-Id`

Trace & Diff
- GET `/trace/{session_id}` → events.jsonl (Headers: `X-Event-Count`, `X-Bytes`)
- GET `/trace/recent?limit=` → recent events JSONL (Header: `X-Event-Count`)
- GET `/runtime/diff?a=&b=&days=` → `{ ok, diff: { endpoint, status, input_hash_equal, output_hash_equal, policy_hash_equal, params_snapshot:{added,removed,changed} } }`

Proxy (BYO key)
- POST `/proxy/openai/v1/chat/completions` (stream/non-stream; SSE signing)
- GET `/proxy/openai/v1/models`
- POST `/proxy/anthropic/v1/messages` (SSE signing)
- POST `/proxy/gemini/v1beta/models/{model}:generateContent` (SSE signing)
- POST `/proxy/bedrock/invoke` (requires AWS creds)

UI helper APIs
- GET `/ui/api/sessions?limit=`
- GET `/ui/api/regmap`
- GET `/ui/api/file?path=...` (policies/*, audit/*, MANIFEST.json, metrics.json)

Headers
- Rate limit: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Window`
- Pack: `X-Manifest-Sha`, `X-Signer-Id`, `Content-Length`
