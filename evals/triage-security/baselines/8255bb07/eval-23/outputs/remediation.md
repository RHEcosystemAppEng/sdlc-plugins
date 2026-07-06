# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome Summary

- **Scoped stream (2.2.x)**: Versions 2.2.0-2.2.2 were affected, but the fix is already present in 2.2.3+ (quinn-proto 0.11.14). The latest releases already ship the patched dependency. This is an **already-fixed** scenario for the 2.2.x stream -- no new upstream backport or downstream propagation tasks are needed.
- **Cross-stream (2.1.x)**: All versions (2.1.0, 2.1.1) are affected. The fix has not been backported to the release/0.3.z branch. Since no stream-specific CVE Jira exists for 2.1.x, **preemptive remediation tasks** are created (Case B).

## Cross-Stream Impact Comment

To be posted on TC-8001:

> Cross-stream impact: quinn-proto (versions before 0.11.14) also affects stream 2.1.x based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9. This stream is not tracked by a companion CVE issue and requires preemptive remediation.

---

## Remediation Task 1: Upstream Backport (2.1.x stream, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link**: Related to TC-8001

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (denial of service).
The vulnerable dependency (quinn-proto versions before 0.11.14) must be updated
to the fixed version (0.11.14+).

The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This vulnerability is classified as a denial of service (DoS) with CVSS 7.5 (High).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock (and Cargo.toml if directly specified)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE tracking issue, stream 2.2.x)

---

## Remediation Task 2: Downstream Propagation (2.1.x stream, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
**Labels**: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
**Link**: Related to TC-8001; Blocked by upstream backport task (Task 1)

### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport task bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (Task 1 -- upstream backport must merge first)
- Related to: TC-8001 (originating CVE tracking issue, stream 2.2.x)

---

## Already-Fixed: 2.2.x Stream

The 2.2.x stream does not require new remediation tasks. The fix for CVE-2026-31812 is already present:

| Version | quinn-proto | Status |
|---------|-------------|--------|
| 2.2.3 | 0.11.14 | Fixed |
| 2.2.4 | 0.11.14 | Fixed |

The fix was incorporated starting with build 0.4.11 (version 2.2.3, released 2026-03-23). Earlier versions (2.2.0-2.2.2) were affected but the vulnerability was resolved prior to the latest supported release.

### Affects Versions Correction

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) must be corrected to: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**.

---

## Coordination Guidance Reference

The affected repository `rhtpa-backend` has deployment context **customer-shipped** as configured in the Source Repositories table of the project's CLAUDE.md Security Configuration.

Per the customer-shipped deployment context guidance:

> This component is shipped to customers. Coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure. Fix must be released via a security advisory with explicit CVE-to-component mapping.

This guidance is included in the Implementation Notes of each remediation task description above. It applies to both the upstream backport and downstream propagation tasks. The customer-shipped context means:

1. **CVE assignment coordination** -- Work with Product Security to ensure proper CVE assignment for the product-specific advisory.
2. **Advisory preparation** -- The fix must be accompanied by a formal security advisory that maps the CVE to the affected component.
3. **Formal disclosure** -- Follow the organization's coordinated disclosure process. Do not discuss the fix in public channels or PRs until cleared by Product Security.
