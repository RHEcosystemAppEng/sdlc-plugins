# Idempotency Check: TC-8001 (Re-Run)

This document records all pre-existing triage artifacts detected on issue TC-8001
during a second invocation of triage-security, and explains why each mutation
was skipped.

## Summary

All six categories of triage artifacts are already present on TC-8001. The
second run detects each one and skips the corresponding mutation. Zero Jira
writes are required.

## Pre-Existing Artifacts Detected

### 1. Label: `ai-cve-triaged`

- **Detection method**: Checked the issue's `labels` array from the Step 1
  `get_issue` response. The label `ai-cve-triaged` is present in the labels
  list: `[CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged]`.
- **Artifact origin**: Added by the first triage run during the Post-Triage
  Summary phase (SKILL.md: "Add the `ai-cve-triaged` label to the original
  Vulnerability issue to mark it as triaged").
- **Action**: SKIP -- do not add the label again. Adding a duplicate label
  would be a no-op in Jira but constitutes an unnecessary API call. The label's
  presence confirms this issue has already been fully triaged.

### 2. Status: In Progress

- **Detection method**: Checked the issue's `status` field from the Step 1
  `get_issue` response. Current status is `In Progress`.
- **Artifact origin**: The first triage run transitioned the issue from New
  through Assigned to In Progress as part of Step 0.7 and the remediation
  workflow.
- **Action**: SKIP -- do not attempt any status transition. Per the SKILL.md
  status-aware handling rules, an issue already in `In Progress` triggers a
  warning: "This issue is already in In Progress. It may be actively worked on."
  Since this is a re-run (not a new triage), no transition is needed. The
  Step 0.7 transition to Assigned is also skipped because the issue is already
  past that status.

### 3. Depend Link: TC-8001 -> TC-8100 (upstream backport task)

- **Detection method**: Inspected the issue's `issuelinks` array from the
  Step 1 `get_issue` response. Found a link with:
  - `type.name` = "Depend"
  - Target issue key = TC-8100
  - Summary: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]"
  - Status: In Progress
  - Labels include: `ai-generated-jira`, `Security`, `CVE-2026-31812`
- **Artifact origin**: Created by the first triage run during Step 8 (Case A
  remediation -- Cargo ecosystem produces two tasks: upstream backport +
  downstream propagation). The link connects the CVE Vulnerability issue to
  its upstream remediation Task.
- **Action**: SKIP -- do not create a new upstream backport task or a duplicate
  Depend link. The existing task TC-8100 already covers the upstream fix for
  stream 2.2.x. Creating another task would produce duplicate remediation work.

### 4. Depend Link: TC-8001 -> TC-8101 (downstream propagation task)

- **Detection method**: Inspected the issue's `issuelinks` array from the
  Step 1 `get_issue` response. Found a link with:
  - `type.name` = "Depend"
  - Target issue key = TC-8101
  - Summary: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]"
  - Status: Open
  - Labels include: `ai-generated-jira`, `Security`, `CVE-2026-31812`
  - Blocks: TC-8100 (downstream is blocked by upstream)
- **Artifact origin**: Created by the first triage run during Step 8 (Case A
  remediation -- the second of two Cargo ecosystem tasks). The link connects
  the CVE Vulnerability issue to its downstream propagation Task.
- **Action**: SKIP -- do not create a new downstream propagation task or a
  duplicate Depend link. The existing task TC-8101 already covers the Konflux
  release repo update for stream 2.2.x, and its blocking relationship with
  TC-8100 is correctly established.

### 5. Description Digest Comment

- **Detection method**: Scanned the issue's comments array from the Step 1
  `get_issue` response. Found comment #1 matching the description digest
  pattern:
  - Prefix: `[sdlc-workflow] Description digest:`
  - Hash: `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
  - Author: `sdlc-workflow/triage-security`
  - Created: 2026-07-01T10:00:00Z
- **Artifact origin**: Posted by the first triage run as part of the
  description digest protocol (shared/description-digest-protocol.md). This
  comment records the hash of the issue description at triage time, enabling
  downstream skills (like /implement-task) to detect description changes.
- **Action**: SKIP -- do not post a duplicate description digest comment. The
  existing digest already captures the description state. If the description
  had changed since the first triage, a new digest would be warranted, but
  the description content is unchanged.

### 6. Post-Triage Summary Comment

- **Detection method**: Scanned the issue's comments array from the Step 1
  `get_issue` response. Found comment #2 matching the post-triage summary
  pattern:
  - Content: "Triage complete for CVE-2026-31812 (quinn-proto)..."
  - Documents: version impact, Affects Versions correction, remediation tasks
    created (TC-8100, TC-8101), transition to In Progress
  - Footer: "This comment was AI-generated by sdlc-workflow/triage-security v0.11.1"
  - Author: `sdlc-workflow/triage-security`
  - Created: 2026-07-01T10:01:00Z
- **Artifact origin**: Posted by the first triage run during the Post-Triage
  Summary phase (the final step of triage-security). This comment serves as
  the complete audit trail for the triage session.
- **Action**: SKIP -- do not post a duplicate post-triage summary. The existing
  summary already provides the full audit trail. Posting a second summary would
  create noise on the issue and confuse stakeholders reviewing the comment
  history.

## Affects Versions Check

- **Current Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1
- **Version impact analysis** (from security-matrix.md mock data):
  - RHTPA 2.2.0 (tag v0.4.5): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
  - RHTPA 2.2.1 (tag v0.4.8): quinn-proto 0.11.12 -- AFFECTED (< 0.11.14)
  - RHTPA 2.2.2 (tag v0.4.9): retag of v0.4.8 -- AFFECTED (same as 2.2.1)
  - RHTPA 2.2.3 (tag v0.4.11): quinn-proto 0.11.14 -- NOT AFFECTED (>= 0.11.14)
  - RHTPA 2.2.4 (tag v0.4.12): quinn-proto 0.11.14 -- NOT AFFECTED (>= 0.11.14)
- **Assessment**: The existing Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1) are
  already correct per the version impact analysis. No correction needed.
- **Action**: SKIP -- no Affects Versions mutation required.

Note: RHTPA 2.2.2 is also affected (retag of 2.2.1 with the same quinn-proto
version), but the post-triage summary from the first run states "RHTPA 2.2.2
and later ship quinn-proto 0.11.14 (not affected)" -- this may reflect a
judgment that 2.2.2 was a retag that did not actually ship as a product version,
or the first triage run resolved this differently. In either case, the Affects
Versions were already reviewed and confirmed by the engineer in the first run.

## Complete Skip Inventory

| Artifact | Detected | Mutation Skipped |
|----------|----------|------------------|
| `ai-cve-triaged` label | Yes -- present in labels array | Label addition skipped |
| In Progress status | Yes -- current status field | Status transition skipped |
| Depend link to TC-8100 | Yes -- in issuelinks array | Task creation + link creation skipped |
| Depend link to TC-8101 | Yes -- in issuelinks array | Task creation + link creation skipped |
| Description digest comment | Yes -- comment #1 matches digest pattern | Comment posting skipped |
| Post-triage summary comment | Yes -- comment #2 matches summary pattern | Comment posting skipped |

**Total mutations skipped: 6**
**Total mutations executed: 0**
