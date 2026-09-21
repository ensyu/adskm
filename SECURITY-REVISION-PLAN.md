# ADSKM SPEC - Security Gate REVISE 対応計画

**Date:** 2026-09-22  
**Status:** REVISION PLAN - Implementation Ready  
**Target:** Security Gate の 3 critical gaps を修正

---

## 重大ギャップと修正計画

### Gap 1: YAML Safe Parsing Mandate (CRITICAL)

**現状:**
- yaml.safe_load() の requirement が SPEC に明記されていない
- arbitrary code execution 脅威がドキュメントされていない

**修正内容:**
- **追加場所:** Section 10.2 の前に新セクション "10.2.1 YAML Security Requirements" を追加
- **内容:**
  ```
  1. Safe Parsing (Critical)
     - ALL YAML parsing MUST use yaml.safe_load() exclusively
     - NEVER use yaml.load() (arbitrary code execution risk)
     - Threat model: YAML Injection attacks
     - Mitigation: yaml.safe_load() disables unsafe constructors
  
  2. Maximum File Size Limit
     - Knowledge records: Maximum 1 MB per file
     - Rationale: DoS attack prevention
     - Enforcement: Check file size before parsing; reject > 1MB
  
  3. Implementation Checklist
     - Use PyYAML with safe_load() exclusively
     - Test: YAML injection must be rejected with error
     - Timeout configuration for large file handling
  ```

**BUILD Phase での実装:**
- requirements.txt に "PyYAML>=6.0" と明示的に記載
- src/adskm/services/ に yaml_validator.py を追加
- Unit test: test_security.py に YAML injection test case 追加

---

### Gap 2: Input Validation & Sanitization Rules (CRITICAL)

**現状:**
- validate_knowledge_id_format() が呼ばれているが実装不明確
- Path traversal prevention が未指定
- Field length limits がない

**修正内容:**
- **追加場所:** Section 10.3 を拡張して新サブセクション "10.3.1 Input Validation & Sanitization" を追加
- **内容:**
  ```
  1. Knowledge ID Validation
     - Format: KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}
     - Example: KNW-W01-FND-001
     - Implementation: Use regex validation
  
  2. Path Traversal Prevention
     - Reject any ID containing: .., ./, ~, symlinks
     - Normalize paths using pathlib.Path.resolve()
     - Validate all file operations stay within knowledge/ directory
  
  3. Field Length Limits
     - title: max 100 characters
     - summary: max 500 characters
     - approval_comment: max 2000 characters
     - evidence_notes: max 5000 characters
  
  4. URL Validation
     - Scheme: Must be http:// or https://
     - Domain: Optional whitelist for internal sources
     - No credentials in URL parameters
  
  5. String Sanitization
     - Remove control characters (0x00-0x1F except \n \t \r)
     - Encoding: UTF-8 only, reject invalid sequences
  ```

**BUILD Phase での実装:**
- src/adskm/validation/input_validator.py を作成
- Pydantic validators を活用（Field constraints）
- Unit test: test_validation.py に injection/traversal test cases

---

### Gap 3: Audit Log Immutability Enforcement (CRITICAL)

**現状:**
- "append-only YAML files" と記載されているが locking mechanism 未指定
- 同時実行書き込み対策が曖昧
- Immutable ledger は Post-MVP に deferred だが no roadmap

**修正内容:**
- **追加場所:** Section 9 "Audit Log" を拡張
- **内容:**
  ```
  ## Audit Log Immutability Enforcement

  ### MVP Implementation
  1. Append-Only File Strategy
     - New entries appended only; no retroactive modification
     - File permissions: 444 (r--r--r--) after close
     - No in-process modification of closed audit files

  2. Concurrency Control
     - File locking mechanism (mandatory):
       - Unix: fcntl-based locking (fcntl.flock)
       - Windows: LockFile API or file handle locking
     - Mutex-based in-memory locking for concurrent processes
     - Read: Always consult most recent file state
  
  3. Access Control
     - Audit logs are append-only after creation
     - Only audit_service.append() can write (no update/delete)
     - Read access: Approval Authority + Auditors only
  
  ### Post-MVP: Cryptographic Ledger (Q1 2027 Target)
  - Algorithm: SHA-256 hash-chain (each entry includes hash of previous)
  - Verification: Entry tampering detected by hash mismatch
  - Immutability proof: Sequential hashes form unbreakable chain
  - Migration path: Export existing YAML, migrate to ledger format
  
  ### Implementation Roadmap
  - Q4 2026 (MVP): File locking + append-only YAML
  - Q1 2027: Design cryptographic ledger specification
  - Q2 2027: Implement hash-chain ledger
  - Q3 2027: Migration tools + verification utilities
  ```

**BUILD Phase での実装:**
- src/adskm/services/audit_service.py に locking 実装
- Cross-platform compatibility (Unix fcntl + Windows LockFile)
- Unit test: test_audit.py に concurrent write test cases

---

## 修正優先度

| Gap | 優先度 | MVP PASS 要件 | Build Phase での実装期限 |
|-----|--------|---------------|-----------------------|
| YAML Safe Parsing | **P0** | MUST | Weeks 1-2 |
| Input Validation | **P0** | MUST | Weeks 1-2 |
| Audit Log Immutability | **P0** | MUST | Weeks 1-2 |

---

## Secondary Items (Priority 2 - Before MVP Release)

### Credential Handling Policy (Section 8 拡張)
```
新サブセクション: "8.3.1 Credential Protection Policy"

1. Explicit Prohibition
   - No credentials, API keys, passwords, authentication tokens in knowledge records
   - Violation check: Unit test must reject credential patterns

2. Credential Pattern Detection
   - Regex patterns: AWS keys (AKIA...), Azure connections, generic API patterns
   - Pre-commit hook: Prevent commit if patterns detected

3. Safe Storage for Evidence Sources
   - Credentials required for evidence sources: Use environment variables or vault
   - Never store in YAML; reference by named environment variable
   - Documentation: How to configure source credentials safely
```

### Approval Authority Formal Definition (Section 7 拡張)
```
新サブセクション: "7.2.1 Approval Authority Definition"

1. Role Qualification
   - Must have director/manager-level role
   - Validation: has_approval_authority(user_id) checks role level

2. Authorization Rules
   - company_standard promotion: Director level minimum
   - high-risk knowledge: Director + Safety Officer sign-off
   - override approval: Project Manager level sufficient

3. Escalation Matrix
   - risk_level: low → fast-track (1 day)
   - risk_level: medium → normal (3 days)
   - risk_level: high/critical → executive review (5+ days)
```

### API/MCP Security Post-MVP Roadmap (Section 16 拡張)
```
新サブセクション: "16.2 API/MCP Security Post-MVP Roadmap"

Timeline:
- Q1 2027: API security model design + stakeholder review
- Q2 2027: Minimal read-only API (authentication + rate limiting)
- Q3 2027: MCP authorization layer design
- Q4 2027: Full external integration support (Kanna, Garoon)

Authorization Model (TBD in Q1 2027):
- API Keys: Simple for internal services
- OAuth 2.0: For third-party integrations
- mTLS: For machine-to-machine with MCP

Rate Limiting:
- Default: 100 req/min per API key
- Tier 2: 1000 req/min (approved integrations)

Audit Trail:
- All API calls logged with endpoint, user, resource, timestamp
- Searchable audit records in knowledge/audit_logs/api/
```

---

## 実装ロードマップ

**Week 1-2 (MVP BUILD):**
- [ ] 10.2.1 YAML Security Requirements を SPEC に追加
- [ ] 10.3.1 Input Validation & Sanitization を SPEC に追加
- [ ] Section 9 Audit Log Immutability を拡張
- [ ] これら3つの Gap に対応する実装コード
- [ ] Unit tests 作成（YAML injection、path traversal、concurrent writes）

**Week 3-4 (MVP BUILD Continuation):**
- [ ] Credential handling policy を SPEC に追加
- [ ] Approval Authority formal definition を SPEC に追加
- [ ] API/MCP security roadmap を SPEC に追加
- [ ] Integration tests 実行

**Pre-MVP Release:**
- [ ] SPEC documentation review and cleanup
- [ ] SECURITY-REVISION-PLAN.md を DEVELOPMENT.md にマージ
- [ ] Build-phase TODO リストとして実装チームに引き継ぎ

---

## Validation Checklist

Before Security Gate の再レビュー:
- [ ] YAML security section は SPEC に明記されている
- [ ] Input validation regex patterns は実装可能
- [ ] Audit log locking は OS-agnostic
- [ ] Test cases は injection/traversal/concurrent scenarios を cover
- [ ] Secondary items roadmap は explicit

---

**Status:** REVISION PLAN READY FOR IMPLEMENTATION

Next: このプランをコミットし、Security Gate 再レビューを実行。
