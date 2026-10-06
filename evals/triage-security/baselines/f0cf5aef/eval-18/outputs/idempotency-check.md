# Idempotency Check: TC-8001 (Re-Run)

This document analyzes all pre-existing triage artifacts detected on TC-8001
during the second run of triage-security, and records each mutation that was
skipped because the artifact already exists.

## Pre-Existing Artifact Inventory

### 1. Label: `ai-cve-triaged`

- **Detection**: The `ai-cve-triaged` label is present in the issue's Labels field: `CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged`.
- **Skill reference**: Post-Triage Summary, step 1 ("Add the `ai-cve-triaged` label").
- **Action**: SKIP -- label already present. Adding it again would be a no-op in Jira (labels are a set), but the skill detects it and skips the mutation entirely.
- **Implication**: The presence of `ai-cve-triaged` is the primary signal that this issue has already been triaged. Discovery mode (JQL filter `labels NOT IN (ai-cve-triaged)`) would exclude this issue from the untriaged list.

### 2. Status: In Progress

- **Detection**: Issue status is `In Progress`, not `New`.
- **Skill reference**: Step 0.7 ("If the issue is already in Assigned or any later status, skip the transition silently") and the Status-aware handling section ("In Progress / Code Review / QA -- warn the user").
- **Action**: SKIP transition -- the issue is already past `Assigned` status. Step 0.7 skips the transition silently. The status-aware handler warns that the issue is already in `In Progress` and may be actively worked on, but allows proceeding with re-triage if the user confirms.
- **Implication**: No status transition mutation needed.

### 3. Remediation Task Link: Depend -> TC-8100 (upstream backport)

- **Detection**: Issue links include `Depend: TC-8100` with summary "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]", status "In Progress", labels include `ai-generated-jira, Security, CVE-2026-31812`.
- **Skill reference**: Step 8, Case B ("Create remediation tasks for each affected stream") and Remediation Task Creation.
- **Action**: SKIP -- remediation task TC-8100 already exists for the upstream backport in the 2.2.x stream. The Depend link from TC-8001 to TC-8100 already exists. No new task creation or link creation needed.
- **Implication**: Creating a duplicate upstream backport task would violate the skill's idempotency. The existing task is already in progress.

### 4. Remediation Task Link: Depend -> TC-8101 (downstream propagation)

- **Detection**: Issue links include `Depend: TC-8101` with summary "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]", status "Open", labels include `ai-generated-jira, Security, CVE-2026-31812`. TC-8101 also has a Blocks link to TC-8100 (upstream task blocks downstream).
- **Skill reference**: Step 8, Case B and ecosystem classification table (Cargo = source dependency = 2 tasks: upstream backport + downstream propagation, with downstream blocked by upstream).
- **Action**: SKIP -- remediation task TC-8101 already exists for the downstream propagation in the 2.2.x stream. The Depend link from TC-8001 to TC-8101 already exists. The Blocks relationship (TC-8101 blocked by TC-8100) is also already in place. No new task creation, link creation, or blocking relationship needed.
- **Implication**: The full 2-task remediation structure (per the Cargo ecosystem classification) is already complete for the 2.2.x stream.

### 5. Description Digest Comment

- **Detection**: Comment 1 matches the description digest pattern: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6...`. Posted by `sdlc-workflow/triage-security` on 2026-07-01T10:00:00Z.
- **Skill reference**: Remediation Task Creation ("After creating each remediation task, post a description digest comment per `shared/description-digest-protocol.md`"). The digest on the Vulnerability issue itself records that the description was hashed at triage time.
- **Action**: SKIP -- a description digest comment already exists. Posting a second digest would create a duplicate comment. The existing digest hash captures the description state from the first triage run.
- **Implication**: If the description had changed between runs, the digest mismatch would be detectable, but posting a new digest is unnecessary when the existing one is present and the description is unchanged.

### 6. Post-Triage Summary Comment

- **Detection**: Comment 2 is a post-triage summary documenting: version impact (RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected), Affects Versions correction, remediation tasks (TC-8100 upstream backport, TC-8101 downstream propagation), and transition to In Progress. Posted by `sdlc-workflow/triage-security` on 2026-07-01T10:01:00Z. Includes the Comment Footnote.
- **Skill reference**: Post-Triage Summary, step 2 ("Post a summary comment to the original Vulnerability issue").
- **Action**: SKIP -- a post-triage summary comment already exists. Posting a second summary would create a duplicate comment with the same content, adding noise to the issue history.
- **Implication**: The audit trail from the first triage run is already complete.

### 7. Affects Versions

- **Detection**: The issue's Affects Versions are `RHTPA 2.2.0, RHTPA 2.2.1`, which match the version impact analysis (2.2.0 ships quinn-proto 0.11.9, 2.2.1 ships 0.11.12 -- both below the 0.11.14 fix threshold). The issue is scoped to stream 2.2.x, so only 2.2.x versions are in scope.
- **Skill reference**: Step 3 ("Affects Versions Correction").
- **Action**: SKIP -- Affects Versions are already correct. Step 3.2 states: "If Affects Versions are already correct: note this and proceed without changes."
- **Implication**: No Affects Versions mutation needed.

## Summary Table

| Artifact | Expected by Skill | Found on Issue | Mutation Skipped |
|----------|-------------------|----------------|------------------|
| `ai-cve-triaged` label | Post-Triage Summary step 1 | YES | Label addition skipped |
| Status = In Progress | Step 0.7 transition | YES (past Assigned) | Transition skipped |
| Depend link to TC-8100 | Step 8 Case B (upstream backport) | YES | Task creation + link skipped |
| Depend link to TC-8101 | Step 8 Case B (downstream propagation) | YES | Task creation + link skipped |
| TC-8101 Blocks TC-8100 | Step 8 Case B (downstream blocked by upstream) | YES | Blocking link skipped |
| Description digest comment | Remediation Task Creation | YES | Comment skipped |
| Post-triage summary comment | Post-Triage Summary step 2 | YES | Comment skipped |
| Affects Versions = RHTPA 2.2.0, 2.2.1 | Step 3 correction | YES (already correct) | No correction needed |

All 8 triage artifacts from the first run are present and consistent. Zero mutations required on the second run.
