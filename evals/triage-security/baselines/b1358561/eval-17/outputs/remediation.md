# Step 8 – Remediation: CVE-2026-31812 (TC-8001)

These are proposed actions only. No Jira calls were made. Every mutation below needs
explicit engineer confirmation, and the Step 1.7 embargo gate must have been answered
"Yes" first.

## Inputs carried forward

| Item | Value |
|------|-------|
| Issue scope | 2.2.x (scoped, suffix `[rhtpa-2.2]`) |
| Ecosystem | Cargo, a source dependency (2 tasks per affected stream) |
| Affected in scope (2.2.x) | 2.2.0, 2.2.1, 2.2.2. **Already fixed in 2.2.3 and 2.2.4** (quinn-proto 0.11.14) |
| Affected out of scope (2.1.x) | 2.1.0, 2.1.1 (quinn-proto 0.11.9). No fixed release yet. |
| Development stream | Undetermined (no Jira/repo access) |
| Deployment context | `upstream` (default). No Deployment Context column, so Coordination Guidance is omitted. |
| Security level | Copy TC-8001's security level onto every created Task (read it at creation time; it is not in the mock data) |

## Steps 4–7 (status in this eval)

- **Step 4 (siblings/duplicates)**: the JQL `project = TC AND labels = 'CVE-2026-31812' AND
  issuetype = 10024 AND key != TC-8001` could not be run. This plan **assumes no sibling
  exists**: no same-stream duplicate and no 2.1.x companion. If a 2.1.x companion issue
  exists, skip the 2.1.x preemptive tasks below and add a Related link to that issue
  instead. Step 4.3 (cross-CVE overlap) is skipped because Upstream Affected Component is
  not configured.
- **Step 5 (lifecycle)**: the product pages URL was not fetched. The engineer must
  confirm that 2.1.x is still supported before the 2.1.x tasks are created. If 2.1.x is
  EOL, drop those tasks.
- **Step 6 (already fixed)**: there are no resolved siblings to check. Note that the
  in-scope stream already ships the fix in 2.2.3 (lock-file evidence).
- **Step 7 (concurrent triage)**: skipped, because Upstream Affected Component is not
  configured.
- **Step 7.5 (release Jira)**: search for or propose `RHTPA <version> Release Tasks`
  (Epic) and `RHTPA <version> CVE triage` (Task). Each creation needs individual
  confirmation. Preemptive tasks are not linked to release Jira.

## Decision

The issue is scoped and other streams are affected, so this is **Case A
(cross-stream) followed by Case B**.

### 2.2.x (in scope): no new remediation tasks are proposed

The latest shipped 2.2.x releases (2.2.3 at `v0.4.11` and 2.2.4 at `v0.4.12`) already
contain quinn-proto 0.11.14. A dependency bump plus downstream propagation pair for
2.2.x would change nothing. Recommendation:

- Keep TC-8001 open with Affects Versions corrected to RHTPA 2.2.0, 2.2.1, and 2.2.2.
- Record in the summary comment that the fix shipped in RHTPA 2.2.3. The remediation
  for affected users is to upgrade to 2.2.3 or later.
- Let the engineer or ProdSec decide the issue's final disposition (for example,
  transition per the fixed-in-release workflow).
- **Override option:** if the engineer still wants Case B tasks for 2.2.x (for example
  because the dev branch HEAD turns out to be affected), use the dependency-bump variant
  on `release/0.4.z` plus downstream propagation in `rhtpa-release.0.4.z`. The format is
  the same as below, with Depend links to TC-8001.

### 2.1.x (out of scope): Case A cross-stream comment and preemptive tasks

**Cross-stream impact comment on TC-8001:**

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s)
2.1.x (RHTPA 2.1.0, RHTPA 2.1.1 — quinn-proto 0.11.9 at v0.3.8 / v0.3.12)
based on lock file analysis.
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

Upstream fix status on `release/0.3.z` is **not confirmed**, so the **upstream backport**
template is used. If the engineer confirms `release/0.3.z` HEAD already has quinn-proto
0.11.14 or later, switch Task 1 to the dependency-bump variant.

---

#### Task 1: Upstream backport (2.1.x, preemptive)

- **Summary**: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)`
- **Issue type**: Task
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Security**: same level as TC-8001
- **Link**: TC-8001 (inward) to this task (outward), type **Related** (preemptive, not Depend)

```
## Repository

backend (rhtpa-backend)

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panics when a remote peer sends a QUIC
STREAMS frame requesting an excessive number of streams (denial of service).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (quinn-proto 0.11.9), RHTPA 2.1.1 (quinn-proto 0.11.9)
Source commit(s): backend v0.3.8 (2.1.0), backend v0.3.12 (2.1.1)

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: not determined during triage (only lock-file versions were
  available). Confirm with `cargo tree -i quinn-proto`; quinn-proto is commonly
  transitive via `quinn`.
- If the vulnerable dependency is dev-only or build-only (identified
  in Step 2.3.5), the remediation priority is Normal regardless of CVE
  severity. Add `dev-dependency` label to the task.

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When the vulnerable package is a **transitive** dependency (pulled in
through intermediate packages), use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in quinn-proto (see dependency
  chain above)
- Bump the direct dependency to a version whose transitive closure
  includes quinn-proto >= 0.11.14
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable (breaking API changes,
no release available with the fix):
- Cargo: `cargo add quinn-proto@0.11.14` to add as a direct
  dependency, overriding the transitive resolution
- Document why the direct dep bump was not viable in the PR description

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)
```

After creation, post the description digest comment
(`[sdlc-workflow] Description digest: <tagged-digest>`) **before** any links or other
comments.

---

#### Task 2: Downstream propagation (2.1.x, preemptive)

- **Summary**: `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)`
- **Issue type**: Task
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`
- **Security**: same level as TC-8001
- **Links**: TC-8001 to this task, type **Related**. Task 1 (inward) blocks this task
  (outward), type **Blocks**.

```
## Repository

rhtpa-release.0.3.z (git.example.com/rhtpa/rhtpa-release.0.3.z)

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from <Task 1 key>.

The upstream backport (<Task 1 key>) bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: backend is pinned in `artifacts.lock.yaml` (download URL
  contains the tag, currently `v0.3.12`)
- **Dependency type**: carried forward from <Task 1 key> (to be confirmed there)
- Update the rhtpa-backend reference to the merged commit or new release tag
- If the upstream fix pinned a transitive dependency directly (fallback
  approach), verify the pinning is reflected in the downstream build's
  lock file after the source reference update
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: <Task 1 key> (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)
```

After creation, post the description digest comment before any links or other comments.

---

## Follow-up comments on TC-8001 (after the task links)

**Preemptive task list:**

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <Task 1 key> (upstream backport, security-preemptive)
- 2.1.x: <Task 2 key> (downstream propagation, blocked by <Task 1 key>, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.

<Comment Footnote per shared/comment-footnote.md, skill: triage-security>
```

## Post-triage summary (proposed)

1. Add the label `ai-cve-triaged` to TC-8001.
2. Post a summary comment containing:
   - the version impact table (from version-impact.md)
   - the Affects Versions correction: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - the outcome: 2.2.x was already fixed in RHTPA 2.2.3 (no new 2.2.x tasks); 2.1.x
     affected, with preemptive tasks <Task 1 key> and <Task 2 key>
   - release Jira references (if created in Step 7.5); no dedup results
   - an ADF @mention of the TC-8001 reporter (account ID taken from the issue at runtime)
   - the Comment Footnote (skill `triage-security`)

## Pre-creation checklist

- [x] Task count per stream: 2.1.x has 2 tasks (Cargo is a source dependency). 2.2.x has
      0 new tasks because the fix already shipped, and this is flagged for engineer override.
- [x] Cross-stream coverage: 2.1.x is covered by preemptive tasks, assuming no sibling
      CVE Jira exists (Step 4 could not be run).
- [x] Link types: Related (preemptive to TC-8001), Blocks (upstream to downstream).
      No Depend links, because no non-preemptive tasks are proposed.
- [x] Preemptive labels: `security-preemptive` on both 2.1.x tasks.
- [x] Coordination guidance: omitted, because the Deployment Context column is absent.
- [x] Release Jira linking: no non-preemptive tasks, so nothing to link with Blocks.
      Link TC-8001 to the release Task (Related) if Step 7.5 created one.
- [x] Dedup consistency: not applicable (Step 7.5.3 found no dedup without the
      component field).
