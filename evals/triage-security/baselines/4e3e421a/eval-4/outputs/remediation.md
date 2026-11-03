# TC-8004 — Step 7.5 / Step 8 Remediation

## Decision

- Supported versions affected? **Yes** — 2.1.x only (RHTPA 2.1.0, 2.1.1).
- Issue scoped? **No (unscoped)** -> Case A skipped; **Case B** for affected streams.
- **2.1.x**: create remediation tasks (Cargo = source dependency -> 2 tasks: upstream backport + downstream propagation; fix not confirmed on `release/0.3.z`, so backport variant).
- **2.2.x**: **no tasks** — every 2.2.x version already ships h2 >= 0.4.8.
- Issue stays open (not Case C); no VEX justification set.

## Step 7.5 — Release Jira orchestration (2.1.x only)

Find or create, each with individual engineer confirmation:
- Release Epic `RHTPA <next 2.1.x version> Release Tasks` (e.g. `RHTPA 2.1.2 Release Tasks` — version must be confirmed by the engineer, not inferred).
- Child release Task `RHTPA <version> CVE triage`.
- 7.5.3 cross-CVE dedup: not applicable (Upstream Affected Component field not configured) -> no dedup; create tasks.

No release Jira is needed for 2.2.x.

---

## Task 1 — Upstream backport (2.1.x)

**Summary:** Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)
**Project:** TC | **Type:** Task | **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames (unbounded
header block accumulation). The vulnerable dependency (h2 < 0.4.8) must be updated
to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): v0.3.8 (2.1.0), v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: likely transitive (via hyper / HTTP client stack); confirm the
  chain with `cargo tree -i h2` — not determinable from the triage evidence
- Runtime dependency (not dev-only); priority follows CVE severity (CVSS 7.5)

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (`cargo tree -i h2`)
- Bump it to a version whose transitive closure includes h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes

**Fallback: pin the transitive dependency directly**
- `cargo update -p h2 --precise 0.4.8` (or later), or `cargo add h2@0.4.8`
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

## Task 2 — Downstream propagation (2.1.x)

**Summary:** Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
**Project:** TC | **Type:** Task | **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix
from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the next build
ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g. v0.3.12)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is
  reflected in the downstream build's Cargo.lock after the reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8004 (parent tracking issue)
```

(Coordination Guidance subsection omitted: Source Repositories table has no Deployment Context column.)

---

## Ordered Jira operations (each requires confirmation — none executed)

1. Create Task 1; post description digest comment (`[sdlc-workflow] Description digest: sha256-md:<hex>`).
2. Create Task 2; post description digest comment.
3. Link TC-8004 -> Task 1 (Depend); TC-8004 -> Task 2 (Depend).
4. Link Task 1 -> Task 2 (Blocks).
5. If release Task exists: Task 1 and Task 2 -> release Task (Blocks); release Task -> TC-8004 (Related).
6. Transition TC-8004 to In Progress; ensure assigned to current user.
7. Comment on TC-8004: "Remediation tasks created: <Task 1> (upstream backport), <Task 2> (downstream propagation, blocked by <Task 1>). Stream 2.2.x not affected — no tasks created." + footnote.
8. Add label `ai-cve-triaged` to TC-8004.
9. Post-triage summary comment: version impact table, Affects Versions correction (2.1.0, 2.2.0 -> 2.1.0, 2.1.1), outcome (remediation for 2.1.x only; 2.2.x not affected), task links, release Jira keys, no dedup, @mention of reporter (ADF mention node), Comment Footnote.

## Pre-creation checklist

- [x] Task count: 2 for 2.1.x (Cargo); 0 for unaffected 2.2.x
- [x] Cross-stream coverage: N/A (unscoped issue)
- [x] Link types: Depend (CVE->tasks), Blocks (upstream->downstream), Blocks/Related for release Jira
- [x] Preemptive labels: none (no preemptive tasks)
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: planned for 2.1.x
- [x] Dedup consistency: no dedup (field not configured)
