# TC-8050 — Step 8 Remediation

## Decision

- Supported versions affected: **YES**. 2.2.0 through 2.2.4 all ship criterion 0.5.1 (< 0.5.2) in the lock file.
- Dependency scope: **dev-only** (`[dev-dependencies]`, not shipped in production). Per the dependency scope decision tree, tasks are still created with the **`dev-dependency` label** and **priority overridden to Normal**.
- Issue is scoped (2.2.x), and another stream (2.1.x) is also affected. This gives **Case A** (cross-stream comment, plus preemptive tasks for 2.1.x if it has no CVE Jira of its own) followed by **Case B** for 2.2.x.
- Ecosystem: Cargo (source dependency), so 2 tasks per stream. The upstream fix is not confirmed, so the tasks are an upstream backport and a downstream propagation.
- Priority: **Normal**. This overrides the CVE severity (CVSS 5.3 Medium). The CVE priority is NOT inherited because the dependency is dev-only.

Nothing below was created in Jira. Each item is a proposal that would go through the engineer confirmation gate.

---

## Task 1 — Upstream backport (2.2.x)

- **Summary:** Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)
- **Issue type:** Task
- **Project:** TC
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** Normal (dev-only dependency override; CVE severity not inherited)
- **Links:** TC-8050 → this task (Depend); this task → Task 2 (Blocks); this task → RHTPA 2.2.5 CVE triage release Task (Blocks)

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: criterion path traversal in benchmark output — crafted
benchmark names containing path separators allow writing benchmark output files
to arbitrary paths. The vulnerable dependency (criterion < 0.5.2) must be updated
to the fixed version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12 (backend tags from the supportability matrix)

Upstream fix: none listed in remote links
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (chain: backend (workspace) → criterion, declared in
  [dev-dependencies] of backend/Cargo.toml)
- **Dependency scope**: dev-only — used for benchmarks only; NOT present in
  production builds or container images. Priority is Normal regardless of CVE
  severity; `dev-dependency` label applied.
- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml
  ([dev-dependencies] criterion = "0.5.1" → "0.5.2") and Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog); benchmarks may need adjustment

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency
- [ ] Benchmarks (`cargo bench --no-run`) still compile

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

---

## Task 2 — Downstream propagation (2.2.x)

- **Summary:** Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)
- **Issue type:** Task
- **Project:** TC
- **Labels:** `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`
- **Priority:** Normal (dev-only dependency override)
- **Links:** TC-8050 → this task (Depend); Task 1 blocks this task; this task → RHTPA 2.2.5 CVE triage release Task (Blocks)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the CVE-2026-99001
fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps criterion to 0.5.2 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build ships the fix.

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct (dev-only) — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Note: because criterion is a dev-dependency, the shipped container image
  contents are not expected to change for criterion itself; this update keeps
  the source reference aligned with the remediated upstream lock file
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)
```

---

## Case A — Cross-stream impact (2.1.x)

Proposed comment on TC-8050:

```
Cross-stream impact: criterion < 0.5.2 also affects stream(s) 2.1.x
(2.1.0, 2.1.1 ship criterion 0.5.1 as a [dev-dependencies] entry) based on lock
file analysis. These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by sdlc-workflow/triage-security.
```

If the Step 4 sibling search finds no 2.1.x CVE Jira for CVE-2026-99001, create **preemptive** tasks for 2.1.x. They use the same templates as above with these changes:
- Target branch `release/0.3.z`, Konflux repo `rhtpa-release.0.3.z`, affected versions 2.1.0 and 2.1.1 (tags v0.3.8, v0.3.12)
- Labels: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `security-preemptive`, `dev-dependency`
- Priority: Normal (dev-only override)
- Link to TC-8050 as **Related** (not Depend). Preemptive tasks are not linked to the 2.2.x release Task.
- Description prefix: "> **Preemptive remediation**: This task was created proactively from cross-stream impact analysis of TC-8050 (stream 2.2.x). No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one, this task will be linked and the `security-preemptive` label removed."

If a 2.1.x sibling CVE Jira exists, skip creating tasks for 2.1.x.

---

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo source dependency)
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks or uses its existing sibling
- [x] Link types: Depend (own CVE), Related (preemptive), Blocks (upstream → downstream and → release Task)
- [x] Preemptive labels applied to 2.1.x tasks only
- [x] Coordination guidance: omitted because Source Repositories has no Deployment Context column
- [x] Release Jira linking: 2.2.x tasks Block the release Task; TC-8050 is Related to the release Task
- [x] Dedup: not applicable (Step 7.5.3 requires Upstream Affected Component, which is not configured)
- [x] Dev-only handling: `dev-dependency` label on all tasks; priority Normal; scope note in each description

## Post-triage (proposed)

- Add the `ai-cve-triaged` label to TC-8050.
- Summary comment containing the version impact table, the Affects Versions correction (2.2.0 → 2.2.0 through 2.2.4), the outcome (remediation created at Normal priority because the dependency is dev-only), task keys, release Jira keys, an @mention of the reporter, and the Comment Footnote.
- Each created task gets a description digest comment before any of its links.
