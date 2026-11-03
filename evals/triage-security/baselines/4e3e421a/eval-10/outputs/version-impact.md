# TC-8020 — Version Impact Analysis (Step 2) and Jira Triage (Steps 3–7)

## Step 2.1 — Supportability matrix (both streams enumerated)

| Stream | Konflux repo | Versions (backend tag) |
|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`) |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, retag of 2.2.1), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`) |

## Step 2.2 — Development stream

No unreleased Jira version data was supplied for this eval; no development stream is evaluated.

## Step 2.3 — Dependency versions (simulated `git show <tag>:Cargo.lock`)

tokio versions come from the cross-stream analysis supplied with the eval task (the matrix mock has no tokio section). Values are not invented.

## Step 2.4 — Version impact table

Version Impact for CVE-2026-55123 (tokio < 1.42.0, fixed in 1.42.0):

| Version | Stream | Backend tag | tokio | Affected? | Notes |
|---|---|---|---|---|---|
| RHTPA 2.1.0 | 2.1.x (rhtpa-2.1) | `v0.3.8` | 1.40.0 | **YES** | **outside issue scope — cross-stream** |
| RHTPA 2.1.1 | 2.1.x (rhtpa-2.1) | `v0.3.12` | 1.40.0 | **YES** | **outside issue scope — cross-stream** |
| RHTPA 2.2.0 | 2.2.x (rhtpa-2.2) | `v0.4.5` | 1.41.1 | **YES** | in scope |
| RHTPA 2.2.1 | 2.2.x (rhtpa-2.2) | `v0.4.8` | 1.41.1 | **YES** | in scope |
| RHTPA 2.2.2 | 2.2.x (rhtpa-2.2) | `v0.4.8` | — (same as 2.2.1) | YES (carried forward) | backend retag of 2.2.1; lock-file check skipped per retag rule |
| RHTPA 2.2.3 | 2.2.x (rhtpa-2.2) | `v0.4.11` | not provided | UNVERIFIED | needs `git show v0.4.11:Cargo.lock` — not assumed |
| RHTPA 2.2.4 | 2.2.x (rhtpa-2.2) | `v0.4.12` | not provided | UNVERIFIED | needs `git show v0.4.12:Cargo.lock` — not assumed |

**Cross-stream finding:** stream **rhtpa-2.1 (2.1.x)** ships tokio 1.40.0 < 1.42.0 and is affected, although TC-8020 is scoped only to rhtpa-2.2.

### Step 2.3.5 — Dependency chain context

tokio is a runtime dependency of the Rust backend (rhtpa-backend / `backend`). Direct vs transitive status requires `cargo tree -i tokio` at the pinned tags (not available in eval); task templates carry both the direct and transitive remediation approaches. Not dev-only → standard priority applies (no `dev-dependency` label).

## Step 2.5 — Upstream fix status

| Stream | Ecosystem | Upstream branch | tokio at HEAD | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | `release/0.3.z` | not provided | Not confirmed |
| 2.2.x | Cargo | `release/0.4.z` | not provided | Not confirmed |

No evidence that either upstream branch already ships tokio >= 1.42.0 → use the **upstream backport + downstream propagation** task pair (not the dependency-bump variant).

---

## Step 3 — Affects Versions correction (scoped to 2.2.x)

- Current: `[RHTPA 2.2.0, RHTPA 2.2.1]`
- Lock-file-confirmed in scope: RHTPA 2.2.0, RHTPA 2.2.1 → correct.
- RHTPA 2.2.2 is a retag of 2.2.1 (same backend source) → proposed addition, subject to engineer confirmation:
  `Current: [RHTPA 2.2.0, RHTPA 2.2.1] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- RHTPA 2.2.3 / 2.2.4: flagged for verification before final correction.
- RHTPA 2.1.0 / 2.1.1 are **not** added — they belong to stream 2.1.x (outside scope) and are handled in Case A.
- Version IDs to be discovered via `getJiraIssueTypeMetaWithFields` (no hardcoded IDs).

## Step 4 — Duplicate / sibling / overlap / reconciliation

- JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020` → **no results**.
- 4.1 Same-stream duplicates: none.
- 4.2 Cross-stream companions: **none — no CVE Jira exists for rhtpa-2.1**. No Related links to create.
- 4.3 Cross-CVE overlap: skipped (Upstream Affected Component field not configured in Security Configuration).
- 4.4 Preemptive reconciliation: no existing `security-preemptive` task for CVE-2026-55123 / rhtpa-2.2 → nothing to reconcile.

## Step 5 — Lifecycle check

Product pages not fetched (eval). No EOL evidence supplied; 2.1.x and 2.2.x treated as supported (both appear in the supportability matrix). Engineer should confirm 2.1.x is still in support before preemptive tasks are created.

## Step 6 — Already fixed check

No resolved siblings → not already fixed.

## Step 7 — Concurrent triage detection

Skipped — Upstream Affected Component custom field not configured.

## Step 7.5 — Release Jira orchestration

- 2.2.x: find/create `RHTPA <next 2.2.z> Release Tasks` Epic and `RHTPA <next 2.2.z> CVE triage` Task (version requires individual engineer confirmation; not resolvable without Jira). Standard 2.2.x remediation tasks link to the release Task (Blocks) and TC-8020 links to it (Related).
- 2.1.x: preemptive tasks are **not** linked to release Jira (release linking applies to non-preemptive remediation only).
- 7.5.3 dedup: no existing remediation task covers tokio → create tasks.

## Decision

Some supported versions affected → issue scoped to 2.2.x → other stream (2.1.x) also affected → **Case A** (cross-stream comment + preemptive tasks for 2.1.x, which has no CVE Jira) then **Case B** (standard tasks for 2.2.x).
