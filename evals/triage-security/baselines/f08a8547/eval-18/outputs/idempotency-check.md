# Idempotency Check: TC-8001 Re-Run Analysis

This document analyzes all pre-existing triage artifacts detected on issue TC-8001
during the second (re-run) invocation of triage-security, and explains why each
artifact causes the corresponding triage step to be skipped.

## Summary

TC-8001 was fully triaged in a prior run on 2026-07-01. All triage artifacts are
already present. The re-run detects each one and skips the corresponding mutation,
producing a fully idempotent execution with zero new Jira writes.

---

## Artifact 1: `ai-cve-triaged` Label

- **Detected**: Yes -- the label `ai-cve-triaged` is present in the issue's Labels field.
- **Skill behavior**: The Post-Triage Summary (end of Step 8) adds this label to mark
  an issue as triaged. On re-run, the label is already present.
- **Action**: Skip adding the label. No Jira `edit_issue` call needed for labels.
- **Relevant step**: Post-Triage Summary, section 1 ("Add the ai-cve-triaged label").

## Artifact 2: Issue Status -- In Progress

- **Detected**: Yes -- the issue's current status is "In Progress", which is a
  post-triage status (beyond New and Assigned).
- **Skill behavior**: Step 0.7 transitions the issue to Assigned (if in New status)
  and assigns it to the current user. The status-aware handling in the Inputs section
  detects that the issue is already in "In Progress" and warns: "This issue is already
  in In Progress. It may be actively worked on."
- **Action**: Skip the Assigned transition (status is already beyond Assigned). The
  assignment to the current user still proceeds (Step 0.7, step 4: "If the issue is
  already in Assigned or any later status, skip the transition silently"). No status
  transition mutation is needed.
- **Relevant step**: Step 0.7 (Assign and Transition to Assigned) and Inputs
  section (status-aware handling).

## Artifact 3: Remediation Task TC-8100 (Upstream Backport)

- **Detected**: Yes -- issue link of type "Depend" to TC-8100 exists.
  - TC-8100 Summary: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]"
  - TC-8100 Status: In Progress
  - TC-8100 Labels: ai-generated-jira, Security, CVE-2026-31812
- **Skill behavior**: Step 8 (Case B) creates remediation tasks for affected streams.
  For the Cargo ecosystem (source dependency), two tasks are created per stream:
  an upstream backport task and a downstream propagation task. On re-run, the existing
  Depend link to TC-8100 indicates that the upstream backport task already exists for
  stream 2.2.x.
- **Action**: Skip creation of the upstream backport task for stream 2.2.x. The task
  already exists and is linked. No `create_issue` or `create_link` call needed.
- **Relevant step**: Step 8 (Remediation, Case B) and remediation-templates.md.

## Artifact 4: Remediation Task TC-8101 (Downstream Propagation)

- **Detected**: Yes -- issue link of type "Depend" to TC-8101 exists.
  - TC-8101 Summary: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]"
  - TC-8101 Status: Open
  - TC-8101 Labels: ai-generated-jira, Security, CVE-2026-31812
  - TC-8101 Blocks: TC-8100
- **Skill behavior**: Step 8 (Case B) creates a downstream propagation task blocked by
  the upstream backport task. On re-run, the existing Depend link to TC-8101 indicates
  that the downstream propagation task already exists for stream 2.2.x.
- **Action**: Skip creation of the downstream propagation task for stream 2.2.x.
  The task already exists and is linked. No `create_issue`, `create_link`, or
  Blocks link creation needed.
- **Relevant step**: Step 8 (Remediation, Case B) and remediation-templates.md.

## Artifact 5: Description Digest Comment

- **Detected**: Yes -- comment matching the marker string `[sdlc-workflow] Description digest:`
  found on the issue.
  - Digest value: `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
  - Posted by: sdlc-workflow/triage-security
  - Created: 2026-07-01T10:00:00Z
- **Skill behavior**: The description-digest-protocol requires that a digest comment be
  posted after creating each remediation task. Since no new remediation tasks are created
  on re-run, no new digest comments are needed. The existing digest comment on the
  Vulnerability issue itself is a record from the prior triage run.
- **Action**: No new digest comments to post. Existing digest is preserved as-is.
- **Relevant step**: Remediation Task Creation / description-digest-protocol.md.

## Artifact 6: Post-Triage Summary Comment

- **Detected**: Yes -- a post-triage summary comment exists on the issue documenting:
  - Version impact (RHTPA 2.2.0 and 2.2.1 affected; 2.2.2+ not affected)
  - Affects Versions correction performed
  - ai-cve-triaged label added
  - Remediation tasks created (TC-8100 upstream backport, TC-8101 downstream propagation)
  - Status transitioned to In Progress
  - Comment footer references sdlc-workflow/triage-security v0.11.1
- **Skill behavior**: The Post-Triage Summary (section 2) posts a summary comment after
  all triage actions are complete. On re-run, a summary comment already exists.
- **Action**: Skip posting a duplicate summary comment. The existing comment provides
  a complete audit trail from the prior triage run.
- **Relevant step**: Post-Triage Summary, section 2.

## Artifact 7: Affects Versions Already Correct

- **Detected**: Yes -- the current Affects Versions on TC-8001 are `RHTPA 2.2.0, RHTPA 2.2.1`.
- **Skill behavior**: Step 3 (Affects Versions Correction) compares the PSIRT-assigned
  Affects Versions against the version impact table. The version impact analysis shows
  that RHTPA 2.2.0 (quinn-proto 0.11.9) and RHTPA 2.2.1 (quinn-proto 0.11.12) are
  affected, while RHTPA 2.2.2+ ship quinn-proto 0.11.14 (fixed). The current Affects
  Versions already match the expected values.
- **Action**: "Affects Versions are already correct" -- no correction needed. No
  `edit_issue` call for the versions field.
- **Relevant step**: Step 3 (Affects Versions Correction), jira-triage-operations.md.

---

## Complete Idempotency Matrix

| Triage Step | Artifact | Present? | Re-Run Action |
|-------------|----------|----------|---------------|
| Step 0.7 | Status beyond New | Yes (In Progress) | Skip transition |
| Step 1 | CVE data extraction | N/A (read-only) | Re-extract (no mutation) |
| Step 3 | Affects Versions | Already correct | Skip correction |
| Step 4 | Sibling/duplicate check | N/A (read-only) | Re-check (no mutation) |
| Step 8 | TC-8100 (upstream backport) | Yes (Depend link) | Skip task creation |
| Step 8 | TC-8101 (downstream propagation) | Yes (Depend link) | Skip task creation |
| Post-Triage | ai-cve-triaged label | Yes | Skip adding label |
| Post-Triage | Summary comment | Yes | Skip posting comment |
| Post-Triage | Description digest comment | Yes | Skip posting digest |
