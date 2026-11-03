# Step 8 – Remediation: TC-8030 (CVE-2026-48901, h2 < 0.4.8)

## Decision

| Question | Answer |
|----------|--------|
| Any supported versions affected? | Yes — 2.1.0, 2.1.1 (stream 2.1.x) |
| Issue scoped to a single stream? | Yes — `[rhtpa-2.2]` → 2.2.x |
| In-scope stream (2.2.x) affected? | **No** — all 2.2.x releases ship h2 >= 0.4.8 |
| Other streams affected? | Yes — 2.1.x |
| Ecosystem | Cargo (source dependency → 2 tasks per affected stream) |

Outcome:
1. **Case C for TC-8030 itself (2.2.x)** — recommend closing as **Not a Bug** (not affected).
   No Case B (non-preemptive) remediation tasks are created for 2.2.x.
2. **Case A — cross-stream impact** — post a cross-stream comment and, since no 2.1.x CVE Jira is
   known, create **preemptive** remediation tasks (upstream backport + downstream propagation) for
   2.1.x, linked to TC-8030 with "Related".

Step 7 (concurrent triage): Upstream Affected Component field not configured → skipped.
Step 7.5 (release Jira): preemptive tasks are not linked to release Jira (only non-preemptive
remediation is); no release Jira structure needed for TC-8030 since 2.2.x is unaffected.

All mutations below are **proposed** and require engineer confirmation; nothing was sent to Jira.

---

## Proposed Jira operations on TC-8030

1. **Affects Versions correction** (Step 3): `[RHTPA 2.2.0]` → `[]` with comment:
   > Corrected Affects Versions: [RHTPA 2.2.0] → []. Based on lock file analysis at pinned commits
   > from security-matrix.md, all 2.2.x releases ship h2 0.4.8 or 0.4.9, which are outside the
   > affected range (< 0.4.8, per MITRE CVE API and OSV.dev RUSTSEC-2026-0089). Scoped to stream
   > 2.2.x per issue suffix.

2. **Cross-stream impact comment** (Case A):
   > Cross-stream impact: h2 < 0.4.8 also affects stream(s) 2.1.x (RHTPA 2.1.0, 2.1.1 ship h2 0.4.5)
   > based on lock file analysis. These streams are tracked by companion issues (see Related links)
   > or may require separate PSIRT triage.

3. **Preemptive tasks comment** (Case A step 5):
   > Preemptive remediation tasks created for streams without CVE Jiras:
   > - 2.1.x: <upstream-task-key> (upstream backport, security-preemptive)
   > - 2.1.x: <downstream-task-key> (downstream propagation, security-preemptive)
   >
   > These tasks use the "Related" link type and carry the security-preemptive label. When PSIRT
   > creates stream-specific CVE Jiras, Step 4.4 reconciliation will link them and remove the label.

4. **Close as Not a Bug** (Case C), comment:
   > No supported versions in stream 2.2.x ship a vulnerable version of h2. Version impact analysis:
   >
   > | Version | h2 | Affected? |
   > |---|---|---|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | 0.4.8 (retag of 2.2.1) | NO |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |
   >
   > All supported 2.2.x versions ship h2 0.4.8 or later, which is outside the affected range
   > (< 0.4.8). Stream 2.1.x is affected and is covered by preemptive remediation tasks (see
   > Related links).
   - Transition: Closed, resolution **Not a Bug**
   - VEX Justification (`customfield_12345`): **Component not Present** (default when lock-file
     analysis shows the vulnerable package version is not included in any in-scope version)

5. **Post-triage**: add label `ai-cve-triaged`; post summary comment (version impact table,
   Affects Versions correction, outcome, preemptive task links, @mention of the reporter, Comment
   Footnote).

---

## Task 1 (preemptive): Upstream backport — 2.1.x

- **Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Link**: TC-8030 → this task, type **Related**
- **Priority note**: production runtime dependency, CVSS 7.5 (High)

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

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood. h2 does not limit the number
of CONTINUATION frames following a HEADERS frame, allowing an attacker to cause
excessive memory allocation and CPU usage (denial of service, CVSS 7.5).
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend tags v0.3.8, v0.3.12

Fix threshold source: MITRE CVE API (lessThan 0.4.8) and OSV.dev RUSTSEC-2026-0089
(fixed 0.4.8) — cross-validated; the Jira description gave no numeric threshold.

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed — h2 is most likely transitive
  (chain: backend → hyper/reqwest/tonic → h2). Run `cargo tree -i h2` on
  release/0.3.z to determine the exact path.
- h2 0.4.8 is semver-compatible with the currently pinned 0.4.5, and stream 2.2.x
  already ships 0.4.8/0.4.9, so `cargo update -p h2 --precise 0.4.8` (or later 0.4.x)
  is expected to suffice.

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.toml / Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (e.g., hyper)
- Bump it (or run `cargo update -p h2`) so the resolved closure includes h2 >= 0.4.8
- Verify no breaking API changes are introduced

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

- Related: TC-8030 (originating CVE Jira, stream 2.2.x)
```

---

## Task 2 (preemptive): Downstream propagation — 2.1.x

- **Summary**: Propagate CVE-2026-48901 h2 fix to rhtpa-release.0.3.z (2.1.x)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-48901`, `security-preemptive`
- **Links**: TC-8030 → this task (**Related**); Task 1 **Blocks** this task

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

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from <upstream-task-key>.

The upstream backport (<upstream-task-key>) bumps h2 to 0.4.8 on release/0.3.z.
Once that PR merges, update the source pinning in this Konflux release repo so the
next 2.1.x build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains the backend
  tag, currently `v0.3.12`)
- **Dependency type**: carried forward from upstream task (likely transitive)
- Update the backend reference to the merged commit or new release tag
- Verify the rebuilt Cargo.lock resolves h2 >= 0.4.8
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <upstream-task-key> (upstream backport must merge first)
- Related: TC-8030 (originating CVE Jira, stream 2.2.x)
```

Each task gets a description digest comment (`[sdlc-workflow] Description digest: ...`) immediately
after creation, before links/other comments.

---

## Pre-creation checklist

- [x] Task count per stream: 2.1.x Cargo → 2 tasks; 2.2.x not affected → 0 tasks
- [x] Cross-stream coverage: 2.1.x covered by preemptive tasks (pending Step 4 sibling verification)
- [x] Link types: Related (preemptive → TC-8030), Blocks (upstream → downstream); no Depend links
      because no remediation is created for TC-8030's own stream
- [x] Preemptive labels: both tasks carry `security-preemptive`
- [x] Coordination guidance: omitted (no Deployment Context column configured)
- [x] Release Jira linking: N/A (preemptive tasks only)
- [x] Dedup consistency: N/A (Step 7.5.3 not applicable)

## Caveats

- If a 2.1.x sibling CVE Jira for CVE-2026-48901 exists (Step 4 JQL not executed in this eval),
  skip the preemptive tasks — 2.1.x would be triaged via its own issue.
- Due date 2026-08-01 has passed; flag to the engineer.
- Security matrix is 128 days stale; a refresh could reveal newer 2.1.x/2.2.x releases.
