# PoC One‑Pager / 48h Audit‑Pack Challenge (中 / 日 / EN)

---

## 简体中文（客户版）

- 产品定位：Verified Inference Runtime（证据层），不改客户模型栈，用 base_url/SDK/Sidecar 即插即用；输出“可提交、可回放、可签名”的审计/诉讼包。
- 我们交付什么（48小时样本）
  - `audit_pack.zip`：MANIFEST.json（含 sha256）、MANIFEST.sig（Ed25519）、metrics.json（SR/延迟分位）、审计日志（hash 链）、replay 脚本、条款映射（regmap.json）
  - 离线校验器：开源 `verify_pack.py`（可独立验证证据链与 MANIFEST）
- PoC（6–8周）范围
  - 覆盖 1–2 条关键业务用例；接入 OpenAI/Anthropic/Vertex/Bedrock（BYO‑Key）或自托管模型
  - 策略：no‑cite‑no‑output、PII 掩码、工具白名单；温度/seed 约束；SR 门控
  - 目标：通过一次内部审计/尽调（Annex IV / DORA / ISO42001 映射齐全）
- 验收与SLA（建议写入合同）
  - capture≥98%  replay≥99%  latency overhead≤80ms  pack≤48h
  - `/audit/verify`=OK（返回首错定位）、MANIFEST.sig 验签通过
- 集成方式
  - base_url 代理（最快）/ SDK 中间件 / Sidecar（自托管）/ 日志适配（兜底）
- 价格锚点（建议）
  - 48h样本：可抵扣 5–10k  /  PoC：25–60k（6–8周）  /  年订：10–30万/租户
- 快速验证（示例）
  ```bash
  curl -H "x-api-key:$API_KEY" http://<host>/runtime/selfcheck
  curl -H "x-api-key:$API_KEY" -o audit_pack.zip "http://<host>/audit/pack?days=7"
  python mvp/cli/verify_pack.py audit_pack.zip
  ```
- 开源与资料：REM‑Evidence（规范/Schema/SDK/验证器） https://github.com/SYNOVAW/REM-Evidence

---

## 日本語（お客様向け）

- 製品：Verified Inference Runtime（証拠レイヤー）。既存LLMの base_url/SDK/Sidecar 切り替えのみ。監査・訴訟に提出可能な署名付きパックを生成。
- 48時間で提供
  - `audit_pack.zip`：MANIFEST（sha256）/MANIFEST.sig（Ed25519）/metrics（SR/レイテンシ分位）/監査JSONL（hash chain）/replayスクリプト/regmap（条文マッピング）
  - オフライン検証：`verify_pack.py`（独立検証）
- PoC（6–8週）範囲
  - 主要ユースケース 1–2件、OpenAI/Anthropic/Vertex/Bedrock（BYO‑Key）またはオンプレ
  - ポリシー：no‑cite‑no‑output、PIIマスク、ツール許可リスト、温度/seed固定、SRゲート
  - 目標：一度の内部監査/デューデリジェンス合格（Annex IV / DORA / ISO42001対応）
- 受入/SLA（契約に明記）
  - capture≥98%  replay≥99%  latency overhead≤80ms  pack≤48h
  - `/audit/verify`=OK、MANIFEST.sig 検証OK
- 連携方法：base_url プロキシ / SDK ミドルウェア / Sidecar / ログアダプタ
- 価格の目安：48hサンプル 5–10k控除 / PoC 25–60k（6–8週） / 年間 $100k–300k/テナント（目安）
- クイック検証
  ```bash
  curl -H "x-api-key:$API_KEY" http://<host>/runtime/selfcheck
  curl -H "x-api-key:$API_KEY" -o audit_pack.zip "http://<host>/audit/pack?days=7"
  python mvp/cli/verify_pack.py audit_pack.zip
  ```
- OSS/資料：REM‑Evidence https://github.com/SYNOVAW/REM-Evidence

---

## English (customer brief)

- Product: Verified Inference Runtime (evidence layer). Drop‑in proxy/SDK/sidecar to make any LLM signed, replayable, and audit‑ready.
- 48‑hour deliverable
  - `audit_pack.zip`: MANIFEST.json (sha256), MANIFEST.sig (Ed25519), metrics.json (SR/latency percentiles), audit JSONL (hash chain), replay script, regmap.json (Annex IV/DORA/ISO42001 mapping)
  - Offline verifier: `verify_pack.py` (open source)
- PoC (6–8 weeks) scope
  - 1–2 key use cases; OpenAI/Anthropic/Vertex/Bedrock (BYO‑Key) or on‑prem models
  - Policies: no‑cite‑no‑output, PII masking, tool allowlist, temperature/seed constraints, SR gating
  - Goal: pass one internal audit/due‑diligence (EU AI Act Annex IV / DORA / ISO 42001 ready)
- Acceptance & SLA (contract)
  - capture≥98%, replay≥99%, latency overhead≤80ms, audit_pack≤48h
  - `/audit/verify` returns OK; MANIFEST.sig verification passes
- Integration: base_url proxy (fastest), SDK middleware, sidecar (on‑prem), log adapter (fallback)
- Pricing anchor: 48h sample credit 5–10k / PoC 25–60k (6–8 weeks) / Annual $100–300k/tenant (tiered)
- Quick verify
  ```bash
  curl -H "x-api-key:$API_KEY" http://<host>/runtime/selfcheck
  curl -H "x-api-key:$API_KEY" -o audit_pack.zip "http://<host>/audit/pack?days=7"
  python mvp/cli/verify_pack.py audit_pack.zip
  ```
- OSS & docs: REM‑Evidence https://github.com/SYNOVAW/REM-Evidence

---

Contacts / 連絡先 / 联系方式
- Email: <info@synova-w.com>
- Repo: https://github.com/SYNOVAW/REM-Evidence
