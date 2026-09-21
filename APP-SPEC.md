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

### Project Override (`knowledge/overrides/`)
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
  - Standard foundation reinforcement spacing
  
Project Override (Current Project Exception):
  - Site-specific soil condition requires tighter spacing
  - Valid for Project X only
  - Does not change company standard
```

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
| Approval Authority | Final knowledge approval | **Yes** |

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

### Evidence Integrity
**Threat:** Evidence becomes invalid (link breaks, version changes, removed source)

**Controls:**
- Record source version explicitly
- Track access date
- Periodic verification of sources
- Alert on broken links
- Maintain source archive (future)

### Approval Contamination
**Threat:** Unapproved knowledge accidentally appears approved

**Controls:**
- Explicit status transitions only
- No implicit approval from creation
- No batch approvals without review
- Audit log of all approvals
- Separate draft/approved storage

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

## 10. System Architecture (Code)

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

## 11. Development Session Structure

### Session Types

**SPEC SESSION** (This session)
- Define requirements and architecture
- Create specification documents
- Output: APP-SPEC.md, schema definitions
- Ends: "SPEC READY FOR REVIEW"
- Does NOT implement code

**REVIEW SESSION** (Separate context)
- Independent review of specifications
- Review A: Architecture consistency
- Review B: Completeness
- Review C: Feasibility
- Security review
- Ends: "SPEC APPROVED" or "REVISE REQUIRED"

**BUILD SESSION** (After SPEC approval)
- Implement to specification
- Unit tests included
- Ends: "IMPLEMENTATION READY FOR REVIEW"
- Code review in separate context

**REVIEW SESSION** (Code review)
- Separate context
- Independent code review
- Ends: "APPROVED" or "REVISE REQUIRED"

**FIX SESSION** (If needed)
- Address review findings only
- No scope expansion
- Then return to code review

### Context Isolation
- Each session is separate Claude context
- No bleeding of implementation details into review
- Reviewers see only spec or code, not both
- Prevents bias and conflict of interest

---

## 12. Initial MVP Implementation

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

## 13. Testing Strategy

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

## 14. ADS v4.2 Compliance

This specification follows ADS v4.2 standards:
- **Session Separation:** Different contexts for SPEC/BUILD/REVIEW/FIX
- **Risk Classification:** Knowledge security as elevated risk
- **Independent Review:** Required before approval
- **Security Gates:** Multiple security checkpoints
- **Model Tier Routing:** Standard Tier 1; escalate if needed
- **Human Gates:** No AI self-approval
- **Context Budget:** Keep sessions focused and scoped

---

## 15. Success Criteria

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

## 16. Next Actions

1. **SPEC REVIEW SESSION** (Separate context)
   - Independent review of this specification
   - Fix any gaps or inconsistencies
   - Security review

2. **HUMAN APPROVAL**
   - Manager/Director approval of SPEC
   - Final scope confirmation

3. **BUILD SESSION** (Separate context)
   - Implement to specification
   - Create unit tests
   - Output: Implementation ready for review

4. **CODE REVIEW SESSION**
   - Independent code review
   - Security verification
   - Approval or revision

---

## 17. Document References

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
