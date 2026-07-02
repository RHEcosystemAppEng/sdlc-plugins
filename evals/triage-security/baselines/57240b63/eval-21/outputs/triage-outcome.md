# Triage Outcome for TC-8020 (CVE-2026-31812)

## Summary

CVE-2026-31812 affects the **quinn-proto** crate (versions before 0.11.14) -- a denial-of-service vulnerability allowing remote panic via excessive QUIC stream creation. The issue is scoped to stream **2.2.x** per the summary suffix `[rhtpa-2.2]`.

## Version Impact Summary

### Stream 2.2.x (in scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

### Stream 2.1.x (cross-stream, out of scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |

## Triage Decision

**Case A + Case B apply**: The issue's scoped stream (2.2.x) has affected versions (2.2.0, 2.2.1, 2.2.2), and cross-stream impact exists in 2.1.x.

**However, Step 7 (Concurrent Triage Detection) blocks remediation task creation.**

TC-8019 is currently "In Progress" with assignee engineer-b@example.com, triaging a different CVE that also affects `quinn-proto`. The engineer must choose one of three options before remediation proceeds:

1. **Wait** -- Pause until TC-8019 completes, then re-run from Step 4.3
2. **Skip** -- Defer task creation; post a skip comment on TC-8020
3. **Proceed** -- Create tasks with `concurrent-triage-overlap` label for deduplication

## Proposed Jira Mutations (all require engineer confirmation)

All of the following are PROPOSALS pending engineer approval. No Jira mutations are executed without explicit confirmation.

### Already Actionable (independent of Step 7 choice)

1. **Assign and transition (Step 0.7):**
   - PROPOSAL: Assign TC-8020 to current user
   - PROPOSAL: Transition TC-8020 from "New" to "Assigned"

2. **Affects Versions correction (Step 3):**
   - PROPOSAL: Change Affects Versions from `[RHTPA 2.0.0]` to `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Rationale: RHTPA 2.0.0 does not exist in any configured Version Stream. Lock file evidence confirms versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto (< 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version and are excluded.
   - PROPOSAL: Post comment documenting the correction (scoped to stream 2.2.x per issue suffix)

3. **Add ai-cve-triaged label (Post-Triage):**
   - PROPOSAL: Add `ai-cve-triaged` label to TC-8020

### Contingent on Step 7 Decision

#### If engineer chooses "Wait":
- Stop execution. No remediation tasks created. Engineer re-runs triage after TC-8019 completes.

#### If engineer chooses "Skip":
- PROPOSAL: Post comment on TC-8020 explaining task creation was skipped due to concurrent triage on quinn-proto (TC-8019 In Progress)
- No remediation tasks created.

#### If engineer chooses "Proceed":

4. **Add concurrent-triage-overlap label:**
   - PROPOSAL: Add `concurrent-triage-overlap` label to TC-8020

5. **Case A -- Remediation tasks for stream 2.2.x (in scope):**
   - PROPOSAL: Create upstream backport Task:
     - Summary: "Bump quinn-proto to >= 0.11.14 in rhtpa-backend (release/0.4.z) [CVE-2026-31812]"
     - Labels: `CVE-2026-31812`, `security-fix`, `concurrent-triage-overlap`
     - Ecosystem: Cargo
     - Repository: rhtpa-backend
     - Branch: release/0.4.z
     - Target: Update quinn-proto from 0.11.12 to >= 0.11.14 in Cargo.lock
     - Link: "Depend" to TC-8020
   - PROPOSAL: Create downstream propagation subtask:
     - Summary: "Propagate quinn-proto fix to rhtpa-release.0.4.z [CVE-2026-31812]"
     - Labels: `CVE-2026-31812`, `security-fix`, `concurrent-triage-overlap`
     - Blocked by: upstream backport task
     - Link: "Depend" to TC-8020

6. **Case B -- Cross-stream impact notice:**
   - PROPOSAL: Post comment on TC-8020:
     ```
     Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
     based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship
     quinn-proto 0.11.9.
     These streams are tracked by companion issues (see Related links)
     or may require separate PSIRT triage.
     ```
   - Check for existing CVE sibling Jiras for 2.1.x stream with label CVE-2026-31812
   - If no sibling exists for 2.1.x: create preemptive remediation tasks with `security-preemptive` label and "Related" link to TC-8020
   - If a sibling exists: skip preemptive task creation for that stream

7. **Post-triage summary comment:**
   - PROPOSAL: Post summary comment on TC-8020 including:
     - Version impact table
     - Affects Versions correction details
     - Triage outcome and remediation task links
     - @mention of the issue reporter (PSIRT analyst)
     - Comment Footnote per shared/comment-footnote.md

## Key Observations

1. **PSIRT Affects Versions was incorrect**: RHTPA 2.0.0 does not correspond to any configured stream. The correct affected versions in the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2.

2. **Fix already present in latest releases**: Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fix version). The vulnerability was remediated starting from build v0.4.11.

3. **Concurrent triage is the critical gate**: TC-8019 is actively being triaged by another engineer on the same upstream component (quinn-proto). This is the primary blocker for remediation task creation and the reason the triage cannot proceed to completion without engineer input.

4. **Cross-stream impact exists**: Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9), but this issue is scoped to 2.2.x. Cross-stream impact will be handled via Case B (comment + potential preemptive tasks).
