# TC-8060 — Step 2: Version Impact Analysis

CVE-2026-99010: h2 < 0.4.5 is affected; 0.4.5 fixes it. Ecosystem is Cargo. Issue scope is **2.2.x**.

## 2.1 Supportability matrix (loaded)

I loaded both streams from `security-matrix-mock.md`. The format check passed: Supportability Matrix, Ecosystem Mappings, Source Pinning Method and Forward Pointer are all present, and the Ecosystem Mappings columns match the template. The staleness warning from Step 0.3 still applies, since the matrix is 152 days old.

| Stream | Version | Build | backend tag | Notes |
|--------|---------|-------|-------------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | retag of 2.2.1 (backend) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | |

## 2.2 Development stream

There is no Jira version metadata (`getJiraIssueTypeMetaWithFields` was not called in this eval), so I could not identify an unreleased RHTPA version. 2.2.x is the latest configured stream and has no forward pointer. **No development stream was checked.** In a real triage, this row would come from branch HEAD of the matching source repo.

## 2.3 Dependency versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`)

The h2 lock-file versions below come from the issue fixture's "Mock Dependency Chain Data" Cargo.lock evidence: 2.2.0 through 2.2.2 have h2 0.4.4, and 2.2.3 and later have h2 0.4.5.

> **Data discrepancy, needs engineer confirmation.** The "h2 versions by tag" table in `security-matrix-mock.md` disagrees with the issue fixture's Cargo.lock evidence:
>
> | Tag | Issue fixture (Cargo.lock evidence) | Matrix mock table |
> |-----|-------------------------------------|-------------------|
> | `v0.4.5` (2.2.0) | 0.4.4 | 0.4.8 |
> | `v0.4.8` (2.2.1 / 2.2.2) | 0.4.4 | 0.4.8 |
> | `v0.4.11` (2.2.3) | 0.4.5 | 0.4.9 |
> | `v0.4.12` (2.2.4) | 0.4.5 | 0.4.9 |
>
> If the matrix-mock values were right, every 2.2.x version would be at or above 0.4.5. The outcome would then be Case C: close as Not a Bug, VEX "Component not Present". In a real triage this is settled by running the `git show` command again on each tag. For this eval I treat the Cargo.lock evidence attached to TC-8060 as authoritative, because it is the scenario-specific lock and manifest evidence for this issue. The rest of this analysis builds on it.

## 2.4 Version impact table

```
Version Impact for CVE-2026-99010 (h2 < 0.4.5), stream 2.2.x (issue scope):

| Version | Stream | backend tag | h2    | Affected? | Notes                                   |
|---------|--------|-------------|-------|-----------|-----------------------------------------|
| 2.2.0   | 2.2.x  | v0.4.5      | 0.4.4 | YES       | transitive via reqwest → hyper → h2     |
| 2.2.1   | 2.2.x  | v0.4.8      | 0.4.4 | YES       | transitive via reqwest → hyper → h2     |
| 2.2.2   | 2.2.x  | v0.4.8      | —     | YES       | same as 2.2.1 (retag), lock check skipped |
| 2.2.3   | 2.2.x  | v0.4.11     | 0.4.5 | NO        | fixed version shipped                   |
| 2.2.4   | 2.2.x  | v0.4.12     | 0.4.5 | NO        | fixed version shipped                   |
| (dev)   | —      | —           | —     | n/a       | no development stream identified        |
```

Out-of-scope stream, used only for the Case A cross-stream check:

| Version | Stream | backend tag | h2 | Affected? | Notes |
|---------|--------|-------------|----|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | NO | matrix-mock h2 table. The issue fixture gives no 2.1.x lock versions |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | NO | matrix-mock h2 table |

The 2.1.x stream is not affected, so there is no cross-stream impact and no preemptive tasks are needed (Case A does not apply).

### Dependency chain context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime [dependencies] entry, not dev/build-only)

First appeared: 2.1.0 (initial project setup; reqwest has always depended on hyper/h2)
Present in: all versions (2.1.x and 2.2.x)

Manifest evidence (backend/Cargo.toml, all versions):
  [dependencies]
  reqwest = { version = "0.12", features = ["json"] }
  # h2 is NOT a direct dependency

Cargo.lock evidence (affected: 2.2.0 – 2.2.2):
  reqwest 0.12.5  → depends on hyper
  hyper   1.4.1   → depends on h2
  h2      0.4.4   ← vulnerable (< 0.4.5)

Cargo.lock evidence (fixed: 2.2.3+):
  h2      0.4.5   ← fixed

Remediation: two-tier.
  1. Preferred: bump the direct dependency (reqwest) and, through it, hyper, so the
     resolved transitive closure has h2 >= 0.4.5. In practice `cargo update -p h2`
     within reqwest 0.12 / hyper 1.x semver ranges is enough, as 2.2.3 shows.
  2. Fallback: pin h2 directly (`cargo add h2@0.4.5`) if the reqwest/hyper bump
     is not viable (breaking API changes, or an intermediate crate pins h2 < 0.4.5).
```

Scope decision: this is a production dependency, so there is no `dev-dependency` label, no priority override, and no feature-gate VEX option.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | not inspected (eval). The latest pinned tag `v0.4.12` has h2 0.4.5 | YES (inferred from 2.2.3 and 2.2.4 releases) |

`release/0.4.z` has shipped h2 0.4.5 since `v0.4.11` (2.2.3). The fix is already upstream for the 2.2.x stream. Branch HEAD itself was not read: real triage would run `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "h2"'` to confirm.

## Steps 3–7 summary (proposed, no Jira mutations performed)

- **Step 3, Affects Versions correction (scoped to 2.2.x):** PSIRT set `RHTPA 2.2.0`. Lock-file evidence shows 2.2.0, 2.2.1 and 2.2.2 are affected. **Proposed:** Affects Versions = RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, which adds 2.2.1 and 2.2.2. 2.2.3 and 2.2.4 are not affected. Version IDs must be discovered dynamically. The correction comment includes the Comment Footnote and no ProdSec @mention, since none is configured.
- **Step 4, duplicates and siblings:** no JQL run (eval). Sibling search: `project = TC AND issuetype = 10024 AND labels = CVE-2026-99010`. Steps 4.3 and 4.4 overlap checks were skipped because the Upstream Affected Component field is not configured.
- **Step 5, lifecycle:** not queried (product pages URL not fetched). The engineer must confirm 2.2.0 through 2.2.2 are still supported. Fixed releases 2.2.3 and 2.2.4 already exist.
- **Step 6, already fixed:** no resolved siblings were examined. Note that the 2.2.x stream already ships the fix from 2.2.3 onward.
- **Step 7, concurrent triage:** skipped because the Upstream Affected Component field is not configured.
- **Step 7.5, release Jira:** proposed find-or-create of the "RHTPA 2.2.x Release Tasks" Epic and "RHTPA 2.2.x CVE triage" Task. The target 2.2.x release version needs engineer confirmation. Cross-CVE dedup was skipped because the Upstream Affected Component field is not configured.

**Outcome: Case B (scoped issue, 2.2.x affected, no other stream affected).** Cargo is a source dependency ecosystem, so 2 remediation tasks are needed. See `remediation.md`.
