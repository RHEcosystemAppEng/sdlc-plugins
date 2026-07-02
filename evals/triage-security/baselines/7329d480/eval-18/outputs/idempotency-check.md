# Idempotency Check: TC-8001 (Re-Run Detection)

This document records all pre-existing triage artifacts detected on TC-8001
during a second invocation of `triage-security`. Each artifact is evidence
that the prior triage run already completed the corresponding step, and
therefore that step's mutations must be skipped.

## Summary

All 6 triage artifact categories are present. The issue has been fully triaged
in a prior run. **No new mutations are required.**

---

## Artifact 1: `ai-cve-triaged` Label

- **Detected**: Yes
- **Source**: Issue labels field contains `ai-cve-triaged`
- **Significance**: This label is added in the Post-Triage Summary phase
  (after Step 8) to mark the issue as fully triaged. Its presence means the
  entire triage workflow completed successfully in the prior run.
- **Action**: Skip adding the label (already present). This also signals to
  discovery mode that this issue should not appear in the "untriaged" list.

## Artifact 2: Issue Status -- In Progress

- **Detected**: Yes
- **Current status**: In Progress
- **Significance**: Step 0.7 transitions the issue from New to Assigned, and
  the post-triage flow transitions it further. The issue is already past
  the New/Assigned states, indicating that prior triage advanced the status.
  Per the status-aware handling rules, an issue in In Progress triggers a
  warning: "This issue is already in In Progress. It may be actively worked
  on."
- **Action**: Skip the Step 0.7 transition (issue is already beyond Assigned).
  The assignment update (Step 0.7, substep 2) may still proceed to record the
  current user, but no status transition is needed.

## Artifact 3: Remediation Task TC-8100 (Upstream Backport)

- **Detected**: Yes
- **Link type**: Depend (outward from TC-8001)
- **Summary**: Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]
- **Status**: In Progress
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Significance**: This is the upstream backport remediation task created by
  Step 8 (Case A) for the Cargo ecosystem. Its existence (linked via Depend)
  means the prior triage already created and linked the upstream remediation task.
- **Action**: Skip creating an upstream backport task. The task already exists
  and is actively being worked on (In Progress).

## Artifact 4: Remediation Task TC-8101 (Downstream Propagation)

- **Detected**: Yes
- **Link type**: Depend (outward from TC-8001)
- **Summary**: Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]
- **Status**: Open
- **Labels**: ai-generated-jira, Security, CVE-2026-31812
- **Blocks**: TC-8100
- **Significance**: This is the downstream propagation subtask created by Step 8
  (Case A) for the Cargo ecosystem. It is blocked by TC-8100 (the upstream
  backport task), which matches the expected remediation structure: upstream
  fix first, then downstream propagation. Its existence means the prior triage
  already created both remediation tasks for the 2.2.x stream.
- **Action**: Skip creating a downstream propagation task. The task already exists
  with proper blocking relationship to TC-8100.

## Artifact 5: Description Digest Comment

- **Detected**: Yes
- **Comment text**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
- **Posted by**: sdlc-workflow/triage-security
- **Posted at**: 2026-07-01T10:00:00Z
- **Significance**: The description digest comment is posted per
  `shared/description-digest-protocol.md` to record the hash of the issue
  description at triage time. Its presence means Step 1 already captured
  and recorded the description state. If the description has not changed
  since the prior run (same digest), there is no new data to extract.
- **Action**: Skip posting a new description digest comment. If the description
  content has changed (different hash), a new digest would normally be posted,
  but no other triage artifacts need re-creation.

## Artifact 6: Post-Triage Summary Comment

- **Detected**: Yes
- **Content summary**: Documents triage completion for CVE-2026-31812 including:
  - Version impact: RHTPA 2.2.0 and 2.2.1 affected, RHTPA 2.2.2+ not affected
  - Affects Versions corrected to RHTPA 2.2.0, RHTPA 2.2.1
  - Label `ai-cve-triaged` added
  - Remediation tasks created: TC-8100 (upstream backport), TC-8101 (downstream propagation)
  - Transitioned to In Progress
- **Posted by**: sdlc-workflow/triage-security
- **Posted at**: 2026-07-01T10:01:00Z
- **Significance**: The post-triage summary comment is the final action in the
  triage workflow. Its presence is definitive proof that the prior triage run
  completed all steps successfully, including Affects Versions correction,
  remediation task creation, status transition, and label application.
- **Action**: Skip posting a new post-triage summary. Posting a duplicate
  summary would create noise in the issue's comment history.

---

## Affects Versions Consistency Check

- **Current Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1
- **Expected from version impact analysis**: RHTPA 2.2.0 and RHTPA 2.2.1 are
  affected (quinn-proto 0.11.9 and 0.11.12, both < 0.11.14). RHTPA 2.2.2+
  ship quinn-proto 0.11.14 (fixed).
- **Match**: Yes -- current Affects Versions are correct per lock file evidence.
- **Action**: No Affects Versions correction needed.

## Remediation Task Completeness Check

Expected for Cargo ecosystem, stream-scoped to 2.2.x:
- 1 upstream backport task: **Found** (TC-8100)
- 1 downstream propagation task: **Found** (TC-8101)
- Blocking relationship (TC-8101 blocked by TC-8100): **Found**

All expected remediation tasks exist with correct structure.
