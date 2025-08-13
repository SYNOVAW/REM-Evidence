# Evidence Pack Spec v0.1

## Directory Layout (zip)
- MANIFEST.json, MANIFEST.sig.json
- metrics.json (requests/errors summary and p50/p90/p95/p99 latency)
- docs/cover.pdf, docs/signature_page.pdf
- policies/*.md|.json|.csv (tech_doc, regmap, roi_sources, monitoring_plan, coverage_matrix, GDPR/DORA/eIDAS templates)
- audit/audit_*.jsonl, audit/incidents.jsonl (if any)
- audit/claims/claims_register.jsonl (litigation if any)
- audit/repro/env_snapshot.json, audit/repro/inference_replay.py
 - trace/events.jsonl (optional consolidated), citations/kb_sources.json

## Signing & Hashing
- Per-line JSONL: sha256 over canonical JSON (sorted keys, compact separators), chained via prev_hash
- Manifest: sha256 + Ed25519 signature; signer_id derived from verify key
- Time: ISO-8601 UTC; NTP synchronized; TSA/QES optional future
- Streaming SSE:
  - event: rem.chunk (sha256 per SSE data frame, optional via env SSE_CHUNK_SIGNING=1)
  - event: rem.manifest (final sha256 and signer_id injected before stream end)

## Replay
- `audit/repro/inference_replay.py` consumes a single JSONL line; customers may extend to full pipeline replay
- Determinism targets: >=0.99 where seeds/params fixed

## Privacy & Truncation
- Sensitive headers/fields (Authorization, API keys, tokens, secrets, passwords) are scrubbed to *** before logging.
- Large strings and arrays are truncated (default string<=2000 chars, list<=50 items) to prevent excessive payloads in chain.

## Mappings
- AI Act Annex IV: link to `policies/tech_doc.md` sections; logs: Art.12/18; PMS: monitoring_plan.md; incidents: incidents.jsonl
- DORA: RoI via roi_sources.json/`/audit/roi`; incidents; BCP/RTO/RPO in coverage_matrix.csv
- ISO 42001: management mapping via regmap.json

## SLA Targets (demo)
- 48h pack from unfamiliar data
- Runtime overhead <=80ms (export not included)
