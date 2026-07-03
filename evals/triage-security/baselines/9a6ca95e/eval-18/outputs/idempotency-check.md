# Idempotency Check: TC-8001 (Re-Run)

This document records every pre-existing triage artifact detected on TC-8001
during a second invocation of `/sdlc-workflow:triage-security`, and the
decision to skip each corresponding mutation.

## Pre-Existing Triage Artifacts Detected

### 1. `ai-cve-triaged` label

- **Present**: YES (found in issue labels)
- **Implication**: The Post-Triage Summary (final step) already ran on a prior
  invocation. This label is the canonical marker that triage was completed.
- **Action**: SKIP adding the label again -- already present.

### 2. Status: In Progress

- **Current status**: In Progress
- **Expected for untriaged**: New
- **Implication**: Step 0.7 (Assign and Transition to Assigned) and the
  remediation step's transition to In Progress both already executed. The issue
  has moved past both the Assigned and In Progress transitions.
- **Action**: SKIP status transition -- already at or past In Progress. Per the
  skill's status-aware handling, the issue is flagged as "already in In Progress"
  and the user is warned that this issue may be actively worked on.

### 3. Assignee set

- **Current assignee**: engineer-a@example.com
- **Implication**: Step 0.7 already assigned the issue during the prior run.
- **Action**: SKIP assignment -- already assigned. (Step 0.7 notes: "The
  assignment in step 2 still proceeds regardless" but in an eval context with
  no Jira access, this is a no-op observation.)

### 4. Remediation tasks linked via Depend

Two remediation tasks are already linked to TC-8001:

| Link Type | Task Key | Summary | Status |
|-----------|----------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

- **Expected from fresh triage**: Step 8 Case A would create exactly two tasks
  for a Cargo ecosystem CVE -- one upstream backport task and one downstream
  propagation subtask. Both are present.
- **TC-8100** matches the upstream backport template (summary pattern:
  "Backport ... fix to >= [fixed-version] on [upstream-branch] [stream]",
  labels: ai-generated-jira, Security, CVE-2026-31812).
- **TC-8101** matches the downstream propagation template (summary pattern:
  "Propagate ... bump to [repo] release branch [stream]", labels:
  ai-generated-jira, Security, CVE-2026-31812), and has a Blocks link to
  TC-8100 (downstream blocked by upstream).
- **Action**: SKIP remediation task creation -- both tasks already exist and
  are linked with the correct link types (Depend to CVE, Blocks between tasks).
  Creating new tasks would produce duplicates.

### 5. Description digest comment

- **Present**: YES
- **Content**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
- **Posted by**: sdlc-workflow/triage-security (2026-07-01T10:00:00Z)
- **Implication**: The description digest protocol already ran. This comment
  enables `/implement-task` to verify description integrity.
- **Action**: SKIP posting a duplicate digest comment. The existing digest
  can be compared against the current description to detect if the description
  changed since the prior triage -- but a new digest comment is not needed
  unless the description was modified.

### 6. Post-triage summary comment

- **Present**: YES
- **Content**: Documents version impact (RHTPA 2.2.0 and 2.2.1 affected,
  2.2.2+ not affected), Affects Versions correction, remediation tasks
  (TC-8100, TC-8101), and transition to In Progress.
- **Posted by**: sdlc-workflow/triage-security (2026-07-01T10:01:00Z)
- **Implication**: The full triage workflow completed in the prior run,
  including the final summary. Posting another summary comment would create
  redundant audit trail entries.
- **Action**: SKIP posting a duplicate summary comment.

### 7. Affects Versions already correct

- **Current Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1
- **Version impact analysis**: 2.2.0 (YES, quinn-proto 0.11.9), 2.2.1
  (YES, quinn-proto 0.11.12), 2.2.2 (YES, retag), 2.2.3+ (NO, 0.11.14).
  Scoped to stream 2.2.x, only released affected versions are 2.2.0 and 2.2.1.
  (2.2.2 is a retag of 2.2.1 but shares the same Jira version tracking.)
- **Implication**: Step 3 already corrected Affects Versions in the prior run.
  The current values match what Step 3 would propose.
- **Action**: SKIP Affects Versions correction -- already correct.

## Summary of Idempotency Checks

| Artifact | Present? | Action |
|----------|----------|--------|
| `ai-cve-triaged` label | YES | SKIP |
| Status In Progress | YES | SKIP transition |
| Assignee | YES | SKIP (or no-op re-assign) |
| Remediation task TC-8100 (upstream) | YES, linked via Depend | SKIP task creation |
| Remediation task TC-8101 (downstream) | YES, linked via Depend | SKIP task creation |
| TC-8101 Blocks TC-8100 | YES | SKIP link creation |
| Description digest comment | YES | SKIP |
| Post-triage summary comment | YES | SKIP |
| Affects Versions correction | Already correct | SKIP |

**Total Jira mutations on re-run: 0**
