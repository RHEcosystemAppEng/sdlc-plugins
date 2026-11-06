# Step 2 – Version Impact Analysis: CVE-2026-31812 (TC-8001)

## 2.1 Supportability matrix (aggregated)

Both stream matrices loaded (format valid: Supportability Matrix, Source Pinning
Method, Ecosystem Mappings, Forward Pointer present). Matrix is 131 days stale — see
Step 0.3 warning in data-extraction.md.

| Stream | Konflux Release Repo | Versions | Cargo repo / lock file | Upstream Branch |
|--------|----------------------|----------|------------------------|-----------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | backend / `Cargo.lock` | `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 – 2.2.4 | backend / `Cargo.lock` | `release/0.4.z` |

## 2.2 Development stream

No Jira version metadata (unreleased RHTPA versions) was available in this eval, so
no development stream could be identified. No dev-stream row is included. In a live
run, `getJiraIssueTypeMetaWithFields` would be queried and the dev stream checked at
branch HEAD.

## 2.3 / 2.4 Version impact table

Data source: simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
output from the mock lock file data, at the pinned backend tag of each version.

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14, fixed in 0.11.14):

| Version | Stream | Backend tag (pinned) | quinn-proto | Affected? | Notes |
|---------|--------|----------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | `v0.4.8` | — | **YES** | retag of 2.2.1 — same as 2.2.1 (lock file check skipped) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | fixed version shipped |

Summary:
- **2.2.x (issue scope)**: affected in 2.2.0, 2.2.1, 2.2.2; fixed from 2.2.3 onward.
- **2.1.x (other stream)**: all released versions (2.1.0, 2.1.1) affected → Case A
  cross-stream impact.

## 2.3.5 Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn → quinn-proto   (expected path; QUIC stack)
  Type: transitive (quinn-proto is normally pulled in via the quinn crate)
  Profile: production (QUIC/HTTP3 runtime path) — not dev-only
  Present in: all released versions of 2.1.x and 2.2.x
```

Note: Cargo.toml manifests were not available in this eval, so the exact intermediate
chain (e.g., reqwest/h3 → quinn → quinn-proto) and direct/transitive classification
could not be confirmed from `git show` output. Remediation tasks therefore include
both the direct and transitive (two-tier) approaches; the implementer must confirm
via `cargo tree -i quinn-proto`.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not available (no branch-HEAD data; last tag `v0.3.12` = 0.11.9) | **Not confirmed — assume NO** |
| 2.2.x | Cargo | `release/0.4.z` | not available directly; released tags `v0.4.11`/`v0.4.12` already ship 0.11.14 | **YES (fix already on the branch since `v0.4.11`)** |

Remediation path implication:
- **2.2.x**: fix already available upstream and already shipped in 2.2.3+ →
  dependency bump variant (verify) + downstream propagation.
- **2.1.x**: fix not confirmed on `release/0.3.z` → upstream backport + downstream
  propagation (preemptive, since 2.1.x has no own CVE Jira known).

## Step 3 – Affects Versions correction (proposed, not executed)

| | Value |
|---|---|
| Current (PSIRT) | RHTPA 2.0.0 |
| Proposed (scoped to 2.2.x, lock-file evidence) | **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2** |
| Rationale | No 2.0.x stream is configured/supported; lock files show quinn-proto 0.11.9/0.11.12 in 2.2.0–2.2.2; 2.2.3 and 2.2.4 ship 0.11.14 (not affected). 2.1.x versions are outside this issue's `[rhtpa-2.2]` scope and are handled via cross-stream comment / preemptive tasks. |

Jira version IDs would be discovered dynamically via
`getJiraIssueTypeMetaWithFields`; engineer confirmation required before editing.

## Steps 4–7 (not executable in eval)

- Step 4 sibling/duplicate search (JQL `labels = CVE-2026-31812`): not run — no 2.1.x
  sibling CVE Jira is known, so 2.1.x tasks are treated as preemptive.
- Step 4.3 / Step 7: skipped — Upstream Affected Component field not configured.
- Step 5 lifecycle: not checked (no external access); assume 2.1.x and 2.2.x supported.
- Step 6 already-fixed: no resolved siblings known. Note that 2.2.3+ already ships the fix.
- Step 7.5 release Jira: not resolved in eval; tasks would additionally be linked
  (Blocks) to the release Task and CVE linked (Related) when available.

Awaiting engineer confirmation of this table before Step 3 (simulated: confirmed).
