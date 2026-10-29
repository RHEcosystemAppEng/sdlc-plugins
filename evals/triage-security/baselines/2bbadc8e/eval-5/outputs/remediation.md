# Step 8 -- Remediation

## Triage Decision

**Ecosystem**: RPM (system package) -- 1 remediation task per affected stream.

**Version impact summary (2.2.x stream)**:
- Affected: 2.2.0, 2.2.1, 2.2.2
- Not affected: 2.2.3, 2.2.4 (already ship fixed openssl-libs 3.0.7-28.el9_4)

**Key finding**: The fix is already present in the latest released versions
(2.2.3 and 2.2.4). The openssl-libs package was updated to 3.0.7-28.el9_4
as part of the regular release process in build 0.4.11 (2026-03-23).

**Case B applies**: Supported versions 2.2.0 through 2.2.2 are affected.
Although the latest versions already ship the fix, the affected versions
require tracking via Affects Versions and remediation documentation.

Since this is an RPM system package present in rpms.lock.yaml (explicit
install), one remediation task is created for the 2.2.x stream.

## Cross-Stream Impact (Case A)

This issue is scoped to 2.2.x, but version impact analysis shows the
2.1.x stream is also affected:

| Version | openssl-libs | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 3.0.7-24.el9 | YES |
| 2.1.1 | 3.0.7-24.el9 | YES |

PROPOSAL: Post cross-stream impact comment on TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also
affects stream 2.1.x based on rpms.lock.yaml analysis.
These streams are tracked by companion issues (see Related links) or may
require separate PSIRT triage.
```

PROPOSAL: Search for existing CVE Jiras for stream 2.1.x with label
CVE-2026-40215. If none exist, create a preemptive remediation task
for stream 2.1.x with the `security-preemptive` label and "Related"
link type to TC-8005.

## Remediation Task Description (2.2.x stream)

The following task would be created as a Jira Task using the system package
(RPM) template for explicit install origin:

---

### PROPOSAL: Jira Task Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <see task description below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability was found in openssl-libs. Versions before
3.0.7-28.el9_4 are vulnerable to a buffer over-read during X.509 certificate
chain verification. A remote attacker can craft a certificate with a malformed
extension that triggers an out-of-bounds read, potentially leaking sensitive
memory contents or causing a crash.

CVSS: 7.1 (High)

Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Source commit(s): v0.4.5 (2.2.0), v0.4.8 (2.2.1), v0.4.9 (2.2.2, retag of 2.2.1)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

Note: The fix (openssl-libs 3.0.7-28.el9_4) is already present in RHTPA 2.2.3+
(builds v0.4.11 and v0.4.12). This task tracks the remediation for affected
versions 2.2.0-2.2.2 and ensures the fix is documented.

## Implementation Notes

- Package origin: explicit install (openssl-libs present in rpms.lock.yaml)
- SBOM verification: skipped (cosign not available); rpms.lock.yaml
  classification used as sole source of truth
- Fixed version is already included in builds v0.4.11+ (versions 2.2.3+)
- Update the package version spec in rpms.in.yaml / rpms.lock.yaml to
  require openssl-libs >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if using a lock file workflow
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo
policy before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

---

### PROPOSAL: Post-Creation Actions

1. **Description digest comment** on the new task (before links):
   ```
   [sdlc-workflow] Description digest: sha256-md:<hex>
   ```

2. **Link task to Vulnerability issue** (Depend):
   ```
   jira.create_link(
     inwardIssue: "TC-8005",
     outwardIssue: "<new-task-key>",
     type: "Depend"
   )
   ```

3. **Link task to release Task** (Blocks, if Step 7.5 created one):
   ```
   jira.create_link(
     inwardIssue: "<new-task-key>",
     outwardIssue: "<release-task-key>",
     type: "Blocks"
   )
   ```

4. **Link CVE to release Task** (Related):
   ```
   jira.create_link(
     inwardIssue: "<release-task-key>",
     outwardIssue: "TC-8005",
     type: "Related"
   )
   ```

5. **Add `ai-cve-triaged` label** to TC-8005.

6. **Post-triage summary comment** on TC-8005 documenting:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation task key
   - Cross-stream impact note (2.1.x also affected)
   - Reporter @mention (ADF mention node)
   - Comment Footnote

## Pre-Creation Checklist

- [x] **Task count per stream**: 1 task (RPM system package = 1 task per stream)
- [x] **Cross-stream coverage**: 2.1.x stream is affected; preemptive task
      or sibling CVE Jira required
- [x] **Link types**: "Depend" for task linked to its CVE Jira (TC-8005)
- [x] **Coordination guidance**: included (upstream context)
- [x] **SBOM verification**: documented as skipped (cosign not available)
