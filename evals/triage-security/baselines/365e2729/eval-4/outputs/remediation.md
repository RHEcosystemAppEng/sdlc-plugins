# TC-8004 — Steps 7, 7.5, 8: Remediation

## Decision

| Check | Result |
|---|---|
| Step 7 – Concurrent triage | Skipped (Upstream Affected Component field not configured) |
| Any supported versions affected? | **Yes**: RHTPA 2.1.0, 2.1.1 (stream 2.1.x) |
| Issue scoped to a single stream? | **No (unscoped)** |
| Case A (cross-stream notice / preemptive tasks) | **Not applicable.** Unscoped issues cover all streams, so no preemptive tasks and no `security-preemptive` label |
| Outcome | **Case B: create remediation tasks for affected streams only** |
| Affected streams | **2.1.x** (create tasks) |
| Unaffected streams | **2.2.x** (no tasks: every 2.2.x version ships h2 >= 0.4.8) |
| Ecosystem | Cargo (source dependency), so **2 tasks** for 2.1.x |
| Upstream fix on `release/0.3.z` | Not confirmed, so **upstream backport + downstream propagation** |
| Dev-dependency handling | Not applicable (h2 assumed production runtime; confirm in Step 2.3.5) |
| Coordination guidance | Omitted (Source Repositories table has no Deployment Context column) |

**Total tasks to create: 2 (both for stream 2.1.x). Zero tasks for 2.2.x.**

## Step 7.5 – Release Jira Orchestration (stream 2.1.x only)

- 7.5.1: Resolve the next 2.1.x release version from the supportability matrix and unreleased Jira versions. The matrix's latest 2.1.x is 2.1.1, so the next is likely RHTPA 2.1.2, but the **engineer must confirm** because the version is not inferred automatically. Then find or create the Epic `"RHTPA <version> Release Tasks"`, which needs individual confirmation.
- 7.5.2: Find or create the child Task `"RHTPA <version> CVE triage"`, which needs individual confirmation.
- 7.5.3: Cross-CVE dedup is skipped (Upstream Affected Component not configured), so no dedup applies.
- No release Jira is created for 2.2.x because that stream is not affected.

---

## Task 1 — Upstream backport (2.1.x)

**Summary:** `Remediate CVE-2026-33501: bump h2 to 0.4.8 (2.1.x)`
**Issue type:** Task | **Project:** TC
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`
**Security level:** copied from TC-8004's `security` field (omitted only if null)

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-33501: h2 memory exhaustion via CONTINUATION frames. A peer can
send an unbounded sequence of CONTINUATION frames after a HEADERS frame; h2 accumulates
the header block without a size limit, allowing unbounded memory consumption (CVSS 7.5).
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: RHTPA 2.1.0 (h2 0.4.5), RHTPA 2.1.1 (h2 0.4.5)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/hyperium/h2/pull/812
Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: to be confirmed. Run `cargo tree -i h2` on release/0.3.z; h2 is
  typically transitive (e.g., via hyper / reqwest / tonic).
- If the vulnerable dependency is dev-only or build-only, the remediation priority is
  Normal regardless of CVE severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if declared directly)
- If a direct bump introduces breaking changes, assess whether a code-level workaround
  is viable (see upstream changelog)

### Remediation approach (transitive dependency)

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (`cargo tree -i h2`)
- Bump the direct dependency (or run `cargo update -p h2` if semver-compatible) so the
  transitive closure includes h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes to the direct dependency

**Fallback: pin the transitive dependency directly**
- Cargo: `cargo add h2@0.4.8` to add as a direct dependency, overriding the transitive
  resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8 in Cargo.lock on release/0.3.z
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8004 (parent tracking issue)
```

---

## Task 2 — Downstream propagation (2.1.x)

**Summary:** `Propagate CVE-2026-33501 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)`
**Issue type:** Task | **Project:** TC
**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-33501`
**Security level:** copied from TC-8004's `security` field (omitted only if null)

```
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-33501 fix
from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps h2 to 0.4.8 on release/0.3.z. Once that PR
merges, update the source pinning in this Konflux release repo so the next build ships
the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- **Dependency type**: carried forward from upstream task (to be confirmed there)
- Update the backend reference to the merged commit or new release tag
- If the upstream fix pinned h2 directly (fallback approach), verify the pinning is
  reflected in the downstream build's Cargo.lock after the source reference update
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

---

## Creation and Linkage Sequence (proposed; requires engineer confirmation; NOT executed)

1. Create Task 1, then post the description digest comment `[sdlc-workflow] Description digest: <sha256-...>` before any links.
2. Create Task 2, then post its description digest comment.
3. Link `TC-8004` to Task 1 (**Depend**).
4. Link `TC-8004` to Task 2 (**Depend**).
5. Link Task 1 to Task 2 (**Blocks**: upstream blocks downstream).
6. If release Jira is active: Task 1 and Task 2 to the 2.1.x release Task (**Blocks**); release Task to TC-8004 (**Related**).
7. Transition TC-8004 to In Progress if it is not already in an in-progress or later status. Make sure it is assigned to the current user.
8. Comment on TC-8004: "Remediation tasks created: <Task 1 key> (upstream backport), <Task 2 key> (downstream propagation, blocked by <Task 1 key>)" + Comment Footnote.

## Pre-creation Checklist

- [x] Task count per stream: 2.1.x gets 2 (Cargo, source dependency); 2.2.x gets 0 (not affected)
- [x] Cross-stream coverage: not applicable (unscoped issue; Case A skipped)
- [x] Link types: Depend (tasks to own CVE), Blocks (upstream to downstream); no Related/preemptive links
- [x] Preemptive labels: none (no `security-preemptive`)
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking: planned for 2.1.x only, pending release version confirmation
- [x] Dedup consistency: no dedup (Step 7.5.3 skipped)

## Post-Triage Summary (proposed)

- Add label `ai-cve-triaged` to TC-8004.
- Post a summary comment covering: the version impact table (2.1.x affected; 2.2.x not affected), the Affects Versions correction `[RHTPA 2.1.0, RHTPA 2.2.0] → [RHTPA 2.1.0, RHTPA 2.1.1]`, outcome Case B with 2 remediation tasks for 2.1.x and none for 2.2.x, the task keys, release Epic/Task keys, a dedup result of none, an ADF @mention of the TC-8004 reporter, and the Comment Footnote ("This comment was AI-generated by sdlc-workflow/triage-security v0.14.0.").

## Caveats for Live Run

- The matrix is 151 days stale, so refresh it before acting. A newer 2.1.x release may exist.
- The development stream and upstream `release/0.3.z` HEAD were not checked.
- MITRE/OSV cross-validation and the product lifecycle check were not performed.
- The due date (2026-08-01) has already passed.
