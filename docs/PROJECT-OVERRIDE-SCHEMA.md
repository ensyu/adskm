# Project Override Schema Specification

**Version:** 1.0-MVP  
**Last Updated:** 2026-09-22

---

## Overview

Project Overrides allow site-specific exceptions to Master Knowledge without modifying company standards. This document specifies the schema for project-level knowledge overrides.

**Key Principle:** Overrides are **isolated from Master**. Changes to Overrides do NOT automatically update Master Knowledge.

---

## 1. Core Concept

### 1.1 What is an Override?

An Override is a project-specific modification or exception to a Master Knowledge record.

**Examples:**
```
Master Knowledge:
  "Foundation rebar spacing: 200mm maximum"

Project Override Reason:
  "Site soil test shows high clay content
   Requires tighter spacing: 150mm for this project only"

Effect:
  This project uses 150mm spacing
  Master still states 200mm (unchanged)
  Other projects follow Master
```

### 1.2 When to Use Overrides

**Appropriate use:**
- Site-specific conditions (soil, climate, local regulation)
- Project-specific requirements (client request, design change)
- Temporary exceptions (during construction, for safety)
- Pilot testing (new procedures for this project only)

**Inappropriate use (Prohibited):**
- Permanent changes to company standard
- Corrections to Master Knowledge errors
- Cost-cutting measures that reduce quality
- Undocumented changes

---

## 2. Override Record Structure

### 2.1 Complete Override Schema

```yaml
override_metadata:
  id: "OVR-W01-FND-001-PRJ-2026-001"  # Unique override ID
  version: "1.0.0"                    # Override version
  master_knowledge_id: "KNW-W01-FND-001" # ID of master knowledge
  project_id: "PRJ-2026-001"          # Project identifier
  project_name: "Tanaka Office Renovation"
  
content:
  override_type: enum                 # "exception" | "modification" | "addition"
  override_scope: string              # What exactly is overridden
  original_requirement: string        # Quote from Master (for clarity)
  override_requirement: string        # What we're doing instead
  rationale: string                   # Why this override is necessary
  risk_assessment: string             # Safety/quality impact
  mitigation: string                  # How we'll manage the risk
  
timeline:
  applicable_from: date               # When override starts
  applicable_until: date              # When override ends (if temporary)
  permanent: boolean                  # true = indefinite, false = temporary
  
source:
  override_source_type: enum          # "site_condition" | "client_requirement" |
                                       # "local_regulation" | "design_change" |
                                       # "safety_measure" | "pilot_test"
  
  justification_sources:
    - title: "Site Soil Test Report"
      type: "field_record"
      date_issued: "2026-09-10"
      location: "Lab report, Project file"
      confidence_level: "high"
  
  authority_approval: string          # Who approved this override
  approval_date: date                 # When approved
  
approval:
  created_at: timestamp               # Override created
  created_by: "person_name"           # Who created it
  
  reviewed_at: timestamp              # If reviewed
  reviewed_by: string                 # Who reviewed
  review_findings: string             # Review comments
  
  approved_at: timestamp              # When approved by authority
  approved_by: string                 # **Project manager or higher**
  approval_comment: string            # Approval rationale
  approval_authority: string          # Role/title of approver
  
  status: enum                        # "draft" | "review_required" | "approved" |
                                       # "rejected" | "ended"
  
  last_updated_at: timestamp
  last_updated_by: string
  update_reason: string
```

---

## 3. Override Metadata

### 3.1 Naming Convention

Override IDs follow this pattern:
```
OVR-{Building}-{Phase}-{Seq}-PRJ-{ProjectCode}
```

Example:
```
OVR-W01-FND-001-PRJ-2026-001
│   │   │   │   │   │      │
│   │   │   │   │   │      └─ Project sequence
│   │   │   │   │   └────────── Year
│   │   │   │   └──────────────  "PRJ" marker
│   │   │   └─────────────────── Knowledge sequence
│   │   └──────────────────────── Phase (FND = Foundation)
│   └───────────────────────────── Building (W01 = Wood 1)
└────────────────────────────────── OVR (Override)
```

### 3.2 Project Reference

```yaml
override_metadata:
  project_id: "PRJ-2026-001"          # Must reference actual project
  project_name: "Tanaka Office Renovation"  # Project name
  project_location: "Tokyo, Chiyoda Ward"   # Optional: location
```

---

## 4. Override Types

### 4.1 Exception Override
**Type:** `override_type: "exception"`

Temporarily exceeds or reduces a requirement for specific reason.

```yaml
content:
  override_type: "exception"
  override_scope: "Rebar spacing"
  original_requirement: "Maximum 200mm spacing"
  override_requirement: "150mm spacing for this project"
  rationale: "Site soil test shows high clay content, soil engineer recommends tighter spacing"
  risk_assessment: "No negative safety impact; improves structural margin"
  mitigation: "Structural engineer to sign off on final design"
```

### 4.2 Modification Override
**Type:** `override_type: "modification"`

Changes the method but maintains the objective.

```yaml
content:
  override_type: "modification"
  override_scope: "Rebar fastening method"
  original_requirement: "Mechanical fastening or wired connections"
  override_requirement: "Welded connections (site has welding capability)"
  rationale: "Project has skilled welding team; faster and cleaner installation"
  risk_assessment: "Welding quality must match mechanical fastening durability"
  mitigation: "Welding certification required; quality inspection before pour"
```

### 4.3 Addition Override
**Type:** `override_type: "addition"`

Adds new requirement not in Master Knowledge.

```yaml
content:
  override_type: "addition"
  override_scope: "Additional foundation monitoring"
  original_requirement: "Standard pre-pour inspection"
  override_requirement: "Additional weekly inspections during curing (rainy season mitigation)"
  rationale: "Project during rainy season; moisture monitoring needed"
  risk_assessment: "No negative impact; provides early warning of curing issues"
  mitigation: "Assign site technician for weekly readings"
```

---

## 5. Override Source Types

### 5.1 Source Classification

| Source Type | Meaning | Requires | Example |
|---|---|---|---|
| `site_condition` | Specific site characteristics | Site engineer analysis | "Soil test shows 30% clay" |
| `client_requirement` | Client-requested change | Client approval | "Client wants tighter specs" |
| `local_regulation` | Regional/local requirement | Regulatory authority | "Tokyo ordinance requires..." |
| `design_change` | Project design modification | Design engineer | "Structure redesigned" |
| `safety_measure` | Safety-driven override | Safety officer | "Weather conditions require..." |
| `pilot_test` | Testing new procedure | Project manager | "Pilot test new fastening" |

### 5.2 Justification Sources

Each override must cite sources justifying the override:

```yaml
source:
  override_source_type: "site_condition"
  
  justification_sources:
    - title: "Geotechnical Site Investigation Report"
      type: "design_document"
      date_issued: "2026-08-15"
      location: "Project file / Engineer's office"
      page_reference: "p. 23"
      confidence_level: "high"
    
    - title: "Structural Engineer's Recommendation"
      type: "design_document"
      date_issued: "2026-09-10"
      location: "Email from SE, Project file"
      confidence_level: "high"
```

---

## 6. Timeline Management

### 6.1 Permanent vs. Temporary

**Permanent Override:**
```yaml
timeline:
  applicable_from: "2026-10-01"
  applicable_until: null           # Never ends
  permanent: true
```

Used when override will remain in effect for the life of the project.

**Temporary Override:**
```yaml
timeline:
  applicable_from: "2026-10-01"
  applicable_until: "2027-03-31"   # Ends after rainy season
  permanent: false
```

Used when override expires after a certain date or condition.

### 6.2 Sunset Clause

For temporary overrides, document what happens when it expires:

```yaml
content:
  mitigation: |
    This override is valid until 2027-03-31 (end of rainy season).
    After that date, standard Master rebar spacing (200mm) resumes.
    On 2027-03-15, project team will assess if extension is needed.
```

---

## 7. Approval Workflow

### 7.1 Override Approval Levels

| Approval Required | Authority | Signature Role |
|---|---|---|
| Risk: low | Project Manager | PM or above |
| Risk: medium | Site Manager + PM | Both required |
| Risk: high | Site Manager + Safety Officer + PM | All required |
| Risk: critical | Director approval required | Director/VP |

### 7.2 Approval Flow

```
1. Override Created (draft)
   ↓
2. Evidence Gathering
   ↓
3. Risk Assessment
   ↓
4. Submit for Review (review_required)
   ↓
5. Reviewer Assessment
   ├─ Approved → status: approved
   ├─ Rejected → status: rejected + explanation
   └─ Revise → status: draft + findings
   ↓
6. Execution (if approved)
   ↓
7. Monitoring & Documentation
   ↓
8. Closure (if temporary) OR Continuation (if permanent)
```

### 7.3 No Self-Approval

**Rule:** AI cannot approve overrides. Only humans can.

Status transitions to `approved` require explicit `approved_by` field with human identifier.

---

## 8. Isolation Rules

### 8.1 Override Does NOT Modify Master

**Prohibited:**
```yaml
# WRONG - This violates isolation:
# Modifying Master Knowledge from Override
knowledge/master/KNW-W01-FND-001.yaml
  requirements:
    - "Rebar spacing: 150mm (because of Project PRJ-2026-001)"  # NO!
```

**Correct:**
```yaml
# RIGHT - Override is separate
knowledge/overrides/PRJ-2026-001/OVR-W01-FND-001-PRJ-2026-001.yaml
  content:
    override_requirement: "Rebar spacing: 150mm for this project"

# Master unchanged:
knowledge/master/KNW-W01-FND-001.yaml
  requirements:
    - "Rebar spacing: 200mm"  # Still the standard
```

### 8.2 Override Storage Location

```
knowledge/overrides/
├─ PRJ-2026-001/
│  ├─ OVR-W01-FND-001-PRJ-2026-001.yaml
│  ├─ OVR-W01-FND-002-PRJ-2026-001.yaml
│  └─ ...
├─ PRJ-2026-002/
│  ├─ OVR-W01-FND-001-PRJ-2026-002.yaml
│  └─ ...
└─ ...
```

**Rule:** All overrides for a project go in `PRJ-XXXX/` folder.

### 8.3 Master Knowledge Immutability (Project Level)

When using Master Knowledge in a project context:

```python
# Pseudocode
master_knowledge = load_master("KNW-W01-FND-001")

# Check for overrides
overrides = load_overrides(project_id="PRJ-2026-001")
override = find_override_for(master_knowledge, overrides)

if override:
    # Use override for this project
    effective_knowledge = merge(master_knowledge, override)
else:
    # Use master as-is
    effective_knowledge = master_knowledge

# Master itself is NEVER modified
# Only in-memory merge for this project
```

---

## 9. Master vs. Override Merge Rules

### 9.1 Merge Logic

When a project needs knowledge, the system applies this logic:

```
1. Load Master Knowledge (KNW-W01-FND-001)
2. Check for Project Override (OVR-W01-FND-001-PRJ-2026-001)
3. If override exists AND is approved AND is in timeline:
     Return: Master + Override (Override values override Master)
4. Else:
     Return: Master only
5. Never modify Master file on disk
```

### 9.2 Override Field Precedence

**Example: Override adds additional requirement**

```yaml
# Master Knowledge
requirements:
  - "Rebar spacing ≤ 200mm"
  - "Concrete cover ≥ 50mm"

# Project Override
additional_requirements:
  - "Weekly settlement monitoring during rainy season"

# Effective for Project:
requirements:
  - "Rebar spacing ≤ 150mm"        # from override
  - "Concrete cover ≥ 50mm"        # from master (not overridden)
  - "Weekly settlement monitoring" # from override addition
```

---

## 10. Documentation & Audit

### 10.1 Override Documentation

Every override must have:
- [ ] Clear rationale explaining why
- [ ] Evidence sources justifying the change
- [ ] Risk assessment and mitigation
- [ ] Approved by appropriate authority
- [ ] Timeline (when it applies)
- [ ] Monitoring plan (how we'll track it)
- [ ] Closure plan (how it ends or continues)

### 10.2 Audit Trail

Override changes are logged:

```yaml
audit_entry:
  timestamp: "2026-09-20T14:30:00Z"
  override_id: "OVR-W01-FND-001-PRJ-2026-001"
  action: "created | updated | approved | rejected | ended"
  who: "project_manager_name"
  change: "Status changed from draft to approved"
  reason: "Risk assessment complete, structural engineer sign-off obtained"
```

### 10.3 Monitoring During Execution

While override is active:
- [ ] Regular compliance checks
- [ ] Documentation of actual performance
- [ ] Issue logging if problems occur
- [ ] Photos/evidence collection
- [ ] Sign-off by responsible personnel

---

## 11. Override Lifecycle

### 11.1 Complete Lifecycle

```
Phase 1: Creation
├─ Identify need for override
├─ Create override record in draft
├─ Gather evidence and justification
└─ Mark as review_required

Phase 2: Review & Approval
├─ Risk assessment
├─ Engineering/safety review
├─ Authority approval
└─ Mark as approved

Phase 3: Execution
├─ Communicate to site team
├─ Monitor compliance
├─ Document performance
└─ Collect photographic evidence

Phase 4: Closure
├─ If temporary: Set end date and evaluate
├─ If permanent: Continue until project end
├─ Final documentation
└─ Mark as closed (status: ended)
```

### 11.2 Status Transitions

```
draft
  ├─ [Evidence sufficient] ──→ review_required
  └─ [Rejected in review] ──→ rejected

review_required
  ├─ [Approved] ──────→ approved
  ├─ [Rejected] ──────→ rejected
  └─ [Revise needed] ──→ draft

approved
  ├─ [During execution] ──→ active
  └─ [End date reached] ──→ ended

rejected
  └─ [Mark as closed]
```

---

## 12. Override Examples

### 12.1 Example 1: Soil-Based Tighter Spacing

```yaml
override_metadata:
  id: "OVR-W01-FND-001-PRJ-2026-001"
  master_knowledge_id: "KNW-W01-FND-001"
  project_id: "PRJ-2026-001"
  project_name: "Tanaka Office Renovation"
  version: "1.0.0"

content:
  override_type: "exception"
  override_scope: "Rebar spacing in foundation"
  original_requirement: "Rebar spacing: maximum 200mm center-to-center"
  override_requirement: "Rebar spacing: maximum 150mm center-to-center"
  rationale: |
    Geotechnical survey identified high clay content (>30%) in site soil.
    Structural engineer recommends tighter rebar spacing to handle 
    differential settlement risk.
  risk_assessment: "Low risk - improved structural capacity"
  mitigation: "Structural engineer to certify final rebar layout"

timeline:
  applicable_from: "2026-10-01"
  applicable_until: null
  permanent: true

source:
  override_source_type: "site_condition"
  justification_sources:
    - title: "Geotechnical Investigation Report"
      type: "design_document"
      date_issued: "2026-08-15"
      location: "Project file"
      confidence_level: "high"
    - title: "Structural Engineer Recommendation"
      type: "design_document"
      date_issued: "2026-09-10"
      location: "Email + Signed letter"
      confidence_level: "high"

approval:
  created_at: "2026-09-15T10:00:00Z"
  created_by: "site_manager_tanaka"
  reviewed_at: "2026-09-18T14:00:00Z"
  reviewed_by: "project_manager_yamada"
  review_findings: "Justification solid. SE signature obtained."
  approved_at: "2026-09-20T09:00:00Z"
  approved_by: "construction_director_suzuki"
  approval_comment: "Approved. Structural safety rationale is sound."
  approval_authority: "Director, Construction Operations"
  status: "approved"
```

### 12.2 Example 2: Temporary Rainy Season Override

```yaml
override_metadata:
  id: "OVR-W01-FND-002-PRJ-2026-001"
  master_knowledge_id: "KNW-W01-FND-003"  # Curing procedure
  project_id: "PRJ-2026-001"
  project_name: "Tanaka Office Renovation"
  version: "1.0.0"

content:
  override_type: "addition"
  override_scope: "Foundation curing during rainy season"
  original_requirement: "Standard curing: 7-day water spray, 7-day drying"
  override_requirement: |
    Rainy season curing (Oct 1 - Mar 31):
    - Protect concrete from direct rain
    - Moisture monitoring: daily for first 14 days
    - Extend curing to 10 days if moisture >80%
  rationale: "Project timing coincides with rainy season; moisture management critical"
  risk_assessment: "Medium - affects strength development if not managed"
  mitigation: |
    - Protective covering installed before rain
    - Daily moisture readings with calibrated meter
    - Structural engineer approves early form removal

timeline:
  applicable_from: "2026-10-01"
  applicable_until: "2027-03-31"
  permanent: false

source:
  override_source_type: "site_condition"
  justification_sources:
    - title: "Tokyo Weather Forecast & Historical Data"
      type: "field_record"
      date_issued: "2026-09-20"
      confidence_level: "high"
    - title: "Concrete Curing in Wet Weather - Technical Guide"
      type: "general_practice"
      date_issued: "2024-01-01"
      confidence_level: "medium"

approval:
  created_at: "2026-09-20T09:00:00Z"
  created_by: "site_manager_tanaka"
  approved_at: "2026-09-22T10:00:00Z"
  approved_by: "project_manager_yamada"
  approval_comment: "Approved for rainy season (Oct-Mar). Review again in April."
  approval_authority: "Project Manager"
  status: "approved"
```

---

## 13. Validation Checklist

Before override approval:

- [ ] Master knowledge ID is valid and exists
- [ ] Project ID is valid
- [ ] Override type is clearly stated
- [ ] Original requirement quoted directly from Master
- [ ] Rationale is specific and documented
- [ ] Risk assessment is realistic
- [ ] Mitigation plan is actionable
- [ ] Sources justify the override need
- [ ] Timeline is clear (applicable dates)
- [ ] Approval authority is appropriate for risk level
- [ ] No attempt to modify Master Knowledge
- [ ] Override stored in correct project folder
- [ ] Audit trail will be maintained
- [ ] No PII or confidential data

---

**END OF PROJECT-OVERRIDE-SCHEMA.md**
