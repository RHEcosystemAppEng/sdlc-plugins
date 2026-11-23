# TC-8001 — Step 2: Version Impact Analysis

Evidence: simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
output, taken from the "quinn-proto versions by tag" table in security-matrix-mock.md.
Fix threshold: quinn-proto < 0.11.14 (Jira description; external enrichment unavailable).

## 2.1 Supportability matrix (both streams enumerated from the Version Streams table)

- 2.1.x (rhtpa-release.0.3.z): 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`)
- 2.2.x (rhtpa-release.0.4.z): 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (`v0.4.8`, a backend retag
  of 2.2.1), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`)
- Format validation: both matrices contain Supportability Matrix, Source Pinning Method,
  Ecosystem Mappings (correct 5 columns) and Forward Pointer. Result: pass.

## 2.2 Development stream

No Jira version metadata is available in this eval (`getJiraIssueTypeMetaWithFields`
was not called), and no stream beyond 2.2.x is configured. No development stream
was identified, so no branch HEAD row is included.

## 2.4 Version impact table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Backend pinned tag | quinn-proto | Affected? | Notes |
|--------|---------|--------------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8`  | 0.11.9  | **YES** | outside issue scope (cross-stream) |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.11.9  | **YES** | outside issue scope (cross-stream) |
| 2.2.x | 2.2.0 | `v0.4.5`  | 0.11.9  | **YES** | in scope |
| 2.2.x | 2.2.1 | `v0.4.8`  | 0.11.12 | **YES** | in scope |
| 2.2.x | 2.2.2 | `v0.4.8`  | —       | **YES** | same as 2.2.1 (backend retag; lock file check skipped, result carried forward) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.11.14 | NO | fixed version shipped |

Summary:
- **In scope (2.2.x):** 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and later already ship the fix.
- **Cross-stream (2.1.x):** every released version (2.1.0, 2.1.1) is affected and no 2.1.x
  release has the fix.
- PSIRT Affects Versions `RHTPA 2.0.0` is **wrong**. 2.0.x is not a configured stream and no
  lock file evidence supports it.

## 2.3.5 Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ? → quinn-proto
  Type: NOT DETERMINED — Cargo.toml / full Cargo.lock dependency graph was not
        part of the provided evidence (only version-by-tag data). quinn-proto is
        normally pulled in transitively (e.g., via quinn / an HTTP/3 client), but
        that must be confirmed from the manifests before task creation.
  Profile: assumed production (no evidence of dev/build-only scope); confirm.
  Introduction point: present in all inspected tags (v0.3.8 onward).
```

Remediation tasks therefore include both the direct-bump and transitive two-tier approaches,
and the implementer confirms which one applies.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | not available in evidence (latest tag `v0.3.12` = 0.11.9) | **NO / unverified**, treated as not fixed |
| 2.2.x | Cargo | `release/0.4.z` | not directly read; latest tags `v0.4.11`/`v0.4.12` from this branch ship 0.11.14 | **YES** (inferred from latest pinned tags) |

Effect on remediation:
- 2.2.x: fixed upstream, so the **dependency bump variant** applies (the upstream fix is already
  shipped in 2.2.3/2.2.4).
- 2.1.x: not fixed upstream, so the **upstream backport + downstream propagation** variant applies.

Wait for the engineer to confirm this table before Step 3.

## Steps 3–7 (summary of planned Jira operations, none executed)

- **Step 3 — Affects Versions correction (scoped to 2.2.x):** discover versions via
  `getJiraIssueTypeMetaWithFields` (issue type 10024). Replace `RHTPA 2.0.0` with
  **`RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`**, after engineer confirmation. Post a
  correction comment with the Comment Footnote (sdlc-workflow/triage-security v0.14.0).
- **Step 4 — Duplicates/siblings:** JQL `project = TC AND issuetype = 10024 AND labels =
  CVE-2026-31812 AND key != TC-8001`. The eval provides no sibling data, so we assume no
  `[rhtpa-2.1]` sibling exists. 4.3 overlap is skipped (field not configured).
- **Step 5 — Lifecycle:** cannot query the product pages URL in this eval. 2.1.x and 2.2.x are
  assumed in support. The engineer must verify.
- **Step 6 — Already fixed:** no resolved siblings. Within 2.2.x the fix already shipped in 2.2.3.
- **Step 7 — Concurrent triage:** skipped (Upstream Affected Component field not configured).
- **Step 7.5 — Release Jira:** find or create "RHTPA <next-2.2.z> Release Tasks" Epic and
  "RHTPA <next-2.2.z> CVE triage" Task, each with individual confirmation. The next z version is
  not derivable without Jira version data, so the engineer supplies it. Preemptive 2.1.x tasks
  are not linked to release Jira.
