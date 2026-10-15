# Step 7.5 — Release Jira Orchestration

Release Jira orchestration would search for or create a release Epic and release Task for the 2.2.x stream before creating remediation tasks. The proposed actions are:

1. **Resolve stream-to-version mapping**: Parse stream `rhtpa-2.2` to release family `2.2.x`. Search for existing release Epic matching `"RHTPA 2.2.* Release Tasks"`.
2. **Find or create release Task**: Search for existing release Task under the release Epic matching `"RHTPA <version> CVE triage"`.
3. **Cross-CVE dedup check**: Inspect the release Task's linked remediation tasks to check if any already cover the same Upstream Affected Component.

Since this eval prohibits external tool calls, release Jira orchestration cannot be confirmed. The release Epic version and child Task creation require interactive confirmation from the engineer. This work is **pending** — no release Jira creation has been performed or claimed.

---

# Step 8 — Remediation

## Triage Decision

**Case B: Affected — create remediation tasks**

Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version.

## Ecosystem Classification

- Ecosystem: **RPM** (system package)
- Per the ecosystem classification table, system package ecosystems produce **1 task** per stream (Konflux release repo fix only)
- No upstream backport task is needed — the fix is applied directly in the Konflux release repo

## Remediation Task Description

The following single remediation task would be created for the 2.2.x stream.

### Task: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)

**Issue Type**: Task
**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-40215`
**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)

---

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

The vulnerable system package (openssl-libs, versions before 3.0.7-28.el9_4)
must be updated to the fixed version in the Konflux release repo.

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1), v0.4.9 (2.2.2, retag of 2.2.1)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (openssl-libs is present in rpms.lock.yaml)
- Update the openssl-libs package version in rpms.in.yaml or rpms.lock.yaml
  to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml after updating the package spec if using rpms.in.yaml
- Verify the Konflux build pipeline triggers successfully with the updated package

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

---

## Description Digest Protocol

After creating the remediation task, the following digest procedure would be performed:

1. **Re-fetch the task description** from Jira after `create_issue`:
   ```
   task_desc = jira.get_issue(<task-key>, fields=["description"])
   ```

2. **Compute the SHA-256 digest** using `scripts/sha256-digest.py`:
   ```
   python3 scripts/sha256-digest.py /tmp/task-desc.md
   ```
   This produces a format-tagged digest (e.g., `sha256-md:<64-char-hex>` or `sha256-adf:<64-char-hex>`).

3. **Post the digest comment** on the task (BEFORE creating issue links or other comments):
   ```
   jira.add_comment(<task-key>, "[sdlc-workflow] Description digest: <tagged-digest>")
   ```

The digest is computed from the re-fetched description (via Jira API after `create_issue`), not from the description string passed to `create_issue`, since Jira normalizes content during storage.

## Jira Linkage

After creating the remediation task and posting its description digest comment:

1. **Link task to Vulnerability issue** (Depend):
   ```
   jira.create_link(
     inwardIssue: "TC-8005",
     outwardIssue: <task-key>,
     type: "Depend"
   )
   ```

2. **If release Jira is active** (from Step 7.5), link task to release Task (Blocks):
   ```
   jira.create_link(
     inwardIssue: <task-key>,
     outwardIssue: <release-task-key>,
     type: "Blocks"
   )
   ```

3. **If release Jira is active**, link CVE to release Task (Related):
   ```
   jira.create_link(
     inwardIssue: <release-task-key>,
     outwardIssue: "TC-8005",
     type: "Related"
   )
   ```

4. **Transition TC-8005 to In Progress** (if not already).

5. **Add `ai-cve-triaged` label** to TC-8005.

6. **Post summary comment** on TC-8005 documenting:
   - Version impact table
   - Affects Versions correction
   - Remediation task created (single task for RPM system package)
   - @mention of the vulnerability reporter

All mutations listed above are **proposed actions** and have not been executed. Each requires engineer confirmation before execution.
