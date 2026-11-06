# TC-8001: Step 2 Version Impact Analysis

## 2.1: Supportability matrix (aggregated)

Both matrices were loaded from the mock (`security-matrix-mock.md`). Format check:
all required sections are present (Supportability Matrix, Source Pinning Method,
Ecosystem Mappings, Forward Pointer). The Ecosystem Mappings columns match the
template (`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`).
Result: **Pass**.

| Stream | Version | Build | Build Date | backend tag | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | |
| 2.1.x | 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | |
| 2.2.x | 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.x | 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.x | 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.x | 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## 2.2: Development stream

The Jira call `getJiraIssueTypeMetaWithFields(TC, 10024)` was not made, so the list
of unreleased RHTPA versions is not available. Neither matrix lists a stream past
2.2.x, and the 2.2.x forward pointer says it is the latest stream. **No separate
development-stream row is included.** If Jira reports an unreleased RHTPA version
(e.g. RHTPA 2.2.5 or 3.0), it must be checked at `release/0.4.z` / `main` HEAD
before Affects Versions are finalized.

## 2.3: Dependency versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`)

The values come from the mock's "quinn-proto versions by tag" table, standing in
for real `git show` output. The retag v0.4.9 was not checked; its result is
carried forward from v0.4.8.

## 2.4: Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | backend tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | **YES** | Outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | **YES** | Outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | **YES** | In scope |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | **YES** | In scope |
| 2.2.2 | 2.2.x | v0.4.8 | — | **YES** | Same as 2.2.1 (backend retag of 2.2.1; lock file not re-checked) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | Fixed version shipped |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | Fixed version shipped |

Summary:
- **In-scope stream 2.2.x**: 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and 2.2.4 are not, because the fix arrived in backend v0.4.11.
- **Out-of-scope stream 2.1.x**: 2.1.0 and 2.1.1 are affected and every release ships 0.11.9. This triggers Case A (cross-stream impact).
- PSIRT's Affects Versions value **RHTPA 2.0.0 is wrong**. No 2.0.x stream exists in the supportability matrix.

### 2.3.5: Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn-proto
  Type: NOT DETERMINED. The eval data has no Cargo.toml / full Cargo.lock
        dependency graph. quinn-proto is usually pulled in transitively
        through the `quinn` crate (QUIC/HTTP3 support, e.g. via reqwest/h3).
        Confirm with `git show <tag>:Cargo.lock` (look at the
        `dependencies = [...]` arrays that reference quinn-proto) and
        `git show <tag>:Cargo.toml` before task execution.
  Profile: assumed production (a QUIC transport crate is a runtime dependency).
           No evidence of a [dev-dependencies]/[build-dependencies] scope, so
           no `dev-dependency` label and no priority override.
  Introduction point: present in every checked tag (v0.3.8 through v0.4.12).
  Version progression: 0.11.9 (2.1.0–2.2.0) → 0.11.12 (2.2.1/2.2.2) → 0.11.14 (2.2.3+)
```

Remediation path: if the dependency is transitive, bump the direct dependency
(probably `quinn`) to a release whose closure resolves quinn-proto >= 0.11.14.
Otherwise run `cargo update -p quinn-proto` or pin with
`cargo add quinn-proto@0.11.14`. Within the 0.11.x line,
`cargo update -p quinn-proto --precise 0.11.14` should resolve without
a semver-breaking change.

## 2.5: Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.1.x | Cargo | backend | release/0.3.z | Not available (no HEAD data in mock; last tag v0.3.12 = 0.11.9) | **Treated as NOT fixed.** Needs `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock` verification |
| 2.2.x | Cargo | backend | release/0.4.z | Not read directly; the latest release tag from this branch (v0.4.12) ships 0.11.14 | **YES**, fixed since v0.4.11 |

Effect on remediation:
- **2.2.x**: the fix is already upstream and **already shipped in RHTPA 2.2.3 and 2.2.4**. The Konflux repo `rhtpa-release.0.4.z` already pins v0.4.12, so the remediation is the dependency bump variant (verify release/0.4.z HEAD stays at 0.11.14 or higher) plus downstream propagation (verify or refresh the pin). Customers on 2.2.0–2.2.2 are fixed by upgrading to 2.2.3 or later.
- **2.1.x**: not fixed upstream, so it needs an upstream backport on `release/0.3.z` followed by downstream propagation in `rhtpa-release.0.3.z`.

Simulated engineer confirmation: version impact table accepted.

---

## Steps 3–7.5: Jira triage operations (planned, not executed)

### Step 3: Affects Versions correction (scoped to 2.2.x)

Step 3.1 version discovery (`getJiraIssueTypeMetaWithFields`) was not executed.
Version IDs are resolved at runtime and never hardcoded.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

- RHTPA 2.0.0 is removed: there is no 2.0.x stream, so PSIRT's value is wrong.
- 2.1.0 and 2.1.1 are left out because they are outside this issue's `[rhtpa-2.2]` scope and belong to a companion or preemptive tracker.
- 2.2.3 and 2.2.4 are left out because they are not affected.
- If a 2.2.x version is missing from Jira, flag it to the project admin and continue.

Planned comment (with Comment Footnote; no ProdSec @mention because none is configured):
> Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
> Based on lock file analysis at pinned commits from security-matrix.md.
> Scoped to stream 2.2.x per issue suffix.
> ---
> This comment was AI-generated by sdlc-workflow/triage-security v0.13.10.

### Step 4: Duplicate, sibling, overlap and reconciliation

- JQL: `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001`. Simulated result: **no siblings** (no sibling data provided).
  - 4.1: no same-stream duplicate.
  - 4.2: no 2.1.x companion tracker exists, so 2.1.x gets preemptive tasks in Case A.
- 4.3 cross-CVE overlap: **skipped** (Upstream Affected Component / PS Component / Stream fields are not configured).
- 4.4 preemptive reconciliation: JQL `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812'`. Simulated result: none, so new tasks are created in Step 8.

### Step 5: Lifecycle check

The Product pages fetch (`https://access.example.com/product-life-cycle/rhtpa`) was
not executed. 2.1.x and 2.2.x are assumed to be supported, since both are listed in
Version Streams. Confirm before task creation.

### Step 6: Already-fixed check

No resolved siblings exist, so the issue proceeds to Step 8. Within the stream, the
affected versions (2.2.0–2.2.2) are superseded by 2.2.3, which already ships the fix.

### Step 7: Concurrent triage detection

Skipped. The Upstream Affected Component field is not configured.

### Step 7.5: Release Jira orchestration (2.2.x, non-preemptive tasks only)

- 7.5.1: JQL `project = TC AND issuetype = Epic AND summary ~ 'RHTPA 2.2' AND summary ~ 'Release Tasks' ORDER BY created DESC`. Simulated result: none found. The proposed version is the latest matrix release 2.2.4 plus one patch, giving **"RHTPA 2.2.5 Release Tasks"**. This needs individual engineer confirmation, then a description digest comment.
- 7.5.2: create **"RHTPA 2.2.5 CVE triage"** as a child of the Epic (individual confirmation, then digest comment). Referred to below as `<release-task-key>`.
- 7.5.3 dedup: **skipped** (Upstream Affected Component field is not configured).
- 2.1.x: its tasks are preemptive, so they are not linked to release Jira.
