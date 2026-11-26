# TC-8060 — Step 2: Version Impact Analysis

CVE-2026-99010: h2 < 0.4.5 (fixed in 0.4.5). Issue scope: **2.2.x**
(`rhtpa-release.0.4.z`).

## 2.1 — Supportability matrix (2.2.x stream)

| Version | Build | backend tag | Notes |
|---------|-------|-------------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | `v0.4.12` | |

Note: the backend tag `v0.4.5` (product 2.2.0) is a source tag. It is not the h2 version, even though it matches the h2 fix version string.

Matrix format validation: Supportability Matrix, Source Pinning Method, Ecosystem Mappings (correct columns), and Forward Pointer are all present. Result: Pass.

## 2.2 — Development stream

Unreleased Jira versions could not be queried (eval: no Jira access), so no development stream (branch HEAD) row could be checked. 2.2.x is the latest configured stream, so the next 2.2.z development head would be `release/0.4.z` HEAD. See 2.5.

## Data-source conflict (flagged for engineer review)

The two fixtures disagree about h2 versions in the 2.2.x lock files:

| Tag | `security-matrix-mock.md` "h2 versions by tag" | `vuln-issue-transitive.md` Cargo.lock evidence |
|-----|------|------|
| `v0.4.5` (2.2.0) | 0.4.8 | 0.4.4 |
| `v0.4.8` (2.2.1 / 2.2.2) | 0.4.8 | 0.4.4 |
| `v0.4.11` (2.2.3) | 0.4.9 | 0.4.5 |
| `v0.4.12` (2.2.4) | 0.4.9 | 0.4.5 |

The matrix's generic h2 table would make every 2.2.x version **NOT affected** (all >= 0.4.5), which would mean Case C (close as Not a Bug). The issue fixture's Cargo.lock evidence is the simulated `git show <tag>:Cargo.lock` output for this triage. It also includes the dependency chain and manifest evidence for this CVE scenario, so the **impact table below uses the issue fixture's lock-file evidence**. In a real triage, the skill would stop here and ask the engineer to re-run `git show v0.4.5:Cargo.lock | grep -A2 'name = "h2"'` to settle the conflict before any Jira change.

## 2.3 / 2.4 — Version impact table

```
Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | backend tag | h2      | Affected? | Notes                                     |
|---------|-------------|---------|-----------|-------------------------------------------|
| 2.2.0   | v0.4.5      | 0.4.4   | YES       | Cargo.lock: h2 0.4.4 via hyper 1.4.1      |
| 2.2.1   | v0.4.8      | 0.4.4   | YES       | Cargo.lock: h2 0.4.4 via hyper 1.4.1      |
| 2.2.2   | v0.4.8      | —       | YES       | same as 2.2.1 (backend retag of 2.2.1)    |
| 2.2.3   | v0.4.11     | 0.4.5   | NO        | fixed version shipped                     |
| 2.2.4   | v0.4.12     | 0.4.5   | NO        | fixed version shipped                     |
| dev     | release/0.4.z HEAD | not checked | UNKNOWN | Jira/git unavailable in eval; inferred fixed (see 2.5) |
```

**Affected in scope (2.2.x): 2.2.0, 2.2.1, 2.2.2.** Not affected: 2.2.3, 2.2.4.

### Cross-stream (2.1.x, outside scope — Case A check)

| Version | backend tag | h2 | Affected? | Notes |
|---------|-------------|----|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | NO | matrix h2 table only (no issue-fixture lock data for 2.1.x) |
| 2.1.1 | v0.3.12 | 0.4.5 | NO | matrix h2 table only |

Note: the issue fixture says h2 is "present in all versions" from 2.1.0 onward. That confirms presence but does not give a version. The 2.1.x versions come from the same matrix h2 table that conflicts for 2.2.x, so confidence is reduced. Engineer verification is recommended. Based on available data, no other stream is affected, so **Case A does not apply**.

## 2.3.5 — Dependency chain context

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime [dependencies] entry; not dev/build-only)

Manifest evidence (backend/Cargo.toml, all versions):
  [dependencies]
  reqwest = { version = "0.12", features = ["json"] }
  h2 is NOT a direct dependency.

Lock file evidence (affected 2.2.0–2.2.2):
  reqwest 0.12.5 → hyper 1.4.1 → h2 0.4.4
Lock file evidence (fixed 2.2.3+):
  h2 0.4.5

First appeared: 2.1.0 (initial project setup; reqwest has always depended on hyper/h2)
Present in: all versions (2.1.x and 2.2.x)

Remediation: two-tier.
  1. Preferred: bump the direct dependency (reqwest, and therefore hyper) to a
     version whose resolved closure includes h2 >= 0.4.5. reqwest 0.12 / hyper 1.x
     accept h2 0.4.x semver-compatibly, so `cargo update -p reqwest -p hyper -p h2`
     within existing constraints should resolve h2 0.4.5 (this is what 2.2.3+ shows).
  2. Fallback: pin the transitive dependency directly
     (`cargo update -p h2 --precise 0.4.5` or `cargo add h2@0.4.5`) if the
     reqwest/hyper bump is not viable.
```

Dependency scope decision tree: production dependency, so no `dev-dependency` label and no priority override. It is not feature-gated, so the VEX "not in execute path" option does not apply.

## 2.5 — Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | not read (git unavailable in eval) | Likely YES (inferred: tags v0.4.11 and v0.4.12 from this branch ship h2 0.4.5) |

Because HEAD could not be confirmed, remediation keeps the upstream task with the two-tier approach (see remediation.md). Its first step is to confirm `release/0.4.z` HEAD. If HEAD already has h2 >= 0.4.5, the upstream task reduces to verification or a dependency bump (dependency-bump variant), and the downstream task points the Konflux source reference at a fixed tag (v0.4.11 or later).

## Step 3 — Affects Versions correction (proposed, not executed)

| | Versions |
|--|--|
| PSIRT-assigned | RHTPA 2.2.0 |
| Lock-file evidence | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |
| Proposed change | Add RHTPA 2.2.1 and RHTPA 2.2.2 (version IDs discovered at runtime with getJiraIssueTypeMetaWithFields) |

## Steps 4–7 (simulated)

- Step 4: sibling/duplicate JQL not run (eval). No duplicates assumed. Step 4.3 overlap is skipped because Upstream Affected Component is not configured.
- Step 5: the lifecycle page was not fetched (eval). 2.2.x is assumed supported.
- Step 6: no resolved siblings, so this is not an already-fixed case. Note that 2.2.3 and 2.2.4 already ship the fix.
- Step 7: skipped because Upstream Affected Component field is not configured.
- Step 7.5: release Epic/Task lookup ("RHTPA 2.2.x Release Tasks" / "RHTPA 2.2.x CVE triage") is not executed. The version would be decided by the engineer.

## Outcome

Scoped issue, 2.2.x affected (2.2.0–2.2.2), no other stream affected → **Case B**. Create 2 remediation tasks for 2.2.x (Cargo source dependency, transitive). See remediation.md.
