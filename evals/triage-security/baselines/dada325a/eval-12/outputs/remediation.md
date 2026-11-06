# Steps 4–8 – Remediation: TC-8030 / CVE-2026-48901 (h2 < 0.4.8)

## Steps 4–7 (eval assumptions; no Jira queries executed)

| Step | Result |
|------|--------|
| 4 Duplicate / sibling check | Would run JQL `project = TC AND issuetype = 10024 AND labels = CVE-2026-48901`. The fixture contains no sibling data, so we assume **no 2.1.x companion CVE Jira exists**. This should be verified before creating the tasks below |
| 4.3 Cross-CVE overlap | Skipped. Upstream Affected Component field is not configured |
| 4.4 Preemptive reconciliation | No existing preemptive tasks in the fixture |
| 5 Lifecycle check | Would check https://access.example.com/product-life-cycle/rhtpa for 2.1.x support status. No lifecycle data in the fixture, so 2.1.x is assumed supported |
| 6 Already fixed | No resolved siblings |
| 7 Concurrent triage | Skipped. Upstream Affected Component field is not configured |
| 7.5 Release Jira | Would find or create "RHTPA <next 2.1.x version> Release Tasks" Epic and "RHTPA <version> CVE triage" Task. No release data is in the fixture. Release Jira linking applies only to non-preemptive tasks, and every task here is preemptive |

## Decision

- Issue scope **2.2.x: no versions affected.** All 2.2.x releases ship h2 0.4.8 or 0.4.9, which are >= the fixed 0.4.8.
- Other stream **2.1.x: affected.** 2.1.0 and 2.1.1 ship h2 0.4.5.
- The path is therefore **Case A (cross-stream impact).** The skill posts a cross-stream comment and creates **preemptive** remediation tasks for 2.1.x (Cargo is a source dependency, so 2 tasks). It creates **no** standard Case B tasks for 2.2.x.
- TC-8030 itself: its scoped stream is not affected, so the recommendation is to **close as Not a Bug**, with VEX Justification (customfield_12345) = **Component not Present**. The vulnerable h2 version (< 0.4.8) is not shipped in any 2.2.x release. Close only after the cross-stream comment and preemptive tasks are recorded. The engineer should confirm the closure.

### Proposed Jira actions (all require engineer confirmation; none executed)

1. Affects Versions: `[RHTPA 2.2.0]` → `[]`, with a correction comment and footnote.
2. Cross-stream impact comment on TC-8030:
   > Cross-stream impact: h2 < 0.4.8 (CVE-2026-48901) also affects stream(s) 2.1.x (RHTPA 2.1.0, 2.1.1 ship h2 0.4.5) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.
   >
   > _Comment footnote (triage-security)_
3. Create the 2 preemptive tasks below. Each gets a description digest comment, then a `Related` link from TC-8030, plus `Blocks` from the upstream task to the downstream task.
4. Comment listing the preemptive tasks:
   > Preemptive remediation tasks created for streams without CVE Jiras:
   > - 2.1.x: <upstream-task-key> (security-preemptive)
   > - 2.1.x: <downstream-task-key> (security-preemptive)
   >
   > These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.
   >
   > _Comment footnote (triage-security)_
5. Close TC-8030 as Not a Bug with VEX = Component not Present, plus a comment: "No supported 2.2.x versions ship a vulnerable version of h2. Version impact analysis: [table]. All 2.2.x versions ship h2 0.4.8/0.4.9, which is outside the affected range (< 0.4.8)." The comment includes the footnote.
6. Add the `ai-cve-triaged` label and post a summary comment covering the impact table, the Affects Versions correction, the outcome, the preemptive task links, the absence of release Jira for preemptive tasks, no dedup, an @mention of the reporter, and the footnote.

---

## Task 1 (preemptive): Upstream backport, 2.1.x

- **Summary:** Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)
- **Issue type:** Task
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Link:** TC-8030 → this task, type **Related**

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists yet
> for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood (unbounded CONTINUATION
frames after HEADERS cause excessive memory/CPU use; DoS, CVSS 7.5).
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p (RUSTSEC-2026-0089)

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage (lock-file version only was
  available). Determine with `cargo tree -i h2` on release/0.3.z; h2 is commonly
  transitive via hyper/reqwest/tonic.
- Fix threshold source: MITRE CVE API (lessThan 0.4.8) and OSV.dev (fixed 0.4.8),
  cross-validated; Jira description gave no precise range.
- If the vulnerable dependency is dev-only or build-only, the remediation priority
  is Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if declared)
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (e.g., hyper / reqwest / tonic)
- Bump it to a version whose transitive closure includes h2 >= 0.4.8
  (h2 0.4.x is semver-compatible, so `cargo update -p h2` may suffice)
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo add h2@0.4.8` to override the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8 in Cargo.lock on release/0.3.z
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (originating tracking issue, stream 2.2.x — Related link)
```

---

## Task 2 (preemptive): Downstream propagation, 2.1.x

- **Summary:** Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
- **Issue type:** Task
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Links:** TC-8030 → this task, type **Related**. Task 1 **Blocks** this task.

```
## Repository

rhtpa-release.0.3.z (git.example.com/rhtpa/rhtpa-release.0.3.z)

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists yet
> for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix
from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag,
  currently `v0.3.12`)
- **Dependency type**: not determined — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is
  reflected in the downstream build's Cargo.lock after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix (h2 >= 0.4.8)
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8030 (originating tracking issue, stream 2.2.x — Related link)
```

---

## Pre-creation checklist

- [x] Task count per stream: 2 for 2.1.x (Cargo is a source dependency); 0 for 2.2.x (not affected)
- [x] Cross-stream coverage: the affected 2.1.x stream has preemptive tasks (assuming no sibling CVE Jira)
- [x] Link types: Related (preemptive → originating TC-8030) and Blocks (upstream → downstream). No Depend links, since there are no own-stream tasks
- [x] Preemptive labels: `security-preemptive` on both tasks
- [x] Coordination guidance: omitted, because the Deployment Context column is absent (backward compatibility)
- [x] Release Jira linking: not applicable. Preemptive tasks are not linked to release Jira
- [x] Dedup consistency: no Step 7.5.3 dedup (Upstream Affected Component is not configured)
