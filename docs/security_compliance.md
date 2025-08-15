# Security & Compliance Baseline (MVP → PoC)

## Key controls
- Keys & signing
  - Dev: local Ed25519 key file; Prod: KMS (BYOK), rotation, dual-approval
  - Signer ID = sha256(verify_key) prefix; MANIFEST.sig for packs
- Storage
  - Immutable audit JSONL (append-only); S3/Object Lock (WORM) in prod; versioning & retention
  - Indexes in Postgres (request_id, ts, endpoint, hashes); no secrets in DB
- Policy & privacy
  - YAML rules (no-cite-no-output, tool allowlist, PII masking), hot-reload; expose policy_sha256
  - Scrub sensitive fields (Authorization/API keys/tokens/passwords); truncate large strings/arrays
- Network & access
  - Egress allowlist (deny direct vendor endpoints), gateway-scoped tokens
  - OIDC/SSO + RBAC (admin/auditor/user) roadmap
- Time & integrity
  - UTC ISO timestamps; NTP discipline; TSA/QES optional (later)

## Evidence mapping
- `policies/regmap.json` aligns Annex IV / DORA / ISO 42001 / GDPR → evidence paths
- `metrics.json` includes SR/latency percentiles; `/audit/verify` proves chain integrity

## Operations & SLA
- Metrics: capture_rate, replay_determinism, latency_overhead
- Targets: capture≥98%, replay≥99%, overhead≤80ms, pack≤48h

## Roadmap
- KMS/BYOK + rotation; S3 WORM; OIDC/RBAC; Postgres indexes; OpenTelemetry traces/metrics
