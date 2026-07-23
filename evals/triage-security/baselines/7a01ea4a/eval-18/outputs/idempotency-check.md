# Idempotency Check: TC-8001 Re-Run Analysis

This document analyzes all pre-existing triage artifacts detected on TC-8001
during the second invocation of triage-security, and explains why each
artifact causes the corresponding triage step to be skipped.

## Pre-Existing Artifacts Detected

### 1. Label: `ai-cve-triaged`

- **Detected in**: Issue labels (Step 1 data extraction)
- **Significance**: The `ai-cve-triaged` label is the primary idempotency marker
  applied at the end of the Post-Triage Summary phase. Its presence signals
  that a prior triage run completed successfully through all steps.
- **Effect on re-run**: Discovery mode (no issue key) would exclude this issue
  from the "untriaged" JQL query (`labels NOT IN (ai-cve-triaged)`). When an
  explicit issue key is provided (as in this case), the label does not block
  triage but serves as a signal that all downstream artifacts likely exist.

### 2. Status: In Progress

- **Detected in**: Issue status field (Step 0.7 and status-aware handling)
- **Significance**: The issue has already been transitioned past "New" and
  "Assigned" to "In Progress". This was done by the prior triage run during
  the Jira Linkage phase (remediation-templates.md Step 3: "Transition the
  Vulnerability to In Progress if not already").
- **Effect on re-run**:
  - **Step 0.7 (Assign and Transition to Assigned)**: The transition to
    "Assigned" is skipped because the issue is already past Assigned status.
    Assignment to current user still proceeds (harmless re-assignment).
  - **Status-aware handling**: The skill detects status "In Progress" and
    presents a warning: "This issue is already in In Progress. It may be
    actively worked on." The engineer must confirm to proceed with re-triage
    or skip. For this analysis, we assume the engineer confirms.

### 3. Remediation Tasks: TC-8100 and TC-8101 (Depend links)

- **Detected in**: Issue links array (Step 1 data extraction)
- **Artifacts**:
  - TC-8100 (upstream backport task) -- link type "Depend", status In Progress
  - TC-8101 (downstream propagation subtask) -- link type "Depend", status Open, blocks TC-8100
- **Significance**: These are the two standard remediation tasks for a Cargo
  ecosystem vulnerability (upstream backport + downstream propagation), exactly
  matching the templates in remediation-templates.md.
- **Effect on re-run**:
  - **Step 4.4 (Preemptive Task Reconciliation)**: No preemptive tasks would
    be found because the existing tasks carry standard labels
    (`ai-generated-jira`, `Security`, `CVE-2026-31812`), not `security-preemptive`.
  - **Step 8 (Remediation -- Case A)**: The skill would detect that Depend-linked
    remediation tasks already exist for this stream. Creating duplicate
    remediation tasks would violate the "one remediation Task per affected
    stream" rule (Important Rule 8). The existing TC-8100 and TC-8101 already
    cover the 2.2.x stream. No new tasks are created.

### 4. Description Digest Comment

- **Detected in**: Issue comments (Step 1 data extraction)
- **Content**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
- **Posted by**: sdlc-workflow/triage-security (2026-07-01T10:00:00Z)
- **Significance**: The description digest comment records a hash of the issue
  description at triage time, per shared/description-digest-protocol.md. Its
  presence confirms the prior triage processed this exact description content.
- **Effect on re-run**: A re-run would compute the description digest again.
  If the description has not changed, the digest matches and no new digest
  comment is needed. If the description changed, a new digest comment would
  document the updated content -- but in this scenario the description is
  unchanged, so no new comment is posted.

### 5. Post-Triage Summary Comment

- **Detected in**: Issue comments (Step 1 data extraction)
- **Content**: Full triage summary including version impact, actions taken,
  and the Comment Footnote identifying sdlc-workflow/triage-security v0.11.1
- **Posted by**: sdlc-workflow/triage-security (2026-07-01T10:01:00Z)
- **Significance**: The post-triage summary is the final artifact of a complete
  triage run. It documents the version impact assessment, Affects Versions
  corrections, and all remediation tasks created.
- **Effect on re-run**: A second summary would be redundant. The skill detects
  that a post-triage summary comment already exists (identified by the Comment
  Footnote attribution to `triage-security`) and skips posting a duplicate.

### 6. Affects Versions: Already Correct

- **Detected in**: Jira `versions` field (Step 1 data extraction)
- **Current values**: RHTPA 2.2.0, RHTPA 2.2.1
- **Significance**: These match the version impact analysis exactly -- versions
  2.2.0 and 2.2.1 ship quinn-proto < 0.11.14 (affected), while 2.2.2+ ship
  0.11.14 (not affected). The prior triage already corrected Affects Versions.
- **Effect on re-run**:
  - **Step 3.2 (Compare and Correct Affects Versions)**: The current Affects
    Versions match the proposed correction. The skill notes "Affects Versions
    are already correct" and proceeds without changes. No Jira mutation, no
    correction comment.

### 7. Assignee: Already Set

- **Detected in**: Issue `assignee` field
- **Current value**: engineer-a@example.com
- **Effect on re-run**: Step 0.7 re-assigns to the current user. If the current
  user is the same engineer, this is a no-op. If different, the reassignment
  proceeds (this is intentional -- re-triage by a different engineer should
  update the assignee).

## Summary of Skipped Operations

| Step | Operation | Skipped? | Reason |
|------|-----------|----------|--------|
| 0.7 | Transition to Assigned | Yes | Already past Assigned (In Progress) |
| 3.2 | Affects Versions correction | Yes | Already correct (RHTPA 2.2.0, 2.2.1) |
| 4.2 | Cross-stream sibling linking | N/A | Would re-check; existing links preserved |
| 8 | Create upstream backport task | Yes | TC-8100 already exists (Depend link) |
| 8 | Create downstream propagation task | Yes | TC-8101 already exists (Depend link) |
| 8 | Transition to In Progress | Yes | Already In Progress |
| Post | Add `ai-cve-triaged` label | Yes | Label already present |
| Post | Post summary comment | Yes | Summary comment already exists |
| Post | Post description digest | Yes | Digest comment already exists, description unchanged |
