# TC-8001 — Version Impact Analysis (Step 2)

> Eval run: lock file values come from the "Mock Lock File Data" section of the
> provided security matrix. That section stands in for
> `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`. No `git show` was run.

## 2.1 – Supportability matrix (all configured streams)

Both rows of the Version Streams table were enumerated: 2.1.x (`rhtpa-release.0.3.z`)
and 2.2.x (`rhtpa-release.0.4.z`). Format check: Supportability Matrix, Ecosystem
Mappings (columns `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`),
Source Pinning Method, and Forward Pointer are present in both streams. **Pass.**

## 2.2 – Development stream

Finding the development stream needs the unreleased `RHTPA` versions from
`getJiraIssueTypeMetaWithFields`. That call was not made, and the inputs include no
Jira version metadata or development-branch lock data. **The development stream could
not be determined, so no branch-HEAD row is included.** This must be resolved before
the triage is finalized. Do not assume a dev version.

## 2.3 / 2.4 – Version impact table

Version Impact for **CVE-2026-31812 (quinn-proto < 0.11.14)**. Fix threshold: 0.11.14
(Jira description; external enrichment unavailable).

| Version | Stream | Pinned backend tag | quinn-proto | Affected? | Notes |
|---------|--------|--------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8`  | 0.11.9  | **YES** | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9  | **YES** | |
| 2.2.0 | 2.2.x | `v0.4.5`  | 0.11.9  | **YES** | |
| 2.2.1 | 2.2.x | `v0.4.8`  | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | `v0.4.8`  | —       | **YES** | same as 2.2.1 (backend retag of 2.2.1, build 0.4.9; lock check skipped and result carried forward) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | at fix version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | at fix version |
| dev   | ?     | branch HEAD | not determined | not determined | see 2.2 |

Summary:
- **In issue scope (2.2.x):** 2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and 2.2.4 already
  ship the fixed 0.11.14 (fix first shipped in **RHTPA 2.2.3**, built 2026-03-23).
- **Outside issue scope (2.1.x):** 2.1.0 and 2.1.1 are affected (0.11.9). This is
  cross-stream impact (Case A).
- **PSIRT claim:** RHTPA 2.0.0 does not exist in any configured stream.

### 2.3.5 – Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (rhtpa-backend workspace) → ... → quinn-proto
  Type: NOT DETERMINED (direct vs transitive)
  Profile: NOT DETERMINED
```

The mock data only gives lock file versions. It does not include `Cargo.toml` manifests
or the `[[package]] dependencies` graph, so I can't say whether quinn-proto is a direct
dependency or comes in transitively (for example through `quinn` / an HTTP/3 client).
I also can't tell whether it is production-only or dev-only. Per the guardrails this is
**not assumed**. To resolve it before task creation, run:

- `git show v0.4.8:Cargo.lock` and `git show v0.3.12:Cargo.lock`, then find which packages list `quinn-proto` in their `dependencies`
- `git show v0.4.8:Cargo.toml` and the member manifests, checking `[dependencies]`, `[dev-dependencies]`, and `[build-dependencies]`

Introduction point: quinn-proto is present in every pinned tag of both streams.
2.2.x went from 0.11.9 (v0.4.5) to 0.11.12 (v0.4.8) to 0.11.14 (v0.4.11).

The remediation tasks therefore include both the direct and transitive remediation
approaches. The engineer or `/implement-task` picks the right one after checking the
chain.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.2.x  | Cargo | backend | `release/0.4.z` | Not read (eval). Released tags `v0.4.11` and `v0.4.12` from this line already ship 0.11.14 | **Likely YES**. Confirm with `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock \| grep -A2 quinn-proto` |
| 2.1.x  | Cargo | backend | `release/0.3.z` | Not read (eval). Latest released tag `v0.3.12` ships 0.11.9 | **Not confirmed**. Treat as not fixed upstream until `git show release/0.3.z:Cargo.lock` shows >= 0.11.14 |

Remediation path:
- **2.2.x:** the fix is already on the upstream line and already released in 2.2.3 and 2.2.4.
  This calls for the dependency bump variant, followed by downstream propagation. In
  practice the fix is already shipped (see remediation.md).
- **2.1.x:** upstream backport on `release/0.3.z`, then downstream propagation in
  `rhtpa-release.0.3.z`.

**Engineer checkpoint:** review and confirm this table before Step 3. For this eval it
is assumed confirmed. The 148-day matrix staleness and the unknown dev stream are still
open caveats.
