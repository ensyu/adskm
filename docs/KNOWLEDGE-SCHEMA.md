# Knowledge Schema Specification

**Version:** 1.0-MVP  
**Last Updated:** 2026-09-22

---

## Overview

This document defines the complete schema for ADSKM Knowledge records. All knowledge must conform to this schema.

---

## 1. Knowledge Record Structure

### Root-Level Fields

```yaml
metadata:          # Required: System metadata
  id: string       # Unique identifier (KNW-{Type}-{Phase}-{Seq})
  version: string  # Semantic version (1.0.0)
  # ... (see section 2)

content:           # Required: Knowledge content
  title: string    # Clear, descriptive title
  summary: string  # 1-2 sentence overview
  requirements: array[string]  # List of requirements
  checks: array[string]         # Verification items

source:            # Required: Evidence and sources
  primary_source_type: enum
  # ... (see section 3)

approval:          # Required: Approval tracking
  # ... (see section 4)
```

---

## 2. Metadata Section

### 2.1 Required Fields

```yaml
metadata:
  id: "KNW-W01-FND-001"           # Naming convention:
                                   # KNW = Knowledge
                                   # W01 = Wood type, variant 1
                                   # FND = Foundation phase
                                   # 001 = Sequence number
  
  version: "1.0.0"                # Semantic versioning
  
  building_type: "木造平屋"        # Building classification
  construction_phase: "基礎"       # Construction phase
  construction_task: "基礎配筋"    # Specific task
  
  knowledge_type: enum            # One of:
                                   # - "procedure"      (Step-by-step process)
                                   # - "requirement"    (Must be met)
                                   # - "specification"  (Technical detail)
                                   # - "standard"       (Company standard)
                                   # - "practice"       (Best practice)
  
  status: enum                    # One of:
                                   # - "draft"            (WIP, incomplete)
                                   # - "review_required"  (Awaiting review)
                                   # - "approved"         (Approved by human)
                                   # - "rejected"         (Not approved)
                                   # - "superseded"       (Replaced by newer)
  
  risk_level: enum                # One of:
                                   # - "low"      (Standard practice)
                                   # - "medium"   (Some complexity/safety)
                                   # - "high"     (Safety-critical)
                                   # - "critical" (Life-safety critical)
  
  scope: enum                     # One of:
                                   # - "master"               (Company standard)
                                   # - "project_override"     (Project exception)
```

### 2.2 Risk Level Guidelines

| Level | Examples | Approval Required |
|-------|----------|-------------------|
| low | Administrative procedures, general practices | Project manager |
| medium | Construction quality specifications, standard checks | Site manager + QA |
| high | Safety procedures, load calculations | Site manager + Safety officer |
| critical | Life-safety systems, structural integrity | Director + Safety officer |

### 2.3 Knowledge Type Guidelines

| Type | Purpose | Example |
|------|---------|---------|
| procedure | Step-by-step instructions | "How to set rebar spacing" |
| requirement | Must-meet conditions | "Rebar must be #4 grade or higher" |
| specification | Technical details | "Minimum rebar diameter: 13mm" |
| standard | Company policy | "All foundations use company rebar spec X" |
| practice | Best practice note | "Double-check spacing before pouring" |

---

## 3. Source Section

### 3.1 Source Classification

```yaml
source:
  primary_source_type: enum       # One of:
    # - "law"               (Binding legal requirement)
    # - "regulation"        (Official regulation)
    # - "manufacturer"      (Manufacturer spec)
    # - "design_document"   (Project design doc)
    # - "company_standard"  (Company policy)
    # - "approved_procedure"(Approved internal process)
    # - "general_practice"  (Industry best practice)
    # - "field_record"      (Actual field observation)
    # - "human_input"       (Direct human statement)
    # - "ai_structured"     (AI structuring of above)
  
  source_classification: enum    # Same as primary_source_type
  
  sources:                       # Array of actual sources
    - title: "Building Standards Code 2023"
      type: "law"                # Type of this source
      version: "2023-04-15"      # Source version
      location: "MLIT/BS-2023"   # Where to find it
      page_reference: "p. 45-47" # Specific location (if applicable)
      accessed_at: "2026-09-20"  # When we accessed it
      confidence_level: enum     # "high" | "medium" | "low"
      notes: "[Optional notes about this source]"
```

### 3.2 Confidence Levels

| Level | Criteria |
|-------|----------|
| high | Current version, official source, directly applicable, no ambiguity |
| medium | Clear but not official, requires interpretation, slightly dated |
| low | Indirect reference, requires extension, significant ambiguity |

### 3.3 Evidence Sufficiency

```yaml
  evidence_sufficiency: enum     # "sufficient" | "insufficient"
  
  evidence_notes: string         # Notes about evidence:
    # - Gaps identified
    # - Assumptions made
    # - Outdated sources
    # - Contradictions resolved
    # - Expert judgment applied
```

**Critical Rule:** Knowledge with `evidence_sufficiency: insufficient` must stay in `draft` status.

---

## 4. Approval Section

### 4.1 Approval Workflow Fields

```yaml
approval:
  # Creation
  created_at: "2026-09-22T10:00:00Z"  # ISO 8601 timestamp
  created_by: "human_name | ai_id"    # Who created this
  
  # Review
  reviewed_at: "2026-09-22T14:00:00Z" # When reviewed (null if not yet)
  reviewed_by: "reviewer_name"         # Who reviewed
  review_findings: string              # Review comments
  
  # Approval
  approved_at: "2026-09-22T16:00:00Z" # When approved (null if not)
  approved_by: "manager_name"          # **Only humans can approve**
  approval_comment: string             # Approval rationale
  approval_authority: string           # Title/role of approver
  
  # Tracking
  last_updated_at: "2026-09-22T10:00:00Z" # Latest change
  last_updated_by: "human_name | ai_id"   # Who changed it
  update_reason: "[Reason for latest change]"
```

### 4.2 Status Transition Rules

**Initial Creation:**
```
New knowledge → status: "draft"
```

**To Review:**
```
When evidence is sufficient:
  draft → status: "review_required"
```

**Review Result:**
```
If approved:    review_required → status: "approved"
If rejected:    review_required → status: "rejected"
If revise:      review_required → status: "draft"
If supersedes:  Any → status: "superseded"
```

**Key Rule:** Only `approved_at` + `approved_by` can move knowledge to `approved`.

---

## 5. Content Section

### 5.1 Title

```yaml
content:
  title: "Foundation Rebar Installation - 木造平屋"
  # 50-100 characters
  # Clear, specific, includes building type
  # Not: "Foundation stuff"
  # Yes: "Foundation Rebar Installation - 木造平屋"
```

### 5.2 Summary

```yaml
  summary: |
    Standard procedure for installing rebar in single-story wooden building 
    foundations, including spacing, fastening, and quality checks.
```

**Requirements:**
- 1-2 sentences
- Complete thought
- Stand-alone readable

### 5.3 Requirements

```yaml
  requirements:
    - "Rebar must be JGAPD Grade 4 or equivalent (tensile strength ≥ 400 MPa)"
    - "Spacing between rebars must not exceed 200mm center-to-center"
    - "Minimum concrete cover: 50mm on bottom, 40mm on sides"
    - "All connections must be mechanically fastened or tied (not loose)"
    - "Pre-installation inspection by site manager required"
```

**Each requirement:**
- Stands alone
- Is measurable/verifiable
- Has source evidence
- Is listed in source section

### 5.4 Checks

```yaml
  checks:
    - "Verify rebar grade marking before installation"
    - "Measure spacing with ruler at 3+ points per section"
    - "Inspect all mechanical connections for tightness"
    - "Check concrete cover with depth gauge before pour"
    - "Document completion with dated photos"
    - "Supervisor sign-off on inspection form"
```

**Each check:**
- Is a verification step
- Can be performed by site personnel
- Is observable/documentable
- References inspection procedure

---

## 6. Validation Rules

### 6.1 Required Fields
All of these must be present and non-empty:
- `metadata.id`
- `metadata.version`
- `metadata.status`
- `content.title`
- `content.summary`
- `source.primary_source_type`
- `source.sources` (non-empty array)
- `approval.created_at`
- `approval.created_by`

### 6.2 Conditional Requirements

**If `status: "draft"`:**
- `evidence_sufficiency` must be "insufficient"

**If `status: "review_required"` or `"approved"`:**
- `evidence_sufficiency` must be "sufficient"
- `source.sources` must have at least one entry
- Each source must have `location` and `accessed_at`

**If `status: "approved"`:**
- `approval.approved_at` must be set
- `approval.approved_by` must be set (human name)
- `approval.approval_authority` must be set (role/title)

**If `status: "rejected"`:**
- `approval.approval_comment` must explain reason
- Knowledge should be moved to `rejected` folder
- Not deleted

### 6.3 Format Validation

| Field | Format | Example |
|-------|--------|---------|
| `id` | `KNW-[Code]-[Phase]-[###]` | `KNW-W01-FND-001` |
| `version` | Semantic versioning | `1.0.0` |
| `at` timestamps | ISO 8601 | `2026-09-22T10:00:00Z` |
| `building_type` | Japanese building classification | `木造平屋` |
| `construction_phase` | Japanese phase name | `基礎` |

---

## 7. File Storage

### 7.1 Master Knowledge Files

```
knowledge/master/KNW-W01-FND-001.yaml
```

**Filename format:** `KNW-{Type}-{Phase}-{Seq}.yaml`

**File content:** Complete YAML knowledge record

### 7.2 Project Override Files

```
knowledge/overrides/{project_id}/KNW-W01-FND-001-override.yaml
```

**Difference:** Overrides have additional fields:

```yaml
override_for_id: "KNW-W01-FND-001"    # ID of master knowledge
project_id: "PROJECT-2026-001"        # Project identifier
project_specific_reason: "Site soil composition requires tighter rebar spacing"
applicable_from: "2026-10-01"
applicable_until: "2027-03-31"
```

### 7.3 Draft Knowledge Files

```
knowledge/drafts/KNW-W01-FND-002.yaml
```

**Requirement:** Must have evidence gap notes.

### 7.4 Audit Log Files

```
knowledge/audit_logs/audit-2026-09.yaml
```

Monthly audit log containing all changes.

---

## 8. Schema Examples

### 8.1 Complete Example (Approved Master Knowledge)

```yaml
metadata:
  id: "KNW-W01-FND-001"
  version: "1.0.0"
  building_type: "木造平屋"
  construction_phase: "基礎"
  construction_task: "基礎配筋"
  knowledge_type: "procedure"
  status: "approved"
  risk_level: "high"
  scope: "master"

content:
  title: "Foundation Rebar Installation - 木造平屋"
  summary: |
    Standard procedure for installing foundation rebar in single-story wooden 
    buildings. Covers rebar grade, spacing, fastening, concrete cover, and 
    quality inspection requirements.
  
  requirements:
    - "Rebar must be JGAPD Grade 4 (tensile strength ≥ 400 MPa)"
    - "Maximum spacing between rebars: 200mm (center-to-center)"
    - "Minimum concrete cover: 50mm (bottom), 40mm (sides)"
    - "All connections must be mechanically fastened or wired (not loose)"
    - "Site manager inspection and sign-off required before pour"
  
  checks:
    - "Verify rebar grade from manufacturer markings"
    - "Measure actual spacing at minimum 3 points per section"
    - "Inspect all mechanical connections visually"
    - "Check concrete cover with depth gauge at 5+ locations"
    - "Document with dated photos from 2+ angles"
    - "Obtain site manager signature on inspection form"

source:
  primary_source_type: "company_standard"
  source_classification: "company_standard"
  sources:
    - title: "Building Standards Code 2023"
      type: "regulation"
      version: "2023-04-15"
      location: "MLIT Building Standards Code"
      page_reference: "Chapter 3, Section 2"
      accessed_at: "2026-09-15"
      confidence_level: "high"
      notes: "Current regulation, directly applicable"
    
    - title: "Company Foundation Standard FND-2023"
      type: "company_standard"
      version: "2023-01-01"
      location: "Internal company document"
      page_reference: "p. 12-15"
      accessed_at: "2026-09-15"
      confidence_level: "high"
      notes: "Updated 2023, applies to all projects"
    
    - title: "Rebar Manufacturer Spec - JGAPD Grade 4"
      type: "manufacturer"
      version: "2026-03"
      location: "Manufacturer technical sheet"
      page_reference: "Section 3"
      accessed_at: "2026-09-15"
      confidence_level: "high"
      notes: "Current specification from approved supplier"
  
  evidence_sufficiency: "sufficient"
  evidence_notes: "Three independent sources confirm requirements. No contradictions identified."

approval:
  created_at: "2026-09-15T09:00:00Z"
  created_by: "site_manager_tanaka"
  
  reviewed_at: "2026-09-18T10:30:00Z"
  reviewed_by: "quality_engineer_yamada"
  review_findings: "Requirements clearly documented and sourced. Checks are observable and measurable."
  
  approved_at: "2026-09-20T14:00:00Z"
  approved_by: "construction_director_suzuki"
  approval_comment: "Approved for company-wide use. Aligns with 2023 standards and internal policy."
  approval_authority: "Director, Construction Operations"
  
  last_updated_at: "2026-09-20T14:00:00Z"
  last_updated_by: "construction_director_suzuki"
  update_reason: "Approved for master knowledge"
```

### 8.2 Draft Example (Insufficient Evidence)

```yaml
metadata:
  id: "KNW-W01-FND-002"
  version: "0.5.0"
  building_type: "木造平屋"
  construction_phase: "基礎"
  construction_task: "基礎型枠"
  knowledge_type: "procedure"
  status: "draft"
  risk_level: "medium"
  scope: "master"

content:
  title: "Foundation Formwork Setup - 木造平屋"
  summary: "Procedures for setting up foundation formwork. Needs additional sourcing."
  
  requirements:
    - "Formwork must be plumb and level"
    - "Bracing must prevent lateral movement"
    - "Joint spacing must allow for seasonal expansion"
  
  checks:
    - "Check level with transit"
    - "Apply horizontal bracing every 1.2m"
    - "Measure gap width at 5+ points"

source:
  primary_source_type: "general_practice"
  source_classification: "general_practice"
  sources:
    - title: "Common construction practice (field knowledge)"
      type: "field_record"
      version: "2026-09"
      location: "Site observations from Project X"
      accessed_at: "2026-09-15"
      confidence_level: "medium"
      notes: "Observed in practice but needs regulatory backing"
  
  evidence_sufficiency: "insufficient"
  evidence_notes: |
    - Missing manufacturer specifications for formwork materials
    - No specific Japanese regulation reference
    - Bracing requirement needs engineer stamp
    - Gap measurement tolerance not sourced
    - Recommend: Get structural engineer review and company standard reference

approval:
  created_at: "2026-09-15T09:00:00Z"
  created_by: "ai_structuring_process"
  
  reviewed_at: null
  reviewed_by: null
  review_findings: null
  
  approved_at: null
  approved_by: null
  approval_comment: null
  approval_authority: null
  
  last_updated_at: "2026-09-15T09:00:00Z"
  last_updated_by: "ai_structuring_process"
  update_reason: "Initial draft from field observations"
```

---

## 9. Validation Checklist

Before knowledge can leave `draft` status:

- [ ] All required metadata fields present and valid
- [ ] Title is clear and specific (50-100 chars)
- [ ] Summary is 1-2 sentences, complete thought
- [ ] Each requirement is measurable and has evidence
- [ ] Each check is observable and verifiable
- [ ] At least 2 sources cited
- [ ] No contradictions between sources
- [ ] All sources have `accessed_at` dates and `location` references
- [ ] Evidence sufficiency marked as "sufficient"
- [ ] Evidence notes explain any gaps or assumptions
- [ ] YAML is valid and parseable
- [ ] File naming follows convention
- [ ] No PII, credentials, or confidential data

---

**END OF KNOWLEDGE-SCHEMA.md**
