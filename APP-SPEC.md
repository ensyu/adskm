# ADSKM: AI Driven Construction Knowledge Management

**Project Version:** 1.0-MVP  
**ADS Version:** 4.2  
**Last Updated:** 2026-09-22  
**Status:** SPECIFICATION - READY FOR REVIEW

---

## 1. Executive Summary

ADSKM is a structured knowledge management system for construction operations. It aggregates site information, validates against evidence, and produces company-standard knowledge through human-approved workflows.

**Core Principle:**
```
Evidence-backed Knowledge + Approval Workflow + Audit Trail + AI Harness
```

**Key Distinction:** ADSKM is not a chat application. It is an Evidence → Approval → Canonical Knowledge system.

---

## 2. Purpose & Goals

### Purpose
Build a knowledge base for construction practices that is:
- **Evidence-backed:** Every knowledge claim has documented source
- **Review-gated:** Independent review before approval
- **Audit-tracked:** Complete change history
- **Human-controlled:** No self-approving AI

### Goals (MVP)
1. Define structured knowledge schema for construction operations
2. Implement evidence validation and source tracking
3. Build approval workflow with human gates
4. Create audit logging for all knowledge changes
5. Store canonical knowledge (Master) and project exceptions (Overrides) separately

### Non-Goals (Not in MVP)
- Web GUI / Dashboard UI
- Mobile application
- Integration with Kanna, Garoon, Box, OneDrive
- Automatic site photo analysis
- All construction phases (only Foundation phase in MVP)
- All building types (only 木造平屋 in MVP)
- Auto-approval workflows
- Fully autonomous agents

---

## 3. Scope (MVP)

### Included
**Building Type:** 木造平屋 (Single-story wooden building)  
**Construction Phase:** 基礎 (Foundation)  
**Task:** 基礎配筋 (Foundation reinforcement)

**Example Knowledge ID:** `KNW-W01-FND-001`

### Excluded from MVP
- 木工事 (Wood framing), 屋根 (Roof), 外壁 (Exterior walls), 設備 (Equipment)
- 内装 (Interior), 断熱 (Insulation), 竣工 (Completion)
- All other building types and construction phases

### Future Scope (Post-MVP)
```
木造平屋 事務所・店舗 (Single-story office/shop)
鉄骨ブレース2階 長屋・賃貸住宅 (2-story steel-braced multi-unit residential)
RC壁構造3階 賃貸住宅 (3-story RC wall-structure multi-unit residential)
```

---

## 4. Architecture

### System Components

```
┌─────────────────────────────────────────────┐
│       Target Selection (Source Input)        │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│    Source Extraction & Validation           │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   Knowledge Structuring (Schema Mapping)    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   Source Audit (Evidence Integrity Check)   │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│    Independent Review (Spec/Implementation) │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│ Security Gate (Data/Knowledge Security)     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Human Approval Gate (Decision)         │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   Canonical Storage (Master or Draft)       │
└──────────────────────────────────────────────┘
```

### Knowledge Storage Hierarchy

```
knowledge/
├─ master/
│  └─ [Company-standard knowledge, approved]
├─ overrides/
│  └─ [Project-specific exceptions, isolated]
├─ drafts/
│  └─ [Evidence-insufficient knowledge, pending]
└─ audit_logs/
   └─ [Change history, immutable records]
```

### Technology Stack (MVP)
- **Language:** Python 3.12+
- **Knowledge Format:** YAML (human-readable, git-friendly, AI-friendly)
- **Schema Validation:** Pydantic
- **Testing:** pytest
- **Version Control:** Git (GitHub repository recommended as primary)
- **Storage:** Filesystem (YAML files) - Not a database

---

## 5. Knowledge Schema

### 5.1 Structured Knowledge Record

```yaml
metadata:
  id: "KNW-W01-FND-001"
  version: "1.0.0"
  building_type: "木造平屋"
  construction_phase: "基礎"
  construction_task: "基礎配筋"
  knowledge_type: "procedure | requirement | specification | standard | practice"
  status: "draft | review_required | approved | rejected | superseded"
  risk_level: "low | medium | high | critical"
  scope: "master | project_override"

content:
  title: "[Clear, descriptive title]"
  summary: "[1-2 sentence overview]"
  
  requirements:
    - "[Requirement 1]"
    - "[Requirement 2]"
  
  checks:
    - "[Verification item 1]"
    - "[Verification item 2]"

source:
  primary_source_type: "law | regulation | manufacturer | design_document | company_standard | approved_procedure | general_practice | field_record | human_input | ai_structured"
  source_classification: "[Same as above]"
  sources:
    - title: "[Source document title]"
      type: "law | regulation | ..."
      version: "[Version number]"
      location: "[URL, file path, or reference]"
      page_reference: "[Page number if applicable]"
      accessed_at: "2026-09-22"
      confidence_level: "high | medium | low"
  evidence_sufficiency: "sufficient | insufficient"
  evidence_notes: "[Any notes about evidence quality or gaps]"

approval:
  created_at: "2026-09-22T10:00:00Z"
  created_by: "human_identifier | ai_process_id"
  reviewed_at: null
  reviewed_by: null
  approved_at: null
  approved_by: null
  approval_comment: null
  last_updated_at: "2026-09-22T10:00:00Z"
  last_updated_by: "human_identifier | ai_process_id"
  update_reason: "[Reason for latest change]"
```

### 5.2 Source Classification

**Critical Rule:** AI cannot unilaterally promote `general_practice` to `company_standard`.

| Classification | Definition | AI Can Create | Approval Required |
|---|---|---|---|
| `law` | Building code, legal requirement | No | Lawyer/Compliance |
| `regulation` | Official regulation (MLIT, etc.) | No | Compliance officer |
| `manufacturer` | Manufacturer specification | Yes | Engineer approval |
| `design_document` | Project-specific design | Yes | Designer/PM approval |
| `company_standard` | Company internal standard | No | Manager/Director |
| `approved_procedure` | Approved company procedure | No | Manager approval |
| `general_practice` | Industry best practice | Yes | **Manager→Standard** |
| `field_record` | Actual field observation | Yes | Supervisor approval |
| `human_input` | Direct human input | Yes | Human verification |
| `ai_structured` | AI structuring of above | Yes | Human review |

**Promotion Path for `general_practice`:**
```
AI discovers general_practice
    ↓
Structures with evidence
    ↓
Independent Review
    ↓
Human Decision
    ↓
Promote to company_standard OR Keep as reference
```

### 5.3 Evidence Rules

**Evidence Sufficiency Criteria:**
- All requirements have documented source
- No contradictions between sources
- Source version is current (not outdated)
- Source accessibility is verifiable
- Confidence levels are explicit

**Knowledge Status Transitions:**

```
draft
  ├─ [Insufficient evidence] ──→ STAYS IN DRAFT
  ├─ [Review requested] ───────→ review_required
  │                              ├─ [Approved] ───→ approved
  │                              ├─ [Rejected] ───→ rejected
  │                              └─ [Revise] ─────→ draft
  ├─ [Superseded] ──────────────→ superseded
  └─ [Approved by human] ───────→ approved
```

**Rule:** Only humans can move knowledge to `approved` status.

---

## 6. Master vs. Override

### Master Knowledge (`knowledge/master/`)
- **Company-standard knowledge**
- **Ownership:** Company management
- **Change Control:** Formal approval process
- **Scope:** All projects unless overridden
- **Access:** Read-only in project context

**Canonical Rules:**
- One source of truth
- Version-controlled
- Audit-logged
- Cannot be modified by projects
- Immutable once approved

### Project Override (`knowledge/overrides/<project_id>/`)
- **Project-specific exceptions**
- **Ownership:** Project team
- **Change Control:** Project-level approval
- **Scope:** Specific project only
- **Access:** Readable, overrides Master in project

**Isolation Rules:**
- Overrides do NOT automatically update Master
- Override changes are project-local
- No permission to modify Master from Override
- Separate approval workflow from Master

**Example:**
```
Master (Company Standard):
  - Standard foundation reinforcement spacing: 200mm
  
Project Override (Current Project Exception):
  - Project X site-specific soil condition requires tighter spacing: 150mm
  - Valid for Project X only
  - Does not change company standard
```

### Master/Override Composition Logic (Runtime)

**How the system loads and applies knowledge with overrides:**

```yaml
# Composition Algorithm
function get_knowledge(knowledge_id, project_id=null):
  
  # 1. Load Master record (always)
  master = load("knowledge/master/{knowledge_id}.yaml")
  
  # 2. Check for Project Override
  if project_id:
    override_path = "knowledge/overrides/{project_id}/{knowledge_id}.yaml"
    if file_exists(override_path):
      override = load(override_path)
    else:
      override = null
  else:
    override = null
  
  # 3. Apply Composition Logic
  if override:
    return compose(master, override, mode="OVERRIDE_PRECEDENCE")
  else:
    return master

function compose(master, override, mode="OVERRIDE_PRECEDENCE"):
  # Mode: OVERRIDE_PRECEDENCE
  # - Override requirements REPLACE master requirements (stricter or different)
  # - Override checks REPLACE master checks
  # - Override evidence is separate from master evidence
  # - Override source tracking independent from master
  
  result = {
    metadata: merge_metadata(master.metadata, override.metadata),
    content: {
      title: override.content.title OR master.content.title,
      summary: override.content.summary OR master.content.summary,
      requirements: override.content.requirements OR master.content.requirements,
      checks: override.content.checks OR master.content.checks,
    },
    source: {
      master_sources: master.source.sources,    # Preserved for reference
      override_sources: override.source.sources, # Project-specific evidence
      applied_source_type: override.source.primary_source_type,
      evidence_sufficiency: override.source.evidence_sufficiency,
    },
    approval: {
      master_approval: master.approval,      # Preserved for reference
      override_approval: override.approval,  # Project approval chain
      effective_approval: override.approval, # Override is operationally effective
    },
  }
  return result
```

**Composition Example:**
```yaml
# Master: KNW-W01-FND-001 (Foundation Reinforcement Standard)
content:
  requirements:
    - Reinforcement spacing: 200mm centers
    - Bar diameter: D13 minimum
    - Concrete cover: 50mm

# Project Override: Project_X/KNW-W01-FND-001
content:
  requirements:
    - Reinforcement spacing: 150mm centers (site-specific soil)
    - Bar diameter: D13 minimum (unchanged)
    - Concrete cover: 50mm (unchanged)

# Composed Result (for Project X):
content:
  requirements:
    - Reinforcement spacing: 150mm centers ← override applied
    - Bar diameter: D13 minimum           ← master value used (no override)
    - Concrete cover: 50mm              ← master value used (no override)
```

**Access Control for Composition:**
- `load_master()` — Read-only, no project ID required
- `load_override(knowledge_id, project_id)` — Accessible only to project members
- `compose()` — Automated; no approval gate
- Result visibility: Master always readable; Override + Composition available only within project context

---

## 7. Approval Workflow

### Approval Stages

**Stage 1: Creation**
- AI or human creates knowledge
- Assigned to `draft` status
- Evidence must be attached

**Stage 2: Independent Review**
- Separate context (different session)
- Review A: Architecture/Spec consistency
- Review B: Implementation correctness
- Review C: Evidence quality
- Security gate assessment
- Knowledge security gate assessment

**Stage 3: Human Approval Gate**
- Manager/appropriate authority reviews
- Decision: `approved`, `rejected`, or `revise`
- If `revise`: Return to draft with specific findings
- If `approved`: Move to canonical status
- If `rejected`: Explain reason, archive to rejected folder

**Automatic Actions:** None. All status changes require explicit human approval.

### Review Roles

| Role | Responsibility | Approval Authority |
|---|---|---|
| Creator | Initial knowledge structuring | No |
| Reviewer A | Spec consistency | No |
| Reviewer B | Implementation quality | No |
| Reviewer C | Evidence quality | No |
| Security Officer | Data/Knowledge security | Yes/No (escalate if concern) |
| Field Supervisor | field_record validation & authenticity | No (escalates to Approval Authority) |
| Approval Authority | Final knowledge approval | **Yes** |

**Field Supervisor Role Details:**
- Validates that field_record observations are authentic and representative
- Ensures observation metadata is complete (date, location, conditions, observer credentials)
- Reviews observation for potential bias or non-typical conditions
- Escalates disputes (field observation vs. general_practice contradiction) to Approval Authority

### Evidence Exception Framework

**When knowledge has insufficient evidence but operational need exists:**

**Criteria for Evidence Exception Request:**
- `evidence_sufficiency: insufficient` AND
- Operational or safety need documented AND
- All available sources cited (cannot do better with current resources) AND
- Risk assessment provided

**Approval Process:**
1. Knowledge creator documents exception request in `evidence_notes` field
2. Reviewer C (Evidence Quality) flags as insufficient
3. Knowledge moves to `review_required` status (explicit)
4. Approval Authority receives exception request with risk assessment
5. Approval Authority decision: `approved_with_exception` OR `rejected`
   - If approved: Requires explicit approval comment documenting risk acceptance
   - If rejected: Knowledge returns to draft for evidence collection

**Example Exception Case:**
```yaml
Knowledge: KNW-W01-FND-001
evidence_sufficiency: insufficient
evidence_notes: |
  Only one source available: company standard from 2020.
  No current MLIT regulation found.
  Site supervisor confirms practice matches observed field conditions.
  Risk: Guideline may be outdated; recommend 1-year review cycle.
approval_comment: "Approved with documented risk: May require update when MLIT 2026 
  standard released. Interim reliance on field validation acceptable. Review by 2027-09-01."
```

---

## 8. Knowledge Security

### Knowledge Poisoning Prevention
**Threat:** Incorrect or malicious information becomes company standard

**Controls:**
- Evidence requirement (no claims without sources)
- Source classification (track origin)
- Independent review (catch inconsistencies)
- Audit log (detect unauthorized changes)
- Human approval gate (final human oversight)

**Operational Safeguards:**

1. **AI Hallucination Detection**
   - Reviewer C (Evidence Quality) verifies that AI-structured sources actually match claimed source documents
   - Requirement: Source verification step must cite specific page/section of claimed source
   - If unverifiable: Confidence level marked as "low" or rejected

2. **Field Record Validation**
   - Field Supervisor reviews field_record observations for authenticity
   - Checks: observation date, location, conditions, observer credentials
   - Flags: potentially biased observations, non-typical conditions
   - Escalation: If field_record contradicts general_practice → USER_DECISION_REQUIRED

3. **Knowledge Aging Review**
   - Automated: Audit log provides age tracking (created_at, last_updated_at)
   - Manual frequency: All company_standard records reviewed annually minimum
   - Triggers: Source version change, regulation update, risk level increase
   - Owner: Knowledge Steward role (assigned ownership required)
   - Decision: Supersede, refresh evidence, or keep current

### Evidence Integrity
**Threat:** Evidence becomes invalid (link breaks, version changes, removed source)

**Controls:**
- Record source version explicitly
- Track access date
- Periodic verification of sources
- Alert on broken links
- Maintain source archive (future)

**Operational Implementation:**

1. **Source Location Verification**
   - Implementation: URL validation (HTTP/HTTPS scheme, accessible)
   - Frequency: At creation time; optional periodic re-verification
   - Failure handling: Log as warning; mark evidence_sufficiency as "insufficient" if critical source inaccessible

2. **Broken Source Handling**
   - Detection: Manual (Audit log review) or future automated (link checker)
   - Procedure: When approved knowledge has broken source:
     - Create superseding record with updated sources
     - Mark original as "evidence_compromised"
     - Notify affected projects using this knowledge
     - Requires re-approval of superseded knowledge
   - Recovery: Source archive (post-MVP) enables historical evidence preservation

3. **Evidence Replacement Control**
   - Policy: Changing source evidence triggers notification to prior reviewers
   - Contradiction detection: If new evidence contradicts prior evidence → escalate to Reviewer C
   - Re-approval: Evidence-only changes do NOT require full review if contradiction absent; audit-logged as "evidence_update"

### Approval Contamination
**Threat:** Unapproved knowledge accidentally appears approved

**Controls:**
- Explicit status transitions only
- No implicit approval from creation
- No batch approvals without review
- Audit log of all approvals
- Separate draft/approved storage

**Operational Implementation:**

1. **Access Control Enforcement**
   - Master knowledge: File permissions read-only after approval (chmod 444)
   - Draft knowledge: Readable only to creator/assigned reviewers
   - Override knowledge: Accessible only to project members
   - Implementation: Service layer validates access before load/save

2. **Approval Metadata Integrity**
   - Audit log: Append-only YAML files (no retroactive modification)
   - Future: Immutable ledger with cryptographic hashing
   - Requirement: Approval records include timestamp, approver ID, approval_comment
   - Cryptographic verification deferred post-MVP; documented in DEVELOPMENT.md

3. **Unapproved Knowledge Operational Use Prevention**
   - Technical boundary: `load_master()` returns only approved records
   - Draft/Override knowledge not returned by default
   - Explicit opt-in required: `load_draft(knowledge_id, project_id)` for project-level access

### Typical Security Concerns (Also Assessed)
- Data leakage (Confidential project info)
- Credential leakage (API keys, passwords)
- Personal information (Names, contact details)
- Customer information (Client data)
- Company confidential data (Proprietary standards)
- External API misuse
- MCP unauthorized access
- File access boundaries

---

## 9. Audit Log

### Recorded Information

For every knowledge change:
```yaml
audit_entry:
  timestamp: "2026-09-22T14:30:00Z"
  change_id: "AUD-001"
  who: "human_name | ai_process_id"
  action: "create | update | approve | reject | review | escalate"
  knowledge_id: "KNW-W01-FND-001"
  previous_version: "0.9.0"
  new_version: "1.0.0"
  previous_status: "draft"
  new_status: "review_required"
  evidence_changed: true
  field_changed: ["summary", "requirements"]
  reason: "[Why this change was made]"
  approval_comment: "[If approved/rejected, reason]"
  security_notes: "[Any security-relevant details]"
```

### Audit Log Purpose
- Compliance verification
- Change traceability
- Forensic analysis
- Rollback capability (future)
- Human oversight verification

**Immutability Note:** Future versions may use immutable ledger; for now, audit logs are append-only YAML files.

---

## 10. Operational & Implementation Details

### 10.1 YAML Security Requirements (CRITICAL)

**Threat Model:** YAML injection attacks, arbitrary code execution, DoS attacks

**Safe Parsing Mandate (CRITICAL):**
- **ALL YAML parsing MUST use `yaml.safe_load()` exclusively**
- **NEVER use `yaml.load()`** — arbitrary code execution vulnerability
- **Enforcement:** Pydantic validator + service-layer checks

**Maximum File Size Limit:**
- Knowledge records: Maximum 1 MB per file
- Rationale: Prevent DoS attacks via oversized payloads
- Enforcement: Check file size before `yaml.safe_load()`; reject > 1MB with error

**Implementation Checklist:**
```python
# Pseudocode
def load_knowledge_yaml(file_path):
  # 1. Check file size
  if os.path.getsize(file_path) > 1_000_000:
    raise ValueError("Knowledge file exceeds 1 MB limit")
  
  # 2. Use safe_load ONLY
  with open(file_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
  
  # 3. Validate against schema
  validated = KnowledgeRecord(**data)
  return validated
```

**Testing Requirements:**
- Unit test: YAML injection attempt must be rejected with clear error
- Integration test: Verify `yaml.load()` is never called in codebase
- Pre-commit hook: Prevent commits containing `yaml.load()` (non-safe-load usage)

---

### 10.2 Input Validation & Sanitization

**Knowledge ID Format Validation:**
```
Format: KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}
Example: KNW-W01-FND-001
Regex: ^KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}$
Rejection: Any ID not matching format
```

**Path Traversal Prevention (CRITICAL):**
- Reject any ID containing: `..`, `./`, `~`, symlinks, path separators (`\`, `/`)
- Implementation: Normalize paths using `pathlib.Path.resolve()`
- Validation: Confirm all file operations stay within `knowledge/` directory
- Cross-platform: Works on Windows + Unix/Linux

**Field Length Limits:**
| Field | Max Length | Rationale |
|---|---|---|
| `title` | 100 chars | Prevent unbounded metadata |
| `summary` | 500 chars | Knowledge overview brevity |
| `approval_comment` | 2000 chars | Detailed approval rationale |
| `evidence_notes` | 5000 chars | Complex evidence documentation |
| URL in source | 2048 chars | Standard URL limit |

**URL Validation:**
- Scheme: Must be `http://` or `https://` only
- Domain: Optional internal whitelist (e.g., company intranet)
- **Explicit prohibition:** No credentials in URL parameters (`username:password@host`)
- Validation: urllib.parse + regex check

**String Sanitization:**
- Remove control characters (0x00–0x1F except `\n`, `\t`, `\r`)
- Encoding: UTF-8 only; reject invalid UTF-8 sequences
- Whitespace: Normalize CRLF to LF; trim leading/trailing spaces

**Implementation:**
```python
# In Pydantic validators
class KnowledgeRecord(BaseModel):
  id: str = Field(..., regex=r'^KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}$')
  content: ContentModel

  @validator('id')
  def validate_no_path_traversal(cls, v):
    if '..' in v or '/' in v or '\\' in v or '~' in v:
      raise ValueError("Path traversal characters not allowed in ID")
    return v
```

**Testing Requirements:**
- Unit test: Path traversal attempts rejected (`../../../`, `~user/`, symlinks)
- Unit test: YAML injection attempt rejected
- Unit test: Field length limits enforced
- Unit test: Invalid UTF-8 sequences rejected

---

### 10.3 Audit Log Immutability Enforcement

**Threat Model:** Tampering with audit records, retroactive modification, evidence of approvals altered

**MVP Implementation: Append-Only File Strategy**

1. **Write Operation Rules:**
   - New entries appended only; no retroactive modification
   - No in-process modification of closed audit files
   - File permissions set to `444` (r--r--r--) after audit rotation
   - Audit entries immutable once written

2. **Concurrency Control (MANDATORY):**

   **Unix/Linux (fcntl-based):**
   ```python
   import fcntl

   def append_audit_entry(entry):
     with open(audit_file_path, 'a') as f:
       fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
       try:
         yaml.safe_dump([entry], f, append=True)
       finally:
         fcntl.flock(f.fileno(), fcntl.LOCK_UN)  # Unlock
   ```

   **Windows (LockFile API):**
   ```python
   import msvcrt

   def append_audit_entry(entry):
     with open(audit_file_path, 'a') as f:
       msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
       try:
         yaml.safe_dump([entry], f, append=True)
       finally:
         msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
   ```

3. **Mutex-based In-Memory Locking:**
   - For concurrent processes within same VM
   - Per-audit-file mutex; prevents race conditions
   - Implementation: `threading.Lock` (single-process) or `multiprocessing.Lock` (multi-process)

4. **Read Access Control:**
   - Always consult most recent file state
   - Audit logs: Read-only after append
   - Access: Approval Authority + Auditors only
   - No permission to delete or modify audit entries

5. **Access Control Matrix:**
   ```yaml
   audit_logs/ permissions:
     - Owner: deployment service account
     - Permissions: 444 (r--r--r--)
     - Append: Only audit_service.append() can write
     - Read: Approval Authority + Auditors only
     - Delete: NEVER (audit trail immutable)
   ```

**Post-MVP: Cryptographic Ledger (Q1 2027 Target)**
- Algorithm: SHA-256 hash-chain (each entry includes hash of previous)
- Verification: Entry tampering detected by hash mismatch
- Immutability proof: Sequential hashes form unbreakable chain
- Migration path: Export existing YAML, migrate to ledger format

**Implementation Roadmap:**
- **Q4 2026 (MVP):** File locking + append-only YAML
- **Q1 2027:** Design cryptographic ledger specification
- **Q2 2027:** Implement hash-chain ledger
- **Q3 2027:** Migration tools + verification utilities

**Testing Requirements:**
- Unit test: Concurrent writes from multiple processes → entries recorded in order
- Unit test: Audit log cannot be retroactively modified
- Integration test: Verify file locking prevents race conditions
- Cross-platform test: Unix fcntl + Windows LockFile both functional

---

### 10.4 Versioning Policy

**Version Numbering: Semantic Versioning (MAJOR.MINOR.PATCH)**

When to increment:

```yaml
MAJOR version:
  - Knowledge requirement structure fundamentally changes (requirement added/removed)
  - Approval status transitions to superseded (knowledge wholly replaced)
  - Scope changes (master ↔ project_override)
  
MINOR version:
  - Evidence updated (sources added/changed/removed)
  - evidence_sufficiency changes (insufficient → sufficient)
  - Source version changes (e.g., regulation updated)
  - confidence_level changes across sources
  
PATCH version:
  - Metadata-only changes (approval_comment, title refinement)
  - status changes (draft → review_required)
  - Non-content field updates (knowledge_type, risk_level adjustment)
```

**Implementation:** Audit log `new_version` field increments automatically; creator/reviewer cannot manually override.

### 10.5 Error Handling & Recovery

**YAML Parse Failures**
- Symptom: Malformed YAML syntax in knowledge files
- Response: Log error with file path and line number; skip file; continue processing others
- Recovery: Manual human intervention required; file moved to `knowledge/corrupted/` for review
- Alert: Operator notification for manual remediation

**Pydantic Validation Failures**
- Symptom: Required field missing, type mismatch, enum value invalid
- Response: Return detailed field-level errors to creator/reviewer
- Recovery: Prevent save to master/; allow save to drafts/ for revision with error details
- Decision: Require explicit error correction before re-submission

**Audit Log Write Failures**
- Symptom: Cannot append to audit log file (permissions, disk full, I/O error, locking timeout)
- Response: **CRITICAL** — do not finalize knowledge save; rollback transaction
- Recovery: Rollback knowledge record to previous state; raise alert to operator
- Rationale: Audit trail integrity is non-negotiable

**Source Accessibility Failures**
- Symptom: URL unreachable, file path invalid, source not found
- Response: Log as warning in evidence_notes; do NOT block knowledge creation
- Recovery: Manual decision to proceed with insufficient evidence or locate alternative source
- Escalation: If critical source inaccessible → Evidence Exception pathway (Section 7)

**Broken Source in Approved Knowledge**
- Symptom: Periodic verification detects source link now broken
- Response: Trigger knowledge review; create superseding record with updated sources
- Recovery: Previous knowledge marked as "evidence_compromised"; manual decision to update or retire
- Notification: Alert all projects using this knowledge

### 10.6 Access Control Model

**File-level Permissions (Filesystem)**

```yaml
knowledge/master/
  - Owner: deployment service account
  - Permissions: 550 (rwxr-x---)
  - File permission after approval: 440 (r--r-----)
  - Write-protect once approved: immutable in operational use

knowledge/overrides/<project_id>/
  - Owner: project service account
  - Permissions: 770 (rwxrwx---)
  - Readable by: project team members
  - Not readable by: other projects, general public

knowledge/drafts/
  - Owner: creator/assigned reviewer
  - Permissions: 600 (rw-------)
  - Accessible only to: creator, assigned reviewers

knowledge/audit_logs/
  - Owner: deployment service account
  - Permissions: 444 (r--r--r--)
  - Append-only: locking mechanism prevents concurrent writes
```

**Service-layer Access Control**

```python
# Pseudocode for KnowledgeService access checks

def load_master(knowledge_id):
  # Always allowed; read-only access to approved master knowledge
  validate_knowledge_id_format(knowledge_id)
  return read_file(f"knowledge/master/{knowledge_id}.yaml")

def load_draft(knowledge_id, user_id):
  # Restricted: creator and assigned reviewers only
  draft = read_file(f"knowledge/drafts/{knowledge_id}.yaml")
  if draft.created_by != user_id and user_id not in draft.assigned_reviewers:
    raise AccessDenied("Not authorized to view draft knowledge")
  return draft

def load_override(knowledge_id, project_id, user_id):
  # Restricted: project members only
  if not is_project_member(project_id, user_id):
    raise AccessDenied("Not authorized to access project overrides")
  return read_file(f"knowledge/overrides/{project_id}/{knowledge_id}.yaml")

def save_master(knowledge_record, approver_id):
  # Restricted: Approval Authority only; triggers immutability
  if not has_approval_authority(approver_id):
    raise AccessDenied("Insufficient authorization to approve knowledge")
  write_file(f"knowledge/master/{knowledge_record.id}.yaml", knowledge_record)
  set_file_immutable(f"knowledge/master/{knowledge_record.id}.yaml")
```

### 10.7 Interaction Model (MVP Limitation)

**Current State:** No CLI/Web UI in MVP

**Workaround for MVP:**
- Knowledge creation/approval conducted via Python scripts + manual YAML editing
- Test case: Demonstrate full workflow with KNW-W01-FND-001 example record
- Assumption: MVP operators are technically capable (engineers, not construction workers)

**Post-MVP Requirement:**
- CLI interface (minimal viable): `adskm knowledge register`, `adskm knowledge approve`
- Web UI (future): Project dashboard, knowledge search, approval workflow UI

---

## 11. System Architecture (Code)

### Directory Structure
```
adskm/
├── src/adskm/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── knowledge.py         # Knowledge schema (Pydantic)
│   │   ├── project_override.py  # Project override schema
│   │   └── audit_log.py         # Audit entry schema
│   ├── services/
│   │   ├── __init__.py
│   │   ├── knowledge_service.py # Load/save knowledge
│   │   ├── override_service.py  # Project override management
│   │   └── audit_service.py     # Audit log operations
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── evidence_validator.py   # Evidence quality checks
│   │   ├── source_validator.py     # Source validation
│   │   └── schema_validator.py     # Schema validation
│   ├── security/
│   │   ├── __init__.py
│   │   ├── knowledge_security.py   # Knowledge-specific security checks
│   │   └── data_security.py        # General data security
│   └── pipeline/
│       ├── __init__.py
│       └── harness.py              # Main harness orchestration
├── knowledge/
│   ├── master/                  # Company-standard knowledge
│   ├── overrides/               # Project-specific overrides
│   ├── drafts/                  # Evidence-insufficient knowledge
│   └── audit_logs/              # Change history
├── tests/
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_validation.py
│   ├── test_security.py
│   └── test_audit.py
├── docs/
│   ├── ADSKM-OVERVIEW.md        # High-level overview
│   ├── KNOWLEDGE-SCHEMA.md      # Detailed schema documentation
│   ├── PROJECT-OVERRIDE-SCHEMA.md # Override schema details
│   └── DEVELOPMENT.md           # Development guidelines
├── scripts/
│   ├── init_knowledge.py        # Initialize sample knowledge
│   └── validate_all.py          # Validate all knowledge
├── APP-SPEC.md                  # This file
├── README.md                    # Quick start
├── AGENTS.md                    # ADS v4.2 agent roles
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
└── .github/workflows/           # CI/CD (future)
```

---

## 12. Development Flow (ADS v4.2 Autonomous Model)

ADSKM follows official ADS v4.2.0 standard with autonomous execution:

```
User Request
    ↓
HEAD AGENT Orchestration
    ├─ Build SPEC
    ├─ BUILD Sub-Agent: Implementation
    ├─ REVIEW Sub-Agents: Independent Review
    │  ├─ Review A: Architecture/Spec
    │  ├─ Review B: Implementation/Impact
    │  ├─ Review C: Quality/Operation
    │  ├─ Security Gate: General
    │  └─ Knowledge Security: ADSKM-specific
    ├─ SECURITY Sub-Agent: Issue remediation
    ├─ FIX Sub-Agent: Address findings
    └─ Autonomous loop to TRIAL-READY
    ↓
TRIAL-READY
    ↓
USER_DECISION_REQUIRED
  (Company standard approval, evidence exceptions, high-risk knowledge)
    ↓
Human Approval → Canonical Master
    ↓
EXTERNAL_ACTION_APPROVAL
  (Formal release, production deployment)
    ↓
Released
```

### Stopping Conditions (ADS v4.2)

**No human gates between technical phases.**

**Only 2 stopping conditions:**

1. **USER_DECISION_REQUIRED**
   - Business decisions: Company standard approval, evidence exceptions, risk decisions
   - AI completes TRIAL-READY and awaits human decision

2. **EXTERNAL_ACTION_APPROVAL**
   - External/irreversible: Formal release, production deployment, real-world impact
   - Requires explicit human authorization before proceeding

### USER_DECISION_REQUIRED Mapping (Detailed)

**Explicit triggers requiring human business decision:**

```yaml
USER_DECISION_REQUIRED Triggers:

1. Company Standard Adoption
   - When: Knowledge is promoted from general_practice to company_standard
   - Who: Manager/Director approval authority
   - Decision: "Is this industry practice appropriate for our company standard?"
   - Escalation: Risk-weighted (low-risk → fast-track, high-risk → executive review)

2. Evidence Exceptions
   - When: Knowledge has insufficient evidence but operational need exists
   - Who: Approval authority + Risk officer sign-off
   - Decision: "Accept evidence gap? Required safety justification?"
   - Threshold: Evidence_sufficiency = insufficient + risk_level >= high

3. Project Override → Master Promotion
   - When: Proven project override has company-wide value
   - Who: Manager + Approval authority
   - Decision: "Should this project exception become company standard?"
   - Example: Site-specific soil condition → becomes foundation standard

4. High-Risk Knowledge Adoption
   - When: risk_level = critical OR risk_level = high + novel_knowledge
   - Who: Director/Technical authority + Risk/Safety officer
   - Decision: "Approve high-risk knowledge? Mitigation plan?"
   - Documentation: Requires signed approval comment + risk assessment

5. Conflicting Evidence Sources
   - When: Multiple sources provide contradictory requirements
   - Who: Subject matter expert + Approval authority
   - Decision: "Which source precedence? Why? Reconciliation approach?"
   - Escalation: Cannot auto-resolve; requires expert judgment

6. General Practice → Field Record Dispute
   - When: field_record contradicts accepted general_practice
   - Who: Supervisor + Field expert + Approval authority
   - Decision: "Update standard based on field observation?"
   - Rationale: Prevents AI from over-weighting single observations
```

**Non-triggers (Auto-processed by HEAD AGENT):**
- Evidence collection and structuring ✅
- Source validation and classification ✅
- Independent review findings ✅
- Security gate remediation ✅
- YAML format and schema compliance ✅
- Versioning and audit logging ✅

### Independent Review (Sub-Agent based)

All reviews use **isolated Sub-Agent contexts within single conversation:**

- **Review A:** Architecture/Spec (isolated context, no Review B/C output)
- **Review B:** Implementation/Impact (isolated, no Review A/C output)
- **Review C:** Quality/Operation (isolated, no Review A/B output)
- **Security Gate:** General security (isolated)
- **Knowledge Security:** ADSKM-specific (isolated)

**Key:** Each reviewer gets only their evaluation criteria, not other reviewers' conclusions.

---

## 13. Initial MVP Implementation

### Phase 1: Schema & Models
```
1. Implement Pydantic models for Knowledge
2. Implement ProjectOverride schema
3. Implement AuditLog schema
4. Add schema validation
5. Add evidence validation
6. Test YAML load/save
```

### Phase 2: Services
```
1. KnowledgeService (load/save master knowledge)
2. OverrideService (manage project overrides)
3. AuditService (record all changes)
4. ValidationService (evidence & source checking)
```

### Phase 3: Security
```
1. Knowledge security checks
2. Data security baseline
3. Source integrity verification
```

### Phase 4: First Knowledge Record
```
1. Create KNW-W01-FND-001 (Foundation reinforcement standard)
2. Attach evidence
3. Demonstrate full workflow
4. Test approval workflow
```

### Not Included in MVP
- CLI interface (future)
- Web API (future)
- Database (use YAML files)
- GUI/Dashboard
- Integration workflows
- Auto-approval
- Sync with external systems

---

## 14. Testing Strategy

### Unit Tests
- Model validation
- Schema conformance
- Evidence checking
- Service logic

### Integration Tests
- Knowledge load/save/update
- Override behavior
- Audit log recording
- Approval status transitions

### Validation Tests
- YAML parsing
- Schema compliance
- Source verification
- Evidence sufficiency

**Test Coverage Target:** 80%+ for core services

---

## 15. ADS v4.2 Compliance

This specification adopts official ADS v4.2.0 standard:

**ADS v4.2 Core Model:**
```
ONE REQUEST. ONE CONVERSATION. AUTONOMOUS EXECUTION TO TRIAL-READY.
```

**Compliance:**
- ✅ **Autonomous Execution:** HEAD AGENT orchestrates BUILD → REVIEW → SECURITY → FIX loops
- ✅ **No Phase Gates:** Technical phases loop autonomously; only 2 stopping conditions
- ✅ **Sub-Agent Review:** Independent review using isolated contexts (not separate sessions)
- ✅ **USER_DECISION_REQUIRED:** Business decisions (company standard approval, evidence exceptions)
- ✅ **EXTERNAL_ACTION_APPROVAL:** Formal release and external operations only
- ✅ **Model Tier Routing:** Tier 1 baseline; Tier 2/3 escalation if needed
- ✅ **Risk Classification:** Knowledge security as specialized risk domain

**ADSKM Extensions (not overrides):**
- Knowledge Poisoning prevention
- Evidence Integrity tracking
- Approval Contamination prevention
- Master/Override isolation
- Knowledge Security gates (separate from general Security)

**Reference:** ADS v4.2.0 official (E:\dev\ai-dev-standard, tag v4.2.0)

---

## 16. Success Criteria

### MVP Success
- [ ] APP-SPEC.md approved
- [ ] Knowledge schema fully defined and validated
- [ ] Master/Override/Draft storage implemented
- [ ] Evidence validation working
- [ ] Approval workflow functional
- [ ] Audit log recording all changes
- [ ] First knowledge record (KNW-W01-FND-001) created with evidence
- [ ] No knowledge self-approval by AI
- [ ] All approval gates working

### Quality Criteria
- [ ] Spec matches implementation
- [ ] Evidence requirements enforced
- [ ] No unapproved knowledge in master
- [ ] Audit trail complete and verifiable
- [ ] All tests passing (pytest)
- [ ] No security vulnerabilities
- [ ] Code review approved

---

## 16.1 MVP Constraints (Intentional)

The following limitations are **intentional MVP design decisions**, not oversight:

### Knowledge Aging
- **Constraint:** Knowledge aging review is **manual** in MVP
- **How it works:** Site subject matter experts periodically review knowledge records
- **Decision trigger:** Human decides when knowledge is outdated or needs superseding
- **Future enhancement:** Automatic detection of knowledge exceeding age threshold (Post-MVP)
- **Rationale:** MVP prioritizes quality over automation; manual review ensures careful transitions

### Database Deferral
- **Constraint:** YAML files + Git, no relational database
- **Rationale:** Sufficient for single-phase MVP; clearer audit trail with Git history
- **Future:** Database considered when multi-phase/multi-building scaling requires

### External Integrations (Post-MVP)
- Kanna, Garoon, Box, OneDrive: Deferred
- MCP authorization: Deferred
- Automatic photo analysis: Deferred
- Web API: Deferred

---

## 17. Next Actions (ADS v4.2 Autonomous Model)

Following ADS v4.2 standard, next steps are automated under HEAD AGENT orchestration:

1. **SPEC Finalization Review** (Sub-Agent, isolated context)
   - Review A: Specification completeness and architecture
   - Review B: Implementation feasibility
   - Review C: Operational suitability
   - Security Gate: General security assessment
   - Knowledge Security Gate: Knowledge-specific threats

2. **BUILD Phase** (Sub-Agent, if SPEC reviewers PASS)
   - Implementation to SPEC
   - Unit test creation
   - Local validation

3. **REVIEW Phase** (Sub-Agents, isolated contexts)
   - Code/Implementation review
   - Quality verification
   - Security deep-dive
   - Knowledge Security re-check

4. **FIX Phase** (Sub-Agent, if findings detected)
   - Address review findings
   - Re-test and re-verify
   - Loop back to Review if needed

5. **TRIAL-READY** (Autonomous completion)
   - All sub-agent reviews PASS
   - Security gates cleared
   - Knowledge security verified
   - 80%+ test coverage

6. **USER_DECISION_REQUIRED** (Stop condition)
   - Business approval decision needed
   - Company standard Knowledge adoption
   - Evidence exception handling
   - High-risk Knowledge approval

7. **EXTERNAL_ACTION_APPROVAL** (Stop condition if needed)
   - Formal release authorization
   - Production deployment approval

**No human gates between technical phases (SPEC/BUILD/REVIEW/FIX).** HEAD AGENT loops autonomously until TRIAL-READY or stopping condition.

---

## 18. Document References

- **ADSKM-OVERVIEW.md** - High-level system overview
- **KNOWLEDGE-SCHEMA.md** - Detailed schema specifications
- **PROJECT-OVERRIDE-SCHEMA.md** - Override schema details
- **DEVELOPMENT.md** - Developer guidelines
- **AGENTS.md** - ADS v4.2 agent roles and responsibilities

---

**END OF APP-SPEC.md**

---

**Status:** ✅ SPECIFICATION READY FOR REVIEW

**Next Gate:** Human approval after independent review
