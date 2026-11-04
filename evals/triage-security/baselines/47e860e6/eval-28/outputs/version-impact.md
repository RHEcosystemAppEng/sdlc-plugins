# Step 2 – Version Impact Analysis: CVE-2026-99010 (h2 < 0.4.5)

Scope: issue TC-8060 is scoped to stream **2.2.x** (`rhtpa-release.0.4.z`). Stream 2.1.x is listed
only for the Case A cross-stream check.

## 2.1 – Supportability matrix (2.2.x)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem mapping: Cargo, repo `backend`, lock file `Cargo.lock`, upstream branch `release/0.4.z`.
Source pinning: `artifacts.lock.yaml` (the download URL contains the tag).

### Step 0.3 – Matrix staleness

The matrix has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-11-04, so it is about 129 days old,
which exceeds the 14-day threshold.

> Security matrix for stream 2.2.x was last updated on 2026-06-28 (129 days ago). The matrix may
> not reflect recent releases. Options: Refresh now / Proceed anyway / Stop.

In this eval I chose **Proceed anyway**. A real triage should refresh the matrix first, because
2.2.5+ releases may be missing.

## 2.2 – Development stream

Jira unreleased versions could not be queried in this eval. No development-stream data is in the
fixtures, so the dev branch HEAD row is marked "not checked".

## 2.3 – Version impact table (2.2.x, in scope)

Source: the `Cargo.lock` evidence in the fixture's "Mock Dependency Chain Data" for TC-8060.

| Version | backend tag | h2 | Affected? | Notes |
|---------|-------------|----|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.4.4 | **YES** | hyper 1.4.1 → h2 0.4.4; reqwest 0.12.5 |
| 2.2.1 | `v0.4.8` | 0.4.4 | **YES** | |
| 2.2.2 | `v0.4.8` | — | **YES** | same as 2.2.1 (backend retag, lock check skipped) |
| 2.2.3 | `v0.4.11` | 0.4.5 | NO | fixed version shipped |
| 2.2.4 | `v0.4.12` | 0.4.5 | NO | fixed version shipped |
| dev (branch HEAD) | — | not checked | — | no dev-stream evidence available |

**Affected in scope:** RHTPA 2.2.0, 2.2.1, 2.2.2. **Not affected:** 2.2.3, 2.2.4.

### Cross-stream check (2.1.x, out of scope)

| Version | backend tag | h2 | Affected? | Notes |
|---------|-------------|----|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.4.5 | NO | from matrix mock h2 table |
| 2.1.1 | `v0.3.12` | 0.4.5 | NO | from matrix mock h2 table |

2.1.x is not affected. **Case A does not apply**: no cross-stream comment and no preemptive tasks.

### Data discrepancy flagged for the engineer

The generic "h2 versions by tag" table in `security-matrix-mock.md` gives **different** 2.2.x values
from the issue-specific Cargo.lock evidence:

| Tag | matrix-mock h2 table | TC-8060 Cargo.lock evidence |
|-----|----------------------|-----------------------------|
| `v0.4.5` (2.2.0) | 0.4.8 | 0.4.4 |
| `v0.4.8` (2.2.1/2.2.2) | 0.4.8 | 0.4.4 |
| `v0.4.11` (2.2.3) | 0.4.9 | 0.4.5 |
| `v0.4.12` (2.2.4) | 0.4.9 | 0.4.5 |

If the matrix-mock values were correct, every 2.2.x version would be >= 0.4.5 and the outcome would be
Case C (close as Not a Bug, VEX "Component not Present"). This analysis uses the issue-specific
Cargo.lock evidence, which the fixture names as the simulated `git show` output for this triage.
In a real run, `git show v0.4.5:Cargo.lock | grep -A2 'name = "h2"'` decides which is right. The
engineer should confirm before any Jira mutation.

## 2.3.5 – Dependency chain context

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime [dependencies] entry, not dev/build-only)

Manifest evidence (backend/Cargo.toml, all versions):
  [dependencies]
  reqwest = { version = "0.12", features = ["json"] }
  # h2 is NOT a direct dependency

Lock evidence (2.2.0 – 2.2.2):
  reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4   (vulnerable, < 0.4.5)
Lock evidence (2.2.3+):
  h2 0.4.5                                  (fixed)

First appeared: 2.1.0 (initial project setup; reqwest has always depended on hyper/h2)
Present in: all versions (vulnerable range only in 2.2.0 – 2.2.2)

Remediation: transitive, so use the two-tier approach.
  1. Preferred: bump the direct dependency (reqwest, and with it hyper) so the resolved
     h2 is >= 0.4.5 (e.g. `cargo update -p reqwest -p hyper -p h2`).
  2. Fallback: pin h2 directly (`cargo add h2@0.4.5` or `cargo update -p h2 --precise 0.4.5`)
     if the reqwest/hyper bump is not viable.
```

Scope decision: this is a production dependency, not dev-only and not feature-gated. No
`dev-dependency` label, no priority override, no VEX option.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | not read (no `git show` in eval) | Likely YES: tags `v0.4.11` and `v0.4.12` cut from this branch already ship h2 0.4.5 |

The fix has already shipped in 2.2.3 and later on this branch. The remaining exposure is that
2.2.0 through 2.2.2 ship h2 0.4.4. Before creating tasks, the engineer should confirm (a) branch HEAD
still resolves h2 >= 0.4.5 and (b) whether 2.2.0 to 2.2.2 still need remediation, or whether
customers on 2.2.x are directed to upgrade to 2.2.3+ (Step 5 lifecycle check, not run in this eval).

## Step 3 – Affects Versions correction (proposed, not executed)

| | Versions |
|--|----------|
| Current (PSIRT) | RHTPA 2.2.0 |
| Proposed | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

Rationale: lock-file evidence shows h2 0.4.4 in 2.2.0 and 2.2.1, and 2.2.2 is a retag of 2.2.1.
2.2.3 and 2.2.4 ship 0.4.5 and must not be added. Version IDs would be discovered dynamically with
`getJiraIssueTypeMetaWithFields`.

## Steps 4–7 (not executable in eval)

- Step 4: no sibling or duplicate JQL was run. Step 4.3 was skipped because the Upstream Affected Component field is not configured.
- Step 5: the lifecycle page was not fetched.
- Step 6: no resolved siblings are known.
- Step 7: skipped because the Upstream Affected Component field is not configured.
- Step 7.5: release Jira lookup was not run.
