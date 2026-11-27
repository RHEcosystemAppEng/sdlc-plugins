# TC-8050 — Step 2 Version Impact Analysis

**CVE-2026-99001 — criterion < 0.5.2 (fixed in 0.5.2), Cargo ecosystem**
Issue stream scope: **2.2.x**

No `git show` commands were run. Lock-file versions come from the "criterion versions by tag" mock data in `security-matrix-mock.md`, which stands in for `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`. The dependency-chain data comes from the mock manifest data in `vuln-issue-dev-dependency.md`.

## 2.1 – Supportability matrix loaded

| Stream | Konflux release repo | Versions | Lock file | Upstream branch |
|--------|----------------------|----------|-----------|-----------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | `Cargo.lock` (backend) | `release/0.3.z` |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4 | `Cargo.lock` (backend) | `release/0.4.z` |

Format validation: both streams contain Supportability Matrix, Ecosystem Mappings (with the expected 5 columns), Source Pinning Method and Forward Pointer. **Pass.**
Staleness: the matrix is 152 days old (see data-extraction.md). The engineer chose to proceed.

## 2.2 – Development stream

No Jira unreleased-version data was available because Jira was not called. The matrix has no stream past 2.2.x ("latest stream — no forward pointer"), so **no separate development stream was identified**. Upstream branch HEADs are covered in 2.5.

## 2.3 / 2.4 – Version Impact Table

```
Version Impact for CVE-2026-99001 (criterion < 0.5.2):
```

| Stream | Version | Backend tag (pinned) | criterion | Affected? | Notes |
|--------|---------|----------------------|-----------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.5.1 | YES (dev-only) | outside issue scope; cross-stream |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.5.1 | YES (dev-only) | outside issue scope; cross-stream |
| **2.2.x** | **2.2.0** | `v0.4.5` | 0.5.1 | **YES (dev-only)** | in scope |
| **2.2.x** | **2.2.1** | `v0.4.8` | 0.5.1 | **YES (dev-only)** | in scope |
| **2.2.x** | **2.2.2** | `v0.4.8` | — | **YES (dev-only)** | in scope; same as 2.2.1 (backend retag) |
| **2.2.x** | **2.2.3** | `v0.4.11` | 0.5.1 | **YES (dev-only)** | in scope |
| **2.2.x** | **2.2.4** | `v0.4.12` | 0.5.1 | **YES (dev-only)** | in scope |

**Summary:** every supported version locks criterion 0.5.1, which is inside the affected range (< 0.5.2). criterion is a **dev-dependency only** and is **not present in any production build or shipped container image**.

### Dependency chain context (Step 2.3.5)

```
Dependency chain for criterion:
  backend (workspace) → criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
           NOT present in production builds — used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in: all versions (2.1.0 – 2.2.4)

Manifest evidence (backend/Cargo.toml, all versions):
  [dev-dependencies]
  criterion = "0.5.1"

Remediation: bump criterion to >= 0.5.2 in backend/Cargo.toml [dev-dependencies]
and refresh Cargo.lock.
```

**Dependency scope decision (dev-only / build-only branch of the decision tree):**

- Cargo `[dev-dependencies]` are used for tests and benchmarks only and are **not shipped**. Exploiting the bug needs crafted benchmark names during a local or CI benchmark run, so there is no production attack surface.
- Dev dependencies are still a supply-chain risk, so remediation tasks **are still created**, with these changes:
  - add the **`dev-dependency`** label
  - set priority to **Normal** regardless of CVE severity (the CVE's priority is not inherited)
  - include the note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."
- This is **not** the feature-gated optional-dependency case, so no VEX "skip remediation" prompt applies. The issue is **not** closed as Not a Bug, because the package is in the lock file inside the affected range.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | unknown (no mock data for branch HEAD; latest pinned tag `v0.4.12` has 0.5.1) | **Not confirmed — treated as NOT fixed** |
| 2.1.x | Cargo | `release/0.3.z` | unknown (latest pinned tag `v0.3.12` has 0.5.1) | Not confirmed — treated as NOT fixed |

No upstream-branch-HEAD evidence was available, and the skill forbids guessing versions. The remediation path therefore uses the **upstream backport + downstream propagation** pair, not the dependency-bump variant. In a real run, check `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'criterion'` before creating tasks. If HEAD already has >= 0.5.2, switch to the dependency-bump variant.

## Steps 3–7.5 – Jira triage operations (simulated, none executed)

- **Step 3 – Affects Versions correction (2.2.x scope):** Jira currently has `RHTPA 2.2.0`. Lock-file evidence shows that 2.2.0–2.2.4 all ship criterion 0.5.1. Proposed: add RHTPA 2.2.1, 2.2.2, 2.2.3 and 2.2.4 to Affects Versions. Version IDs must be discovered at runtime with `getJiraIssueTypeMetaWithFields`. The correction comment would note that criterion is dev-only and not shipped. Engineer confirmation is required.
- **Step 4 – Duplicates/siblings:** JQL for `labels = CVE-2026-99001` was not run. There is no sibling data, so no duplicate is assumed. Step 4.3 (cross-CVE overlap) is skipped because Upstream Affected Component is not configured. Step 4.4 reconciliation found no existing preemptive tasks in the data provided.
- **Step 5 – Lifecycle:** the product pages URL was not fetched. All matrix versions are assumed supported, pending confirmation.
- **Step 6 – Already fixed:** no resolved sibling issues are known and no version ships 0.5.2, so the issue is not already fixed.
- **Step 7 – Concurrent triage:** skipped because Upstream Affected Component is not configured.
- **Step 7.5 – Release Jira:** the release Epic/Task (`RHTPA 2.2.5 Release Tasks` / `RHTPA 2.2.5 CVE triage`, version to be confirmed by the engineer) would be found or created after individual confirmation. Dedup (7.5.3) cannot run because Upstream Affected Component is not configured.

## Cross-stream impact (Case A)

The 2.1.x stream (2.1.0, 2.1.1) is also affected, but it is outside this issue's `[rhtpa-2.2]` scope. Proposed comment on TC-8050:

```
Cross-stream impact: criterion < 0.5.2 also affects stream(s) 2.1.x based on
lock file analysis (2.1.0, 2.1.1 ship criterion 0.5.1 as a dev-only dependency).
These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.

---
This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
```

If the Step 4 sibling search finds no `[rhtpa-2.1]` CVE Jira for CVE-2026-99001, preemptive 2.1.x tasks are proposed. Their structure is in remediation.md.
