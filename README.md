# ADSKM: AI Driven Construction Knowledge Management

**Status:** Specification Phase  
**Version:** 1.0-MVP  
**Last Updated:** 2026-09-22

---

## Quick Start

### What is ADSKM?

ADSKM is a structured knowledge management system for construction operations. It transforms site information → evidence → knowledge → company standards through human-approved workflows.

**Not a chat app. A knowledge infrastructure.**

---

## Project Structure

```
adskm/
├── APP-SPEC.md              # Main specification (start here)
├── AGENTS.md                # ADS v4.2 agent roles
├── README.md                # This file
├── requirements.txt         # Python dependencies
│
├── docs/
│   ├── ADSKM-OVERVIEW.md    # High-level system overview
│   ├── KNOWLEDGE-SCHEMA.md  # Knowledge record specification
│   └── PROJECT-OVERRIDE-SCHEMA.md  # Override system spec
│
├── src/adskm/               # Main source code (not yet implemented)
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   ├── validation/          # Validation logic
│   ├── security/            # Security checks
│   └── pipeline/            # Main harness
│
├── knowledge/               # Knowledge storage
│   ├── master/              # Company standards
│   ├── overrides/           # Project exceptions
│   ├── drafts/              # Pending knowledge
│   └── audit_logs/          # Change history
│
├── tests/                   # Unit tests (not yet implemented)
└── scripts/                 # Utility scripts (not yet implemented)
```

---

## Current Phase: SPECIFICATION

We are currently in the **SPECIFICATION PHASE**.

### What Has Been Done
- ✅ Repository initialized
- ✅ Directory structure created
- ✅ APP-SPEC.md completed
- ✅ Knowledge schema defined
- ✅ Project override system designed
- ✅ Approval workflow documented
- ✅ Security gates defined

### What's Next
1. **SPEC REVIEW** (Independent review, separate context)
2. **SPEC APPROVAL** (Human approval)
3. **BUILD SESSION** (Implementation begins)
4. **CODE REVIEW** (Independent code review)
5. **TESTING & DEPLOYMENT** (When approved)

---

## Documentation

Start with these (in order):

1. **[APP-SPEC.md](APP-SPEC.md)** - Complete specification (30 min read)
   - System purpose and goals
   - Architecture overview
   - Knowledge schema
   - Approval workflow
   - Security model
   - Development roadmap

2. **[docs/ADSKM-OVERVIEW.md](docs/ADSKM-OVERVIEW.md)** - High-level explanation (10 min read)
   - What is ADSKM?
   - The problem it solves
   - The solution approach
   - Example workflows

3. **[docs/KNOWLEDGE-SCHEMA.md](docs/KNOWLEDGE-SCHEMA.md)** - Detailed schema reference
   - Complete knowledge record structure
   - Field definitions and formats
   - Validation rules
   - Examples
   - File storage locations

4. **[docs/PROJECT-OVERRIDE-SCHEMA.md](docs/PROJECT-OVERRIDE-SCHEMA.md)** - Override system details
   - When to use overrides
   - Override types
   - Isolation rules
   - Approval workflow
   - Examples

5. **[AGENTS.md](AGENTS.md)** - Session and role descriptions
   - Agent responsibilities by session type
   - Context isolation rules
   - Model tier routing
   - Security & approval authority

---

## Key Principles

### Evidence First
No knowledge without documented sources.

```
Claim: "Rebar spacing should be X"
Evidence: ✓ Building code says..., ✓ Our standard says..., ✓ Engineer approves...
Result: Knowledge approved
```

### Human Approval Gate
AI does NOT approve knowledge. Only humans do.

```
AI: "I recommend approval"
Manager: "I approve" ← This is what matters
```

### Master Isolation
Project exceptions don't change company standards.

```
Master: "Standard is 200mm"
Project Override: "This project uses 150mm (soil condition)"
Result: Master unchanged, Project has exception
```

### Audit Trail
Every change is recorded and immutable.

```
Who changed it? When? Why? With what evidence?
=> Recorded in audit_logs/
```

### No Self-Approval
AI can recommend, structure, validate. Only humans approve.

### Separate Sessions
- SPEC in one context
- REVIEW in different context (fresh eyes)
- BUILD in different context (spec-focused)
- CODE REVIEW in different context (no bias)

---

## MVP Scope

### Included
- **Building Type:** 木造平屋 (Single-story wooden building)
- **Construction Phase:** 基礎 (Foundation)
- **Task:** 基礎配筋 (Foundation reinforcement)

Example: `KNW-W01-FND-001` - Foundation Rebar Installation

### Not in MVP (Future)
- All other building types and phases
- Web UI/Dashboard
- Database (using YAML files for now)
- Integration with external systems
- Automatic photo analysis
- Auto-approval workflows

---

## Technology Stack

- **Language:** Python 3.12+
- **Data Format:** YAML (human-readable, git-friendly)
- **Validation:** Pydantic v2
- **Testing:** pytest
- **Version Control:** Git
- **Storage:** Filesystem + Git (no database for MVP)

---

## Development Workflow (ADS v4.2)

1. **SPEC SESSION**
   - Design and document
   - No implementation
   - Output: Specifications

2. **REVIEW SESSION** (Separate context)
   - Independent review
   - No implementation
   - Output: Feedback or approval

3. **BUILD SESSION** (After approval)
   - Implement to spec
   - Write tests
   - Output: Working code

4. **REVIEW SESSION** (Code review, separate context)
   - Independent code review
   - Output: Approval or findings

5. **FIX SESSION** (If needed)
   - Address findings only
   - Return to code review

---

## Next Steps

### For Reviewers
1. Read [APP-SPEC.md](APP-SPEC.md)
2. Review [docs/KNOWLEDGE-SCHEMA.md](docs/KNOWLEDGE-SCHEMA.md)
3. Assess completeness and consistency
4. Note any gaps or concerns

### For Builders (After Approval)
1. Read approved SPEC
2. Implement models in `src/adskm/models/`
3. Implement services in `src/adskm/services/`
4. Write unit tests
5. Validate with pytest

---

## Getting Help

- **Understanding the spec?** Start with [docs/ADSKM-OVERVIEW.md](docs/ADSKM-OVERVIEW.md)
- **Schema questions?** See [docs/KNOWLEDGE-SCHEMA.md](docs/KNOWLEDGE-SCHEMA.md)
- **Override system?** Read [docs/PROJECT-OVERRIDE-SCHEMA.md](docs/PROJECT-OVERRIDE-SCHEMA.md)
- **Agent roles?** Check [AGENTS.md](AGENTS.md)
- **Complete spec?** Full details in [APP-SPEC.md](APP-SPEC.md)

---

## Project Status

```
Current Phase: SPECIFICATION
Status: ✅ SPEC READY FOR REVIEW

Completed:
  ✅ Project setup
  ✅ Git repository initialized
  ✅ Directory structure
  ✅ APP-SPEC.md (main specification)
  ✅ KNOWLEDGE-SCHEMA.md (detailed schema)
  ✅ PROJECT-OVERRIDE-SCHEMA.md (override rules)
  ✅ ADSKM-OVERVIEW.md (high-level overview)
  ✅ AGENTS.md (session roles)

Next:
  → Independent REVIEW session
  → Human approval of SPEC
  → BUILD session (implementation)
```

---

## Questions?

Refer to the documentation:
- **"Why this architecture?"** → APP-SPEC.md, Section 4
- **"What goes in a knowledge record?"** → KNOWLEDGE-SCHEMA.md
- **"How do project overrides work?"** → PROJECT-OVERRIDE-SCHEMA.md
- **"What are agent responsibilities?"** → AGENTS.md

---

**Project:** ADSKM  
**Version:** 1.0-MVP  
**Last Updated:** 2026-09-22  
**Status:** SPECIFICATION READY FOR REVIEW
