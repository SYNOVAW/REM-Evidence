# REM Evidence (Spec + Schema + SDK + Verifier)

Open spec, schema, minimal SDKs, and offline verifier for REM Evidence Packs.

- Spec: docs/evidence_pack_spec_v0_1.md
- JSON Schema: schemas/event.schema.json
- CLI Verifier: cli/verify_pack.py
- SDKs: sdk/python/runtime_client.py, sdk/js/runtimeClient.js
- Examples: examples/events_sample.jsonl

## Install (CLI)
```bash
python3 -m venv .venv && source .venv/bin/activate
python cli/verify_pack.py audit_pack.zip
# or local events
python cli/verify_pack.py --events examples/events_sample.jsonl
```

## Python SDK (minimal)
```python
from mvp.sdk.python.runtime_client import RuntimeClient
import anyio

async def main():
    rc = RuntimeClient(base_url="http://localhost:8000", api_key="...", byo_key="...")
    res = await rc.chat_completions({"model":"gpt-4o-mini","messages":[{"role":"user","content":"hi"}]})
    print(res)

anyio.run(main)
```

## JS SDK (minimal)
```js
import { RuntimeClient } from "./sdk/js/runtimeClient.js";
const rc = new RuntimeClient({ baseUrl: "http://localhost:8000", apiKey: "...", byoKey: "..." });
const out = await rc.chatCompletions({ model: "gpt-4o-mini", messages: [{ role: "user", content: "hi" }] });
console.log(out);
```

## Spec
See `docs/evidence_pack_spec_v0_1.md`.

## License
Apache-2.0

## Contact
SYNOVA WHISPER Inc.
www.synovawhisper.com
info@synova-w.com
