# Step 2 – Version Impact Analysis: TC-8001

The lock file data comes from the "Mock Lock File Data" section of security-matrix-mock.md. That data simulates the output of `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at each pinned backend tag.

## 2.1 – Supportability matrix (aggregated)

| Stream | Konflux repo | Versions | Backend pin | Lock file | Upstream branch |
|---|---|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | `v0.3.8`, `v0.3.12` | Cargo.lock | release/0.3.z |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0–2.2.4 | `v0.4.5`, `v0.4.8`, `v0.4.8` (2.2.2 retag), `v0.4.11`, `v0.4.12` | Cargo.lock | release/0.4.z |

Format validation passed. Both files contain Supportability Matrix, Source Pinning Method, Ecosystem Mappings with the canonical columns, and Forward Pointer.

## 2.2 – Development stream

The Jira unreleased-version lookup (`getJiraIssueTypeMetaWithFields`) was not run in this eval, and no development stream beyond 2.1.x and 2.2.x is configured. As a result, no development-branch HEAD row appears below. A real run would add the earliest unreleased RHTPA version (checked at branch HEAD) if one exists.

## 2.4 – Version impact table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Backend tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | Outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | In scope |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | In scope |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | Same as 2.2.1 (backend retag of 2.2.1, so the lock check was skipped) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | Fixed version shipped |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | Fixed version shipped |

Summary:
- **In scope (2.2.x):** 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and 2.2.4 are not affected, because the fix first shipped in 2.2.3 (backend v0.4.11).
- **Out of scope (2.1.x):** 2.1.0 and 2.1.1 are affected. This triggers Case A, cross-stream impact.

### 2.3.5 – Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn → quinn-proto   [chain must be confirmed from Cargo.lock / Cargo.toml]
  Type: likely transitive (quinn-proto is normally pulled in via the `quinn` QUIC crate,
        e.g. through reqwest/h3 http3 support). Not verified: the mock data provides
        only the resolved version, not the dependency graph.
  Profile: assumed production (no evidence of dev-/build-only scope)
  Present in: all versions 2.1.0 – 2.2.4
```

Remediation guidance follows the two-tier transitive approach. First, bump the direct dependency (for example `quinn`/`reqwest`) to a release whose closure resolves quinn-proto >= 0.11.14. If that is not viable, pin with `cargo add quinn-proto@0.11.14` or run `cargo update -p quinn-proto`. Because 0.11.14 is semver-compatible with 0.11.x, `cargo update -p quinn-proto` will most likely work without bumping the parent.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not read (eval: no `git show`). Last release tag v0.3.12 = 0.11.9 | Not confirmed, so treat as NOT fixed |
| 2.2.x | Cargo | release/0.4.z | not read (eval: no `git show`). Release tags v0.4.11/v0.4.12 = 0.11.14 | Not confirmed at HEAD. Tags on the branch already ship 0.11.14 |

For 2.2.x, the release tags cut from `release/0.4.z` already ship quinn-proto 0.11.14. Branch HEAD is therefore very likely fixed, but this could not be verified without `git show release/0.4.z:Cargo.lock`. The skill forbids assuming versions, so the remediation plan uses the upstream backport template by default. If the engineer confirms that HEAD is at 0.11.14 or later, switch the 2.2.x upstream task to the dependency bump variant. The downstream propagation task is unchanged in either case.

Engineer confirmation of this table is required before Step 3.

---

## Step 3 – Affects Versions correction (planned)

- `getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")` → filter `versions.allowedValues` by the "RHTPA" prefix to resolve version IDs dynamically.
- Scoped to stream 2.2.x:
  `Current: [RHTPA 2.0.0] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
  RHTPA 2.0.0 is wrong because no 2.0.x stream exists. The 2.1.x versions belong to a sibling or companion issue and are not added here.
- Comment (with footnote, no ProdSec @mention because none is configured): "Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Based on lock file analysis at pinned commits from security-matrix.md. Scoped to stream 2.2.x per issue suffix."

## Steps 4–7 (planned / assumed)

- Step 4: JQL `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001`. Siblings are assumed to be none for this eval. 4.3 overlap is skipped because the Upstream Affected Component field is not configured. 4.4 found no preemptive tasks to reconcile.
- Step 5: lifecycle check against the Product pages URL. Assume 2.1.x and 2.2.x are supported.
- Step 6: no resolved siblings, so the issue is not already fixed.
- Step 7: skipped, because the Upstream Affected Component field is not configured.
- Step 7.5: find or create "RHTPA 2.2.x Release Tasks" (Epic) and "RHTPA <next 2.2.z> CVE triage" (Task). This needs individual confirmation, and the version must come from the engineer and supportability data. 2.1.x preemptive tasks are not linked to release Jira.
