# Step 7.5 / Step 8 – Remediation: TC-8030 (CVE-2026-48901, h2 < 0.4.8)

## Decision

| Question | Answer |
|---|---|
| Any supported version affected? | Yes — 2.1.0, 2.1.1 (stream 2.1.x) |
| Issue scoped to a single stream? | Yes — `[rhtpa-2.2]` → 2.2.x |
| Issue-stream (2.2.x) versions affected? | **No** — all 2.2.x ship h2 0.4.8 or 0.4.9 (>= fixed 0.4.8) |
| Other streams affected? | Yes — 2.1.x (h2 0.4.5) |
| Path | **Case A** (cross-stream impact for 2.1.x) + **no Case B tasks for 2.2.x**; TC-8030 itself is **closed as Not a Bug** for its stream (Case C applied to the scoped stream) |

No remediation tasks are created for the 2.2.x stream. Remediation for 2.1.x is
handled via the cross-stream path (companion CVE Jira or preemptive tasks).

Step 7.5 (release Jira): no release Epic/Task is needed for 2.2.x (no 2.2.x
remediation). Preemptive tasks are not linked to release Jira. Cross-CVE dedup
(7.5.3) is skipped — Upstream Affected Component field not configured.

---

## Action 1 – Correct Affects Versions on TC-8030 (requires confirmation)

Remove `RHTPA 2.2.0`. Lock-file evidence: 2.2.0 (backend `v0.4.5`) ships h2 0.4.8,
which is the fixed version per MITRE (`lessThan: 0.4.8`) and OSV
(`fixed: 0.4.8`).

## Action 2 – Cross-stream impact comment on TC-8030 (requires confirmation)

```
Cross-stream impact: h2 < 0.4.8 (CVE-2026-48901) also affects stream 2.1.x
(RHTPA 2.1.0, 2.1.1 — backend v0.3.8 / v0.3.12 ship h2 0.4.5) based on lock
file analysis. This stream is tracked by a companion issue (see Related links)
or may require separate PSIRT triage.

---
_Posted by sdlc-workflow/triage-security_
```
(Exact footnote format per `shared/comment-footnote.md`.)

## Action 3 – Close TC-8030 as Not a Bug (requires confirmation)

Comment:

```
No supported versions in stream 2.2.x ship a vulnerable version of h2.

Fix threshold: h2 < 0.4.8 affected (MITRE CVE API lessThan 0.4.8; OSV.dev
RUSTSEC-2026-0089 fixed 0.4.8). The Jira description's range ("versions prior
to the fix") was imprecise and was resolved from these structured sources.

| Version | Backend tag | h2    | Affected? |
|---------|-------------|-------|-----------|
| 2.2.0   | v0.4.5      | 0.4.8 | NO        |
| 2.2.1   | v0.4.8      | 0.4.8 | NO        |
| 2.2.2   | v0.4.8      | —     | NO (same as 2.2.1, retag) |
| 2.2.3   | v0.4.11     | 0.4.9 | NO        |
| 2.2.4   | v0.4.12     | 0.4.9 | NO        |

All 2.2.x versions ship h2 0.4.8 or 0.4.9, which is outside the affected range
(< 0.4.8). Stream 2.1.x is affected — see cross-stream impact comment.

---
_Posted by sdlc-workflow/triage-security_
```

- Transition: Closed, resolution **Not a Bug** (target discovered via
  `get_transitions`).
- VEX Justification (`customfield_12345`): **Component not Present** — the
  vulnerable h2 version (< 0.4.8) is not included in any 2.2.x build (skill
  default when lock-file analysis shows the vulnerable version is absent).
- Add label `ai-cve-triaged`; post-triage summary comment with @mention of the
  issue reporter (reporter account ID not present in fixture).

---

## Action 4 – 2.1.x remediation (Case A, conditional on Step 4 / Step 5)

1. Run the Step 4 sibling JQL for `CVE-2026-48901` with a `[rhtpa-2.1]` suffix.
   - **Sibling exists** → no tasks here; 2.1.x is triaged via that issue (link it
     as Related).
   - **No sibling** → create the two **preemptive** tasks below
     (label `security-preemptive`, linked to TC-8030 with **Related**, not Depend).
2. Confirm 2.1.x is still in support (Step 5, product pages) before creating them.

Neither the sibling search nor the lifecycle check could be run in this eval, so
the tasks below are the proposed descriptions for the "no sibling, still
supported" outcome.

### Task 1 – Upstream backport (preemptive)

- **Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Links**: TC-8030 → Task 1 (**Related**); Task 1 **Blocks** Task 2

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

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood. h2 does not limit the
number of CONTINUATION frames following a HEADERS frame, allowing an attacker to
cause excessive memory allocation and CPU usage (denial of service, CVSS 7.5).
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version
(0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p
(also RUSTSEC-2026-0089: https://rustsec.org/advisories/RUSTSEC-2026-0089.html)

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage — verify whether h2 is a
  direct dependency of a workspace member or transitive (commonly via
  hyper/reqwest/tonic) by inspecting Cargo.toml files and `cargo tree -i h2`
  on release/0.3.z. Apply the matching approach below.
- Fix threshold source: MITRE CVE API (lessThan 0.4.8) and OSV.dev (fixed 0.4.8)
  agree; 0.4.8 is the first non-vulnerable version.
- If the vulnerable dependency is dev-only or build-only, the remediation
  priority is Normal regardless of CVE severity. Add `dev-dependency` label to
  the task.

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if the version
  requirement excludes 0.4.8)
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (`cargo tree -i h2`)
- Bump the direct dependency to a version whose transitive closure includes
  h2 >= 0.4.8 (often `cargo update -p h2` suffices since 0.4.8 is
  semver-compatible with 0.4.5)
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add h2@0.4.8` to add as a direct dependency, overriding the
  transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8030 (parent tracking issue — Related link, preemptive)
```

### Task 2 – Downstream propagation (preemptive)

- **Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Links**: TC-8030 → Task 2 (**Related**); blocked by Task 1

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists yet
> for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains the backend
  tag; currently `v0.3.12` for 2.1.1)
- **Dependency type**: carried forward from upstream task (determined there)
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning
  is reflected in the downstream build's Cargo.lock after the source reference
  update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Depends on: TC-8030 (parent tracking issue — Related link, preemptive)
```

Each task gets a description digest comment (per
`shared/description-digest-protocol.md`) immediately after creation, before any
link or other comment. Coordination Guidance is omitted (no Deployment Context
column in Source Repositories).

### Follow-up comment on TC-8030 (if preemptive tasks are created)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <task-1-key> (upstream backport), <task-2-key> (downstream propagation,
  blocked by <task-1-key>) (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation
will link them and remove the label.

---
_Posted by sdlc-workflow/triage-security_
```

## Pre-creation checklist

- [x] Task count per stream: Cargo → 2 tasks for 2.1.x; 0 for unaffected 2.2.x
- [x] Cross-stream coverage: 2.1.x covered by sibling CVE Jira (if found) or preemptive tasks
- [x] Link types: Related (preemptive → TC-8030), Blocks (upstream → downstream); no Depend links (no in-scope tasks)
- [x] Preemptive labels on both 2.1.x tasks
- [x] Coordination guidance: omitted (Deployment Context column absent)
- [x] Release Jira linking: n/a (no non-preemptive remediation tasks)
- [x] Dedup consistency: 7.5.3 skipped (field not configured)

No Jira mutations were executed (eval mode).
