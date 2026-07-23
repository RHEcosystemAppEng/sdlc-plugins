# Idempotency Check -- Re-run Analysis for TC-8001

This document analyzes all pre-existing triage artifacts detected on TC-8001
and explains why each artifact causes the corresponding triage step to be
skipped on this second run.

## Summary

TC-8001 has already been fully triaged by a prior invocation of
`sdlc-workflow/triage-security`. All 5 categories of triage artifacts are
present. The re-run detects each one and skips the corresponding mutation.

---

## Artifact 1: `ai-cve-triaged` label

- **Detection**: The issue's Labels field includes `ai-cve-triaged`.
- **Skill step**: Post-Triage Summary (label addition)
- **Action on re-run**: **Skip**. The label is already present; adding it
  again would be a no-op in Jira (duplicate label values are not created),
  but the skill detects it and skips the mutation entirely.
- **Implication**: The issue is already marked as triaged. Discovery mode
  queries (`labels NOT IN (ai-cve-triaged)`) will exclude this issue from
  the untriaged list.

## Artifact 2: Status is In Progress

- **Detection**: The issue's Status field is `In Progress`.
- **Skill step**: Step 0.7 (Assign and Transition to Assigned) and
  Remediation Linkage step 3 (Transition to In Progress)
- **Action on re-run**: **Skip transition**. The status-aware handling in the
  Inputs section detects that the issue is already in `In Progress` status.
  This triggers the warning: "This issue is already in In Progress. It may be
  actively worked on." Since In Progress is a later status than both New and
  Assigned, the transition steps are skipped silently. The assignment (Step
  0.7, item 2) still proceeds to ensure the current user is recorded, but the
  transition itself is not re-executed.

## Artifact 3: Remediation tasks linked via Depend

- **Detection**: The issue's `issuelinks` array contains two entries with
  link type `Depend`:
  - TC-8100 (upstream backport task -- Status: In Progress)
  - TC-8101 (downstream propagation task -- Status: Open, Blocks TC-8100)
- **Skill step**: Step 8 Case A (Remediation Task Creation)
- **Action on re-run**: **Skip task creation**. The existing Depend-linked
  remediation tasks cover the same scope (stream 2.2.x) and the same CVE
  (CVE-2026-31812). Creating new tasks would produce duplicates. The skill
  detects existing remediation tasks and skips creation.
- **Details**:
  - TC-8100 summary matches the upstream backport template pattern:
    "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]"
  - TC-8101 summary matches the downstream propagation template pattern:
    "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]"
  - Both tasks carry labels `ai-generated-jira`, `Security`, `CVE-2026-31812`
    consistent with skill-created remediation tasks.
  - TC-8101 has a Blocks link to TC-8100, matching the expected downstream-
    blocked-by-upstream linkage pattern.

## Artifact 4: Description digest comment

- **Detection**: Comment 1 on the issue is a description digest comment:
  `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6...`
  Posted by `sdlc-workflow/triage-security` on 2026-07-01T10:00:00Z.
- **Skill step**: Post-Triage Summary (description digest posting)
- **Action on re-run**: **Skip**. The description digest comment already
  exists. The skill checks existing comments for a digest comment matching
  the `[sdlc-workflow] Description digest:` pattern before posting a new one.
  Since one is present, no new digest comment is posted.
- **Integrity check**: If the description has changed since the prior run,
  the digest would no longer match. On re-run, the skill could optionally
  recompute the digest and compare, but since no description change is
  detected here, the existing digest is valid.

## Artifact 5: Post-triage summary comment

- **Detection**: Comment 2 on the issue is a post-triage summary comment
  documenting:
  - Version impact: RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected
  - Affects Versions corrected to RHTPA 2.2.0, RHTPA 2.2.1
  - Label `ai-cve-triaged` added
  - Remediation tasks TC-8100 (upstream backport), TC-8101 (downstream propagation)
  - Transitioned to In Progress
  - Signed by `sdlc-workflow/triage-security v0.11.1`
  Posted on 2026-07-01T10:01:00Z.
- **Skill step**: Post-Triage Summary (summary comment posting)
- **Action on re-run**: **Skip**. The summary comment already exists. Posting
  a duplicate summary would create redundant audit trail entries. The skill
  detects the existing summary comment and skips posting.

## Additional Idempotency Observations

### Affects Versions

- **Current state**: RHTPA 2.2.0, RHTPA 2.2.1
- **Expected state** (from version impact analysis): RHTPA 2.2.0, RHTPA 2.2.1
  (versions 2.2.0 and 2.2.1 ship quinn-proto < 0.11.14; versions 2.2.2+
  ship >= 0.11.14)
- **Action on re-run**: **No correction needed**. The Affects Versions are
  already correct from the prior triage run.

### Issue Links (Depend)

- TC-8100 and TC-8101 are already linked with the correct link type (Depend).
- **Action on re-run**: **Skip link creation**. Creating duplicate links
  would fail or produce redundant entries. The skill checks existing
  issuelinks before creating new ones (idempotent link check pattern from
  Steps 4.2 and 4.3).

### Assignee

- **Current assignee**: engineer-a@example.com
- **Action on re-run**: Step 0.7 re-assigns the issue to the current user
  regardless. This is the only mutation that always executes (it is safe and
  idempotent -- assigning the same user is a no-op).
