#!/usr/bin/env python3
"""
Minimal offline verifier for audit_pack.zip (standard library only).

Usage:
  python mvp/cli/verify_pack.py path/to/audit_pack.zip
  python mvp/cli/verify_pack.py --events events.jsonl
"""
from __future__ import annotations
import io
import sys
import json
import zipfile
import hashlib


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _verify_events_lines(lines: list[str]) -> dict:
    ok = True
    checked = 0
    last_hash = None
    first_error = None
    for raw in lines:
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            ok = False
            if not first_error:
                first_error = {"file": "events.jsonl", "reason": "json_parse_error"}
            continue
        core_keys = ["ts","ts_iso","request_id","endpoint","status","input_hash","output_hash","params_snapshot","policy_hash","code_git_sha","prev_hash"]
        core = {k: obj.get(k) for k in core_keys}
        prehash = sha256_hex(json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode('utf-8'))
        if prehash != obj.get('hash'):
            ok = False
            if not first_error:
                first_error = {"file": "events.jsonl", "request_id": obj.get('request_id'), "reason": "hash_mismatch"}
        if last_hash and obj.get('prev_hash') not in (last_hash, None):
            ok = False
            if not first_error:
                first_error = {"file": "events.jsonl", "request_id": obj.get('request_id'), "reason": "prev_hash_mismatch"}
        last_hash = obj.get('hash')
        checked += 1
    return {"ok": ok, "checked": checked, "first_error": first_error}


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: verify_pack.py <audit_pack.zip>")
        return 2
    if sys.argv[1] == '--events' and len(sys.argv) >= 3:
        path = sys.argv[2]
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
            out = _verify_events_lines(lines)
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0 if out.get('ok') else 1
        except FileNotFoundError:
            print('File not found:', path, file=sys.stderr)
            return 2
    zpath = sys.argv[1]
    try:
        with zipfile.ZipFile(zpath, 'r') as z:
            # Read MANIFEST
            manifest = {}
            man_sig = {}
            try:
                with z.open('MANIFEST.json') as f:
                    manifest = json.loads(f.read().decode('utf-8'))
            except Exception:
                pass
            try:
                with z.open('MANIFEST.sig.json') as f:
                    man_sig = json.loads(f.read().decode('utf-8'))
            except Exception:
                pass

            # Verify hash chain across all audit_*.jsonl inside audit/
            names = [n for n in z.namelist() if n.startswith('audit/audit_') and n.endswith('.jsonl')]
            names.sort()
            ok = True
            checked = 0
            last_hash = None
            first_error = None
            for name in names:
                with z.open(name) as f:
                    for raw in f.read().decode('utf-8', errors='ignore').splitlines():
                        if not raw:
                            continue
                        try:
                            obj = json.loads(raw)
                        except Exception:
                            ok = False
                            if not first_error:
                                first_error = {"file": name, "reason": "json_parse_error"}
                            continue
                        core_keys = ["ts","ts_iso","request_id","endpoint","status","input_hash","output_hash","params_snapshot","policy_hash","code_git_sha","prev_hash"]
                        core = {k: obj.get(k) for k in core_keys}
                        prehash = sha256_hex(json.dumps(core, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode('utf-8'))
                        if prehash != obj.get('hash'):
                            ok = False
                            if not first_error:
                                first_error = {"file": name, "request_id": obj.get('request_id'), "reason": "hash_mismatch"}
                        if last_hash and obj.get('prev_hash') not in (last_hash, None):
                            ok = False
                            if not first_error:
                                first_error = {"file": name, "request_id": obj.get('request_id'), "reason": "prev_hash_mismatch"}
                        last_hash = obj.get('hash')
                        checked += 1

            out = {
                "ok": ok,
                "checked": checked,
                "manifest_sha256": sha256_hex(json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode('utf-8')) if manifest else None,
                "manifest": manifest,
                "manifest_sig": man_sig,
                "first_error": first_error,
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 0 if ok else 1
    except FileNotFoundError:
        print("File not found:", zpath, file=sys.stderr)
        return 2
    except zipfile.BadZipFile:
        print("Not a zip file:", zpath, file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())


