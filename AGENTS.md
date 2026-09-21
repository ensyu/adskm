# ADSKM Agent Roles (ADS v4.2)

**Project:** ADSKM (AI Driven Construction Knowledge Management)  
**ADS Version:** 4.2  
**Last Updated:** 2026-09-22

---

## Session Types & Agent Roles

### SPEC SESSION (Current)
**Purpose:** Define requirements, architecture, and specifications  
**Duration:** Single focused session  
**Outputs:** APP-SPEC.md, schema documents  
**Ends At:** "SPEC READY FOR REVIEW"  
**Next:** Separate REVIEW session

**Agent Role:** Architect/Spec Writer
- Gather requirements
- Design system architecture
- Define schemas
- Document specifications
- NO implementation
- NO code writing
- NO approval authority

---

### REVIEW SESSION (Separate Context)
**Purpose:** Independent review of specifications  
**Duration:** Single focused session  
**Inputs:** SPEC documents only  
**Outputs:** Review findings, approval/revision decision  
**Key:** Different AI instance, fresh context

**Agent Role:** Independent Reviewer
- Review A: Specification completeness and consistency
- Review B: Implementation feasibility
- Review C: Security and knowledge security
- Identify gaps and issues
- Document findings
- NO implementation
- NO approval authority (recommends to human)

---

### BUILD SESSION (After SPEC Approval)
**Purpose:** Implement to specification  
**Duration:** Focused implementation session  
**Inputs:** Approved SPEC  
**Outputs:** Working code, unit tests  
**Ends At:** "IMPLEMENTATION READY FOR REVIEW"

**Agent Role:** Developer/Implementer
- Follow SPEC exactly
- Write models, services, validation
- Write unit tests
- Document code changes
- Run validation (pytest, git diff --check)
- NO spec changes
- NO architectural decisions
- NO approval

---

### CODE REVIEW SESSION (Separate Context)
**Purpose:** Independent review of implementation  
**Duration:** Focused review session  
**Inputs:** Code diff only  
**Outputs:** Findings, approval/revision decision

**Agent Role:** Code Reviewer
- Check correctness
- Verify spec compliance
- Test quality
- Security checks
- Performance considerations
- NO architectural changes
- NO approval authority

---

### FIX SESSION (If Needed)
**Purpose:** Address review findings  
**Duration:** Short focused session  
**Inputs:** Review findings  
**Outputs:** Fixed code

**Agent Role:** Fixer
- Address ONLY review findings
- No scope expansion
- No new features
- No refactoring beyond findings
- Return to REVIEW

---

## Agent Responsibilities by Session

### SPEC Session - DO THIS
- [ ] Read developer instructions
- [ ] Understand project goals
- [ ] Define knowledge schema
- [ ] Define source classification
- [ ] Define approval workflow
- [ ] Design system architecture
- [ ] Document specifications
- [ ] Create example schemas
- [ ] Validate spec completeness
- [ ] Stop at "SPEC READY FOR REVIEW"

### SPEC Session - DON'T DO THIS
- [ ] Write code
- [ ] Create database
- [ ] Set up web server
- [ ] Create GUI
- [ ] Approve specifications
- [ ] Make implementation decisions
- [ ] Assume future requirements
- [ ] Over-design

---

### REVIEW Session - DO THIS
- [ ] Read SPEC only (not previous sessions)
- [ ] Review A: Specification consistency
- [ ] Review B: Completeness check
- [ ] Review C: Technical feasibility
- [ ] Check for gaps
- [ ] Identify risks
- [ ] Document findings
- [ ] Recommend approval or revision

### REVIEW Session - DON'T DO THIS
- [ ] Reference previous sessions
- [ ] Implement fixes
- [ ] Approve specifications
- [ ] Make architectural changes
- [ ] Consider implementation details
- [ ] Assume what builder will do

---

### BUILD Session - DO THIS
- [ ] Read approved SPEC
- [ ] Implement to specification
- [ ] Write model classes
- [ ] Write service methods
- [ ] Write validation logic
- [ ] Write unit tests
- [ ] Test with pytest
- [ ] Document changes
- [ ] Stop at "IMPLEMENTATION READY FOR REVIEW"

### BUILD Session - DON'T DO THIS
- [ ] Change SPEC
- [ ] Make architectural decisions
- [ ] Add features beyond SPEC
- [ ] Add GUI
- [ ] Add API server
- [ ] Make assumptions about review
- [ ] Approve own work

---

## Context Isolation Rules

### Critical: NO Context Bleeding

**SPEC Session:**
- Does NOT read BUILD session messages
- Does NOT know implementation details
- Designs in isolation

**REVIEW (Spec) Session:**
- Does NOT read previous SPEC session messages
- Does NOT read BUILD session messages
- Reviews from fresh context
- Gets only SPEC documents

**BUILD Session:**
- Does NOT read SPEC session messages (except final SPEC)
- Gets approved SPEC + instructions only
- Implements from clear requirements
- No biasing context

**REVIEW (Code) Session:**
- Does NOT read SPEC messages
- Does NOT read BUILD messages
- Gets only code diff
- Reviews from clean context

---

## Model Tier Routing (ADS v4.2)

### Baseline: Tier 1
- Standard knowledge structuring
- Regular validation
- Normal review processes
- **Model:** Claude 3.5 Sonnet or equivalent

### Escalate to Tier 2 If:
- Knowledge schema conflicts
- Evidence contradictions
- Security HIGH assessment
- Complex validation rules
- **Model:** Claude Opus 5 or equivalent

### Escalate to Tier 3 If:
- Knowledge security critical
- Trust boundary design
- Approval workflow architecture
- Fallback decision logic
- **Model:** Claude Opus Max or specialized

---

## Security & Approvals

### What AI CAN Do
- ✓ Suggest knowledge structures
- ✓ Extract and format information
- ✓ Identify evidence gaps
- ✓ Flag contradictions
- ✓ Recommend PASS/REVISE
- ✓ Write validation code
- ✓ Run tests
- ✓ Record audit logs

### What AI CANNOT Do
- ✗ Approve knowledge (humans only)
- ✗ Bypass security gates
- ✗ Modify source files outside gate
- ✗ Self-approve code
- ✗ Promote general_practice to company_standard unilaterally
- ✗ Remove audit entries
- ✗ Modify approval signatures
- ✗ Override human decisions

---

## Communication Protocol

### Between Humans & AI

**Developer → AI:**
```
"Implement the approved SPEC. Follow the requirements exactly.
Stop at 'IMPLEMENTATION READY FOR REVIEW'."
```

**AI → Human (after SPEC):**
```
"SPEC is complete and ready for review.
Output: APP-SPEC.md, KNOWLEDGE-SCHEMA.md, PROJECT-OVERRIDE-SCHEMA.md
Status: SPEC READY FOR REVIEW
Next: Independent review session"
```

**Human → AI (after REVIEW):**
```
"SPEC approved. Proceed with BUILD session."
```

**AI → Human (after BUILD):**
```
"Implementation complete and tested.
Tests: NN% coverage, all passing
Status: IMPLEMENTATION READY FOR REVIEW
Next: Code review session"
```

---

## Handoff Between Sessions

Each session ends with brief handoff:

```yaml
handoff:
  project: ADSKM
  session_type: SPEC
  status: READY FOR REVIEW
  outputs:
    - APP-SPEC.md
    - docs/KNOWLEDGE-SCHEMA.md
    - docs/PROJECT-OVERRIDE-SCHEMA.md
    - docs/ADSKM-OVERVIEW.md
  key_decisions:
    - YAML for knowledge storage
    - Pydantic for validation
    - No database for MVP
  unresolved:
    - []
  next_action: "Independent review of specifications"
```

Next session reads handoff and uses it as context anchor.

---

## ADS v4.2 Compliance Checklist

- [ ] Session separation (SPEC → REVIEW → BUILD → REVIEW → FIX)
- [ ] Context isolation (each session fresh context)
- [ ] Risk classification (knowledge security = HIGH)
- [ ] Independent review (separate reviewer context)
- [ ] Security gates (multiple checkpoints)
- [ ] Human gates (no AI approval)
- [ ] Model tier routing (mostly Tier 1, escalate if needed)
- [ ] Human decision final (AI recommends, human decides)
- [ ] Audit trail (all changes logged)
- [ ] No self-approval (AI cannot approve own work)

---

**END OF AGENTS.md**

---

For ADS v4.2 details, refer to official ADS documentation.
