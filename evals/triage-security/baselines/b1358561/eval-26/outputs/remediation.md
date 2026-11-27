# TC-8050 — Step 8 Remediation

## Decision

- Affected versions exist in the issue scope: 2.2.0, 2.2.1, 2.2.2 (retag), 2.2.3 and 2.2.4 all ship criterion 0.5.1, which is below 0.5.2.
- The issue is **scoped** (`[rhtpa-2.2]`), and another stream (2.1.x) is also affected. That gives **Case A** (cross-stream comment, plus preemptive 2.1.x tasks if no sibling CVE Jira exists) followed by **Case B** (remediation tasks for 2.2.x).
- Ecosystem: **Cargo**, a source dependency, so **2 tasks per stream**.
- Upstream fix on `release/0.4.z` is **not confirmed** (see version-impact.md, Step 2.5), so the templates are **upstream backport + downstream propagation**.
- Dependency scope: criterion is a **direct `[dev-dependencies]` entry** and is not shipped in production. Per the dependency scope decision tree:
  - Label **`dev-dependency`** is added to every remediation task.
  - Priority is set to **Normal**, overriding the CVE's priority. The Medium (CVSS 5.3) CVE priority is **not** inherited.
  - The dev-only note is included in each task description.
- Not Case C. The vulnerable version is in the lock file of every version, so closing as Not a Bug / VEX does not apply. Feature-gated VEX handling does not apply either.
- Coordination Guidance is omitted because the Source Repositories table has no Deployment Context column.
- Security level: copy TC-8050's `security` level onto every created Task. The fixture does not show one; omit it only if the parent truly has none.

Nothing below has been created. Every item needs engineer confirmation.

---

## Task 1 — Upstream backport (2.2.x)

- **Project**: TC
- **Issue type**: Task
- **Summary**: `Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.2.x)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, **`dev-dependency`**
- **Priority**: **Normal** (dev-only dependency override; CVE severity not inherited)
- **Security**: parent TC-8050 security level
- **Links**: TC-8050 → Depend → this task; this task → Blocks → Task 2; this task → Blocks → release Task (`RHTPA <2.2.x next> CVE triage`, if Step 7.5 is active)

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: criterion path traversal in benchmark output — crafted
benchmark names containing path separators allow writing benchmark output files
to arbitrary paths.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4
(all ship criterion 0.5.1)
Source commit(s): v0.4.5, v0.4.8, v0.4.11, v0.4.12 (backend tags from the
supportability matrix)

Upstream fix: none listed in remote links
Advisory: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (chain: backend (workspace) → criterion), declared
  in `[dev-dependencies]` of backend/Cargo.toml (`criterion = "0.5.1"`). Used for
  benchmarks only; NOT present in production builds.
- The vulnerable dependency is dev-only (identified in Step 2.3.5), so the
  remediation priority is Normal regardless of CVE severity, and the task
  carries the `dev-dependency` label.

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml
  `[dev-dependencies]` and refresh Cargo.lock (e.g., `cargo update -p criterion`)
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency
- [ ] Benchmarks (`cargo bench --no-run`) still compile with the updated criterion

## Dependencies

- Depends on: TC-8050 (parent tracking issue)
```

After creation, post the description digest comment (`[sdlc-workflow] Description digest: <tagged-digest>`) before any links.

---

## Task 2 — Downstream propagation (2.2.x)

- **Project**: TC
- **Issue type**: Task
- **Summary**: `Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.4.z (2.2.x)`
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, **`dev-dependency`**
- **Priority**: **Normal** (dev-only dependency override)
- **Security**: parent TC-8050 security level
- **Links**: TC-8050 → Depend → this task; blocked by Task 1 (Blocks); this task → Blocks → release Task (if active)

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps criterion to 0.5.2 on release/0.4.z.
Once that PR merges, update the source pinning in this Konflux release repo so
the next build reflects the fix.

This dependency is dev/build-only and is not shipped in production. Remediation
priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.4.12)
- **Dependency type**: direct (dev-only, `[dev-dependencies]`) — carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
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

After creation, post the description digest comment before any links.

---

## Case A — Preemptive tasks for 2.1.x (only if no `[rhtpa-2.1]` sibling CVE Jira exists)

The Step 4 sibling search could not run (no Jira access). If it confirms that no 2.1.x CVE Jira exists for CVE-2026-99001, create the same two-task pair for 2.1.x with these changes:

| Field | Task 3 (upstream backport, 2.1.x) | Task 4 (downstream propagation, 2.1.x) |
|-------|-----------------------------------|----------------------------------------|
| Summary | `Remediate CVE-2026-99001: bump criterion to 0.5.2 (2.1.x)` | `Propagate CVE-2026-99001 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)` |
| Repository / branch | backend, `release/0.3.z` | rhtpa-release.0.3.z, `main` |
| Labels | `ai-generated-jira`, `Security`, `CVE-2026-99001`, **`dev-dependency`**, `security-preemptive` | same |
| Priority | **Normal** (dev-only override) | **Normal** |
| Affected versions | RHTPA 2.1.0, 2.1.1 (criterion 0.5.1; tags v0.3.8, v0.3.12) | — |
| Link to TC-8050 | **Related** (not Depend) | **Related** |
| Release Jira link | none (preemptive tasks are not linked to release Jira) | none |

Description prefix for both:

```
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8050 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for this stream. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.
```

Both preemptive descriptions also carry the dev-only note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

---

## Proposed Jira operations (in order, each requires confirmation)

1. Assign TC-8050 to the current user and transition New → Assigned (Step 0.8).
2. Affects Versions: RHTPA 2.2.0 becomes RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 (Step 3), with a correction comment and footnote.
3. Find or create the release Epic/Task for the next 2.2.x release (Step 7.5, individual confirmation; version chosen by the engineer).
4. Create Task 1, then post its digest. Create Task 2, then post its digest.
5. Links: TC-8050 Depend Task 1; TC-8050 Depend Task 2; Task 1 Blocks Task 2; Task 1 and Task 2 Block the release Task; release Task Related TC-8050.
6. Post the cross-stream impact comment (2.1.x) and, if applicable, create preemptive Tasks 3 and 4 (Related links) and post a preemptive task list comment.
7. TC-8050 is already Assigned, so the In Progress transition is skipped as equivalent.
8. Add the `ai-cve-triaged` label. Post the summary comment: version impact table, Affects Versions correction, outcome "remediation created (dev-only dependency, Normal priority)", task keys, release Jira keys, an @mention of the reporter, and the footnote "This comment was AI-generated by sdlc-workflow/triage-security v0.14.0."

## Pre-creation checklist

- [x] Task count per stream: 2 (Cargo is a source dependency)
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks, or is handled by its sibling CVE Jira
- [x] Link types: Depend (own CVE), Related (preemptive), Blocks (upstream → downstream, remediation → release Task)
- [x] Preemptive label on 2.1.x tasks
- [x] Coordination guidance: omitted (no Deployment Context column)
- [x] Release Jira linking for non-preemptive tasks
- [x] Dedup consistency: N/A (Step 7.5.3 cannot run without the Upstream Affected Component field)
- [x] Dev-only handling: `dev-dependency` label + Normal priority + dev-only note on every task
