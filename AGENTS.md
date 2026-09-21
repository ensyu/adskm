# ADSKM Agent Roles (ADS v4.2)

**Project:** ADSKM (AI Driven Construction Knowledge Management)  
**ADS Version:** 4.2.0 (Adopted official standard)  
**Last Updated:** 2026-09-22

---

## ADS v4.2 Core Principle (ADSKM Adoption)

```
ONE REQUEST.
ONE CONVERSATION.
AUTONOMOUS EXECUTION TO TRIAL-READY.
```

HEAD AGENT orchestrates specification, implementation, review, and security 
using Sub-Agents. **No human gates between technical phases.**

### Stopping Conditions (ADS v4.2 Official)

**Only 2 stop conditions:**

1. **USER_DECISION_REQUIRED**
   - Business decisions AI cannot make
   - ADSKM-specific: Company standard approval, evidence exceptions, high-risk knowledge adoption

2. **EXTERNAL_ACTION_APPROVAL**
   - Operations outside development environment
   - ADSKM-specific: Formal release, production deployment

---

## ADSKM Development Flow (ADS v4.2)

```
User Request
    ↓
HEAD AGENT (Task / Risk Analysis)
    ├─ SPEC Building
    ├─ BUILD Sub-Agent (Implementation)
    ├─ REVIEW Sub-Agents (Independent)
    │  ├─ Review A: Architecture/Spec
    │  ├─ Review B: Implementation/Impact
    │  ├─ Review C: Quality/Operation
    │  ├─ Security Gate: General Security
    │  └─ Knowledge Security Gate: ADSKM-specific
    ├─ SECURITY Sub-Agent (Remediation if needed)
    ├─ FIX Sub-Agent (Address findings)
    └─ Autonomous loop until TRIAL-READY
    ↓
TRIAL-READY
    ↓
USER_DECISION_REQUIRED (Knowledge approval)
    ↓
Human Approval
    ↓
Canonical Knowledge Master
    ↓
EXTERNAL_ACTION_APPROVAL (Release)
    ↓
Production Release
```

---

## Key Differences from Prior Structure

### REMOVED: Phase-by-phase Human Gates
- ❌ "SPEC READY FOR REVIEW" → STOP
- ❌ "SPEC APPROVED" → BUILD
- ❌ "IMPLEMENTATION READY FOR REVIEW" → STOP
- ❌ Multiple review session boundaries

### ADOPTED: ADS v4.2 Autonomous Model
- ✅ Continuous SPEC → BUILD → REVIEW → SECURITY → FIX loop
- ✅ Sub-agents (not separate user sessions)
- ✅ Only 2 stop conditions: USER_DECISION_REQUIRED + EXTERNAL_ACTION_APPROVAL
- ✅ Isolated contexts for independent review (within single conversation)

---

## ADSKM-Specific USER_DECISION_REQUIRED Scenarios

**Technical decisions (AI decides):**
- Schema design
- Implementation approach
- Bug fixes
- Refactoring
- Security fixes

**Business decisions (Humans decide):**
- ✋ Company standard Knowledge approval
- ✋ Promoting general_practice → company_standard
- ✋ Project Override → Master Knowledge reflection
- ✋ Evidence-insufficient Knowledge exceptions
- ✋ HIGH risk Knowledge adoption
- ✋ Major Knowledge conflicts (e.g., conflicting requirements)

---

## Independent Review Structure (ADS v4.2)

**No separate review sessions.** Sub-Agents within HEAD AGENT context:

### Review A: Architecture & Specification
- Validates SPEC completeness
- Checks architecture consistency
- No previous review outputs provided
- Isolated context

### Review B: Implementation & Impact
- Validates code against SPEC
- Checks correctness and completeness
- Receives only code diff (not Review A results)
- Isolated context

### Review C: Quality & Operations
- Validates operational suitability
- Checks maintainability
- Receives only quality criteria (not Reviews A/B)
- Isolated context

### Security Gate: General Security
- Data leakage prevention
- Credential protection
- Trust boundaries
- External API safety

### Knowledge Security Gate: ADSKM-Specific
- **Knowledge Poisoning:** AI cannot unilaterally approve unverified claims
- **Evidence Integrity:** Evidence version tracking and validation
- **Approval Contamination:** AI cannot move knowledge to `approved` status

**Each gate uses isolated context. No prior gate results shared.**

---

## What AI CAN Do (ADS v4.2 Autonomously)

✅ Schema design  
✅ Python implementation  
✅ Unit test creation  
✅ Bug fixes  
✅ Security fixes  
✅ Audit logging  
✅ Sub-Agent orchestration  
✅ Review findings analysis  
✅ FIX execution  
✅ Tier escalation  
✅ Evidence validation  

---

## What AI CANNOT Do (Requires USER_DECISION_REQUIRED)

❌ Approve Knowledge as `company_standard`  
❌ Promote `general_practice` → `company_standard` without human decision  
❌ Move Knowledge to `approved` status  
❌ Accept Evidence-insufficient Knowledge exceptions  
❌ Approve HIGH risk Knowledge  
❌ Override conflicting business requirements  
❌ Release Knowledge to production  

---

## ADSKM Extensions to ADS v4.2 (Not Overrides)

ADSKM adds **project-specific knowledge security requirements** on top of ADS v4.2:

| ADS v4.2 Layer | ADSKM Extension |
|---|---|
| General Security | + Knowledge Poisoning Prevention |
| General Security | + Evidence Integrity Tracking |
| General Security | + Approval Contamination Prevention |
| General Security | + Master/Override Isolation |
| Build/Test/Review | + Knowledge Schema Validation |
| Review | + Knowledge Security Gates |
| USER_DECISION | + Knowledge Approval Authority |

**These are extensions, not replacements of ADS v4.2.**

---

## Model Tier Routing (ADS v4.2)

**Baseline: Tier 1**
- Standard implementation
- Regular schema structuring
- Normal validation

**Escalate to Tier 2 if:**
- Evidence conflicts
- Complex validation
- Security HIGH findings
- Architecture redesign needed

**Escalate to Tier 3 if:**
- Critical knowledge contamination risk
- Trust boundary compromise
- Approval mechanism flaw
- ADS v4.2 core principle violation

---

## Autonomous Self-Repair Loop

**Do NOT stop for:**
- Tier 2/3 escalation
- Critical review findings
- Security issues discovered
- Test failures
- FIX loops
- Multiple revisions

HEAD AGENT orchestrates until TRIAL-READY or USER_DECISION_REQUIRED.

---

## EXTERNAL_ACTION_APPROVAL (ADS v4.2 Official)

These require explicit human approval:

```
Formal release/deployment
External system write
Production data modification
Irreversible operations
Large expense operations
```

ADSKM-specific:
```
Publish Knowledge to production Master
External system integration
Real-world deployment
```

---

## Success Criteria (TRIAL-READY)

At TRIAL-READY, the following must be true:

```
✅ APP-SPEC.md complete and consistent
✅ KNOWLEDGE-SCHEMA.md fully defined
✅ Knowledge security gates verified
✅ All sub-agent reviews PASS
✅ Security gate PASS
✅ No Critical/Major issues
✅ Test coverage 80%+
✅ Code ready for production use
✅ Audit trail complete
✅ Ready for knowledge approval decision
```

---

## Expected User Interactions

1. **Initial Request:** "Build ADSKM system for [scope]"
2. **Autonomous Execution:** HEAD AGENT runs build → review → security → fix loops
3. **Stop 1 (if needed):** "Knowledge approval decision needed for [item]"
   - User: "Approve as company_standard" OR "Keep as reference" OR "Reject"
4. **Resume & Complete:** Continue to TRIAL-READY
5. **Stop 2 (if needed):** "Ready to release to production?"
   - User: "GO" or "Wait"
6. **Result:** TRIAL-READY system delivered

---

**END OF AGENTS.md**

---

**ADS v4.2.0 Compliance:** ✅ Official standard adopted  
**ADSKM Extensions:** ✅ Knowledge security added without overriding ADS  
**Repository Reference:** E:\dev\ai-dev-standard (v4.2.0 tag)