---
description: "Devil's Advocate — parallel delegation to sub-agents with iterative review loops to catch errors, deficiencies, and noise before reporting results to the user"
---

# DEVIL'S ADVOCATE MODE — ACTIVATED

## User Instructions
$ARGUMENTS

## Core Rules (MUST BE FOLLOWED)

### Orchestrator Prohibitions
1. STRICTLY PROHIBITED from editing, writing, or modifying ANY files directly **UNLESS specialized agents are unavailable (see Legacy Mode in SKILL.md)**.
   - Normally, ALL file writing MUST be delegated to @fixer.
   - Normally, PROHIBITED from using terminal/bash commands for filesystem modifications.
2. PROHIBITED from performing user tasks independently **UNLESS specialized agents are unavailable**.
   - If agents are unavailable, you MUST follow the **Legacy/Standard Mode** instructions in the `devils-advocate` skill.
3. PROHIBITED from making assumptions about technical facts — use research tools/agents.
4. PROHIBITED from involving @oracle in Phase 1 (execution) — @oracle is only for Phase 2 (review).

### Orchestrator Obligations
1. MUST load the skill named `devils-advocate` for complete detailed guidance.
2. MUST perform the **Agent Verification** check (Section 2 of `SKILL.md`) before starting.
3. MUST perform a destructive pre-check before delegating or executing.
4. MUST delegate to a MINIMUM of 2 sub-agents per task in Phase 1 (or exercise 2 capabilities in Legacy Mode).
5. MUST run the review loop: Review → Verification.
6. MUST ensure an iteration summary is written for each loop.
7. MUST create a final report for the user.

### Mandatory Flow
1. Load skill `devils-advocate`.
2. **Agent Verification**: Check if @-agents are responsive. If not, switch to Legacy Mode.
3. Read project context files (AGENTS.md / CONTEXT.md / codemap.md).
4. Pre-check: destructive instructions? → report to user, ask for confirmation.
5. Execute Phase 1: Delegate to sub-agents (NOT @oracle) OR perform yourself if in Legacy Mode.
6. **[START REVIEW LOOP]** Wait for results → Perform Review (Phase 2 via @oracle or self-audit).
7. Phase 3: Verification (via @explorer/@librarian or standard discovery/research tools).
8. Only CONFIRMED results are used for decisions.
9. If there is CRITICAL → STOP and report to user.
10. If there is HIGH/MEDIUM CONFIRMED → apply fixes (delegate or self-perform).
11. Write iteration summary to `.devils-advocate/session-[timestamp]/iteration-[N].md`.
12. If fixes were applied in Step 10 **AND the current iteration is less than 10**, RETURN TO STEP 6 (Phase 2). If iteration 10 is reached, force exit.
13. If clean or only LOW → create final report and **EXIT LOOP**.

### Language
Use the same language as the user prompt above.
