# FAQ / Troubleshooting

Q: 401 Unauthorized?
- Ensure UI/CLI `x-api-key` matches server `API_KEY`.

Q: 429 Too Many Requests?
- Hit rate limit; check `X-RateLimit-*` headers; back off or increase limits.

Q: Upstream `invalid_api_key`?
- Remove masked/multiple keys from `.env`; use a single valid vendor key; test via `/runtime/info` and UI Dashboard.

Q: CORS errors in browser?
- Add origin to `ALLOW_ORIGINS` or disable for local dev.

Q: Tool bypasses gateway (direct supplier access)?
- Block direct vendor endpoints at egress; issue gateway-scoped tokens; set `OPENAI_BASE_URL` to your proxy.

Q: How to validate an exported pack offline?
```bash
python mvp/cli/verify_pack.py audit_pack.zip
```

Q: How to tail recent events and verify chain?
```bash
python mvp/cli/verify_pack.py --tail http://localhost:8000/trace/recent?limit=200 --api-key $API_KEY
```

Q: Where is regulatory mapping?
- `policies/regmap.json` (preview in `/ui/audit`)
