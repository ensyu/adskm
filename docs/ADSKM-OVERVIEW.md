# ADSKM System Overview

**Version:** 1.0-MVP  
**Last Updated:** 2026-09-22

---

## What is ADSKM?

ADSKM is **not** a chat application.

ADSKM is an **Evidence-to-Knowledge Pipeline** that:

1. **Captures** site information and construction knowledge
2. **Extracts** relevant facts with source attribution
3. **Structures** knowledge into validated schema
4. **Reviews** independently for correctness
5. **Approves** through human authority
6. **Stores** as company-standard knowledge
7. **Maintains** audit trail of all changes

---

## The Core Problem

Construction companies have:
- ✓ Lots of experience in the field
- ✓ Rich informal knowledge in people's heads
- ✓ Project-specific documents scattered everywhere
- ✓ Industry standards and regulations
- ✗ **No structured, auditable, company-standard knowledge base**

Result:
- Knowledge is lost when experts leave
- Standards are inconsistent across projects
- Mistakes repeat across sites
- Compliance verification is difficult
- New teams have to reinvent procedures

---

## The Solution: ADSKM

A system where:

```
Evidence
  ↓
Structuring (with AI help)
  ↓
Independent Review
  ↓
Security Check
  ↓
Human Approval ← Key: NOT AI
  ↓
Canonical Knowledge (Master)
  ↓
Used by Projects
  ├─ Standard way (Master)
  └─ Exception way (Override, with approval)
```

**Key Principle:** Humans make the final decision. AI helps structure and review, but doesn't approve.

---

## Three Layers of Knowledge

### Layer 1: Master Knowledge
**What it is:** Company-standard procedures and specifications

**Properties:**
- One version of truth
- Approved by management
- Applies to all projects
- Cannot be changed by projects
- Changes require formal review

**Example:**
```
KNW-W01-FND-001: Foundation Rebar Installation
  - Rebar Grade 4 required
  - Spacing: max 200mm
  - Concrete cover: 50mm minimum
  - [Full sourced procedure]
```

### Layer 2: Project Overrides
**What it is:** Project-specific exceptions without changing Master

**Properties:**
- Isolated by project
- Cannot modify Master
- Approved by project authority
- Temporary or permanent
- Fully documented and audited

**Example:**
```
PRJ-2026-001 Override:
  - Site soil requires 150mm spacing (not 200mm)
  - Justification: Geotechnical report
  - Approved by: Project Manager
  - Valid: Oct 2026 - Mar 2027 (rainy season)
```

### Layer 3: Draft Knowledge
**What it is:** Pending knowledge with insufficient evidence

**Properties:**
- Cannot move to Master or use in projects
- Marked with evidence gaps
- Awaiting more sources
- Not lost (preserved for future)
- Tracked in audit log

**Example:**
```
KNW-W01-FND-002: Foundation Formwork (Draft)
  - Evidence gap: Missing engineer spec for bracing
  - Evidence gap: No regulation reference
  - Status: Awaiting structural engineer input
```

---

## The Harness Pipeline

### Stages

**1. Target Selection**
- What knowledge do we need?
- What site information or source documents?

**2. Source Extraction**
- Identify relevant information
- Cite exact source with version/date
- Classify source type (law, regulation, field record, etc.)

**3. Knowledge Structuring**
- Map to ADSKM schema
- Extract requirements
- Define checks/verification
- Identify evidence gaps

**4. Source Audit**
- Verify source is current (not outdated)
- Check for contradictions between sources
- Confirm accessibility of sources
- Assess evidence sufficiency

**5. Independent Review**
- Spec Review: Does it match requirements?
- Implementation Review: Is it technically correct?
- Quality Review: Are requirements verifiable?
- Security Review: Any data/knowledge risks?

**6. Human Approval Gate**
- Manager/Director reviews and decides
- Approves OR Rejects OR Requests Revise
- No automatic approval

**7. Canonical Storage**
- If Approved: Goes to `knowledge/master/`
- If Rejected: Archived with explanation
- If Insufficient Evidence: Stays in `knowledge/drafts/`

---

## Example: Creating Foundation Rebar Knowledge

### Step 1: Source Collection
Site manager identifies current practice:
- Building Standards Code 2023 (regulation)
- Company Foundation Standard (policy)
- Rebar manufacturer spec (technical)

### Step 2: Structuring
AI structures into knowledge record:
```yaml
title: Foundation Rebar Installation
requirements:
  - Grade 4 rebar
  - 200mm max spacing
  - 50mm concrete cover
checks:
  - Verify rebar marking
  - Measure spacing
  - Check concrete cover
```

### Step 3: Source Audit
- ✓ Building Standards Code is current (2023)
- ✓ Company standard is up-to-date
- ✓ Manufacturer spec is for approved supplier
- ✓ No contradictions
- ✓ Evidence sufficient

### Step 4: Independent Review
Engineer reviews:
- ✓ Requirements are clear and measurable
- ✓ All sources are appropriate
- ✓ Checks are verifiable
- ✓ No safety gaps

### Step 5: Human Approval
Director reviews:
- ✓ Aligns with company policy
- ✓ Risk level appropriate
- ✓ Evidence is solid
- Approval: **YES**

### Step 6: Storage
Knowledge stored in `knowledge/master/KNW-W01-FND-001.yaml`

### Step 7: Use
Project teams use this knowledge:
- Standard projects: Use Master directly
- Project with clay soil: Create Override with tighter spacing
- New project: Reference for similar conditions

---

## Knowledge Statuses

```
draft
├─ Insufficient evidence
├─ Pending review
└─ Not usable in projects

review_required
├─ Awaiting independent review
└─ Under assessment

approved ← GOAL
├─ Passed review and human approval
├─ Can be used by projects
└─ Is company standard

rejected
├─ Did not meet standards
├─ Archived with reason
└─ Not usable

superseded
├─ Replaced by newer knowledge
├─ Kept for historical reference
└─ Not usable
```

---

## Security: Four Gates

### Gate 1: Knowledge Poisoning Protection
**Threat:** Bad information becomes standard

**Defense:**
- Evidence requirement (sources, not guesses)
- Source classification (track origin)
- Review before approval

### Gate 2: Evidence Integrity
**Threat:** Sources become invalid, links break

**Defense:**
- Version tracking
- Access date recording
- Source verification
- Audit log

### Gate 3: Approval Contamination
**Threat:** Unapproved knowledge accidentally approved

**Defense:**
- Explicit status transitions
- Human approval only
- Separate draft/approved storage
- Audit trail

### Gate 4: General Data Security
**Threat:** Leakage of confidential information

**Defense:**
- No credentials in knowledge
- No customer PII
- No company secrets
- No external API keys
- Access controls (future)

---

## Audit & Traceability

Every change is recorded:

```
Who changed it?
├─ Human name or AI process

What changed?
├─ Knowledge record
├─ Status transition
└─ Field modifications

When?
├─ Exact timestamp

Why?
├─ Reason for change
├─ Approval justification
└─ Evidence for decision

From/To?
├─ Previous version
└─ New version

Approval?
├─ Who approved
└─ With what authority
```

**Use:** Compliance, forensics, rollback capability (future)

---

## Technology Choices

### Why YAML for Knowledge Storage?
- ✓ Human-readable (can read in text editor)
- ✓ Git-friendly (clear diffs)
- ✓ AI-friendly (easy to parse)
- ✓ Schema-validatable (Pydantic)
- ✓ Structured (not just text)
- ✗ Not a database (by design - simpler for MVP)

### Why Python 3.12?
- ✓ Mature language
- ✓ Strong data validation (Pydantic)
- ✓ Good testing (pytest)
- ✓ AI/ML libraries (future)
- ✓ Cross-platform

### Why No Database Yet?
- MVP scope doesn't need transactions
- YAML + filesystem + audit log is sufficient
- Can add database later if needed
- Simpler to understand and audit

### Why Git for Version Control?
- ✓ Full audit trail
- ✓ Rollback capability
- ✓ Branch support (future)
- ✓ GitHub integration (future)
- ✓ Clear change history

---

## Roles & Responsibilities

### Creator
- Identifies knowledge need
- Gathers sources
- Structures initial knowledge
- Can be human or AI

### Reviewer
- Checks spec/implementation consistency
- Verifies quality
- Identifies evidence gaps
- Does NOT approve

### Approver
- Makes final decision
- Authority-based
- **Human only**
- Responsible for knowledge correctness

### Audit
- Records all changes
- Verifies workflow compliance
- Ensures no shortcuts
- Immutable trail

---

## Not in MVP

These are important but deferred:

- [ ] Web UI/Dashboard
- [ ] Mobile app
- [ ] Database
- [ ] All construction phases
- [ ] All building types
- [ ] Integration with Kanna/Garoon
- [ ] Automatic photo analysis
- [ ] Auto-approval
- [ ] Fully autonomous agents
- [ ] Immutable blockchain ledger
- [ ] Real-time collaboration
- [ ] Multi-language support

**MVP Focus:** Get the core pipeline working reliably for one small domain (木造平屋 Foundation 基礎配筋).

---

## Success Looks Like

A project team needs to set foundation rebar:

1. **Check Master:** Reads KNW-W01-FND-001 (Foundation Rebar)
2. **Check Overrides:** Site has clay soil → Project override exists
3. **Get Requirements:** 150mm spacing (from override), Grade 4 (from master)
4. **Do Work:** Install rebar per spec
5. **Document:** Photos, measurements, sign-off
6. **Audit:** All recorded in knowledge system

**vs. Old Way:**
- "What's our standard for rebar?"
- "I don't know, ask Tanaka"
- "Tanaka retired. Let's ask this new employee"
- "I've never done this before, looks like 200mm somewhere"
- "No wait, I found a memo saying 150mm for clay soil"
- "Is that still valid? When was it written?"
- "No idea. Let me call the old project manager"

---

## Next Steps

1. **SPEC Review** (this document gets reviewed)
2. **SPEC Approval** (human approves direction)
3. **BUILD Session** (implement models, services, validation)
4. **CODE Review** (independent code review)
5. **DEPLOYMENT** (first working system)
6. **First Knowledge** (Create KNW-W01-FND-001)
7. **Test Workflow** (Run full pipeline end-to-end)
8. **Live Usage** (Real projects start using)

---

**END OF ADSKM-OVERVIEW.md**

---

For detailed specs:
- **APP-SPEC.md** - Complete specification
- **KNOWLEDGE-SCHEMA.md** - Knowledge record structure
- **PROJECT-OVERRIDE-SCHEMA.md** - Override system
