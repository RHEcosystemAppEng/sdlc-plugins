---
name: triage-security-gate
description: Synthetic native Fullsend execution of the actual triage-security Skill
---

<!-- SYNTHETIC TEST DATA — bypass only production agent's input-before-Skill startup guard -->

Evaluation clock: 2026-09-21T12:00:00Z. Invoke **sdlc-workflow:triage-security**
through the actual **Skill tool** for synthetic issue **TC-8101** as your first
tool call. Do not read or parse trusted input before invoking it. If it cannot
load, expose that failure and stop; do not manually read a Skill file or replace
its execution with expected behavior.

Follow every applicable instruction in the delivered Skill and its companions.
Before its gate instruction, observe only FULLSEND_OUTPUT_DIR presence and value
through a real Bash tool call (never the entire environment or credentials).
Execute each delivered gate/input/final-validation Bash instruction separately,
preserving substituted plugin paths and actual failures. Do not extract commands
from a source file or duplicate them from this fixture. Stop immediately when the
Skill prescribes stopping. Do not mask exits or create a narrated fallback.

For interactive routing, use the synthetic target CLAUDE.md and its existing
missing-Security-Configuration guard. For sandbox routing, use only the actual
mounted trusted input and complete the applicable trusted-evidence analysis.
After successful analysis, write the completed result to the Skill's native
output location and execute its actual inline final JSON/schema validator.
The separate native host validation loop does not substitute for that instruction.

Preserve the Skill's single sandbox result-file contract. Never write local
analysis, logs, receipts, matrices or supplementary sandbox artifacts. Do not
call Jira/GitHub/CVE/WebFetch/lifecycle services, inspect credentials, mutate
anything externally or launch another model CLI. Fullsend retains native runtime
artifacts outside the Skill's output directory; do not fabricate those artifacts.
