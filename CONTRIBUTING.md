# Contributing to REM Evidence

Thanks for helping improve the REM Evidence spec, schema, SDKs, and verifier.

## Scope
This repo is for:
- Evidence Pack specification (`docs/`)
- JSON Schemas (`schemas/`)
- Minimal SDKs (`sdk/python`, `sdk/js`)
- Offline verifier (`cli/verify_pack.py`)

Production runtime/gateway and enterprise features live in private repos.

## How to contribute
1. Fork + create a feature branch from `main`.
2. Make focused changes; add docs/examples when relevant.
3. Run basic checks:
   - Python: `python cli/verify_pack.py --events examples/events_sample.jsonl`
   - JS: ensure `sdk/js/runtimeClient.js` passes a basic `chatCompletions` request against a local runtime
4. Open a PR with a clear title and description.

## Conventions
- Style: keep code minimal, dependency-light, readable.
- Commits: conventional style (e.g., `feat:`, `fix:`, `docs:`, `chore:`).
- Labels: `spec` / `schema` / `sdk` / `cli`.
- Versioning: SemVer. Pre-GA uses `v0.x`.

## Security
Please report suspected vulnerabilities privately via issues (mark as security) or email the maintainers.

## License
By contributing, you agree your contributions are licensed under Apache-2.0.
