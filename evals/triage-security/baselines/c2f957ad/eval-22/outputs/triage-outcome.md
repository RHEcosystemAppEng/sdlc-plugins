# Triage Outcome: TC-8021 (CVE-2026-31812, quinn-proto < 0.11.14)

All Jira mutations below are **proposals**. Under the skill's guardrails, each one needs engineer confirmation before it runs. None were executed, because the eval forbids calls to Jira or other external services.

## Step 2 – Version Impact Analysis

The lock file versions come from the simulated `git show <tag>:Cargo.lock` data in `security-matrix-mock.md`. Each released version is checked at its pinned tag.

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | backend tag | quinn-proto | Affected? | Notes |
|---|---|---|---|---|---|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.8 | — | YES | Retag of 2.2.1, so the 2.2.1 result carries forward |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | |

**Development stream (Step 2.2):**
- Finding it requires checking for unreleased RHTPA Jira versions, which was not possible without Jira.
- The evidence does not show a development stream, so none is reported. Nothing was fabricated to fill the gap.

**Dependency chain (Step 2.3.5):**
- quinn-proto is a Cargo dependency in `backend` (rhtpa-backend).
- The mock data does not say whether it is direct or transitive. A real run would trace it with `cargo tree -i quinn-proto`.
- quinn-proto normally comes in transitively via `quinn`, which is pulled in by HTTP/3-capable crates such as reqwest. This is background knowledge only, not evidence. The remediation task should document the real chain and use the two-tier approach: bump the direct dependency first, and fall back to pinning quinn-proto only if that fails.

**Upstream fix status (Step 2.5):**

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|---|---|---|---|---|
| 2.1.x | Cargo | release/0.3.z | Not inspected (no git access) | Unknown. The latest tag v0.3.12 still ships 0.11.9 |
| 2.2.x | Cargo | release/0.4.z | Not inspected (no git access) | Likely yes: tags v0.4.11 and v0.4.12 already ship 0.11.14 |

## Step 3 – Affects Versions correction (scoped to 2.2.x)

The PSIRT value **RHTPA 2.0.0** is wrong: there is no 2.0.x stream.

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Notes:
- 2.1.0 and 2.1.1 are affected, but they belong to stream 2.1.x. They are excluded from this scoped issue.
- 2.2.3 and 2.2.4 ship the fixed 0.11.14.
- Jira version IDs would be discovered at runtime with `getJiraIssueTypeMetaWithFields`. No IDs are hardcoded.
- After confirmation, add a comment: "Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Based on lock file analysis at pinned commits from security-matrix.md. Scoped to stream 2.2.x per issue suffix." The comment includes the Comment Footnote. There is no ProdSec @mention because none is configured.

## Step 4 – Duplicate / sibling / overlap / reconciliation

- **4.1 / 4.2:**
  - The sibling JQL (`labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8021`) could not be run.
  - No sibling data was provided, so the working assumption is **no siblings**: no same-stream duplicate and no 2.1.x companion issue.
  - This must be confirmed in a live run.
- **4.3:** **Skipped.** The PS Component and Stream custom fields are not configured. The step needs all three fields.
- **4.4:** No preemptive task data was provided, so the assumption is that no matching `security-preemptive` task exists for CVE-2026-31812 and rhtpa-2.2.

## Step 5 – Version lifecycle

- Product pages were not fetched (no WebFetch).
- There is no evidence of EOL status, so 2.2.0–2.2.2 (and 2.1.x) are treated as supported.
- The engineer should confirm this against https://access.example.com/product-life-cycle/rhtpa.

## Step 6 – Already fixed

- No resolved siblings are known, so this does not apply.
- 2.2.3 and later already ship the fix, but that does not cover the affected 2.2.0–2.2.2 releases. They remain affected.

## Step 7 – Concurrent triage

- The JQL on `cf[10632] ~ 'quinn-proto'` returned **zero** in-progress triages.
- No warning is shown and no `concurrent-triage-overlap` label is added. Triage proceeds silently. Details are in `concurrent-triage.md`.

## Step 7.5 – Release Jira orchestration

The affected streams need a release Epic and a release Task each. Each one is found or created individually, with confirmation:

- 2.2.x (next release, for example the version after 2.2.4):
  - Find or create `RHTPA <next 2.2.z> Release Tasks` and `RHTPA <next 2.2.z> CVE triage`.
  - The exact version must be confirmed by the engineer. It is not inferred here.
- 2.1.x (for the preemptive work):
  - Preemptive tasks are not linked to release Jira.
- 7.5.3 cross-CVE dedup:
  - No existing remediation Task for quinn-proto is known on the release Task, so it is not dedup'd.

## Step 8 – Decision: **Case A + Case B (remediation required)**

The decision path:
- Supported versions are affected (2.2.0, 2.2.1, 2.2.2), so this is **not** Case C. The issue is not closed.
- The issue is **scoped** (2.2.x), and the other stream **2.1.x is also affected**. Case A applies.
- Cargo is a source dependency ecosystem, so each stream gets **2 tasks**.

### Case A – Cross-stream impact (2.1.x)

1. Post a comment on TC-8021, with the Comment Footnote:
   > Cross-stream impact: quinn-proto < 0.11.14 also affects stream(s) 2.1.x (2.1.0, 2.1.1 ship 0.11.9) based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage.
2. No 2.1.x CVE Jira is known, so create **preemptive** tasks for 2.1.x. They carry the label `security-preemptive` and link to TC-8021 with **Related**.
   - Preemptive task 1: upstream backport. Bump quinn-proto to >= 0.11.14 on `release/0.3.z` of rhtpa-backend. Upstream fix status is unknown, and the latest 0.3.z tag still ships 0.11.9.
   - Preemptive task 2: downstream propagation. Update rhtpa-release.0.3.z to the new backend tag. This task is **blocked by** task 1.
3. Post a comment listing the preemptive tasks. When PSIRT later creates a 2.1.x CVE Jira, Step 4.4 reconciliation picks them up.

### Case B – Remediation for the issue's stream (2.2.x)

The fix appears to already be on the upstream branch (v0.4.11 and later ship 0.11.14), so the **dependency bump / fix-available** variant applies. This must be confirmed by a `git show release/0.4.z:Cargo.lock` check.

1. **Task 1, upstream / dependency bump (2.2.x):** confirm that `release/0.4.z` HEAD of rhtpa-backend ships quinn-proto >= 0.11.14. If it does not, run `cargo update -p quinn-proto` to reach >= 0.11.14.
   - Labels: CVE-2026-31812, security.
   - Link to TC-8021 with **Depend**.
   - Security level copied from the parent Vulnerability.
2. **Task 2, downstream propagation (2.2.x):** in rhtpa-release.0.4.z, point the backend source reference in `artifacts.lock.yaml` at a tag that ships >= 0.11.14 (v0.4.11 or later).
   - This task is **blocked by** Task 1.
   - Link to TC-8021 with **Depend**.

Both tasks follow `task-description-template.md`. Their Implementation Notes carry `upstream` deployment-context coordination guidance. After each task is created, a description digest comment is posted.

**Release linking:**
- Each 2.2.x remediation Task links to the 2.2.x release Task with **Blocks**.
- TC-8021 links to the release Task with **Related**.

Priority and fixVersion are prompted (both prompts are enabled in the config). They are not set automatically.

Note for the engineer: 2.2.3 and 2.2.4 already ship the fix. Remediation for 2.2.x is mostly about confirming the next 2.2.z release (and any z-stream respin of an older release, if required) carries 0.11.14.

### Pre-creation checklist

- [x] Task count: 2 per stream (Cargo is a source dependency).
- [x] Cross-stream coverage: 2.1.x gets preemptive tasks, because no sibling CVE Jira is known.
- [x] Link types: Depend for 2.2.x to TC-8021, Related for the 2.1.x preemptive tasks to TC-8021, Blocks from upstream to downstream within each stream.
- [x] Preemptive labels are on the 2.1.x tasks.
- [x] Coordination guidance: `upstream` deployment context.
- [x] Release Jira linking: 2.2.x tasks link to the 2.2.x release Task with Blocks. Preemptive tasks are excluded.
- [x] Dedup consistency: no stream was dedup'd.

## Post-triage (after confirmation)

1. Add the `ai-cve-triaged` label to TC-8021.
2. Post a summary comment covering:
   - the version impact table
   - the Affects Versions correction (RHTPA 2.0.0 → RHTPA 2.2.0, 2.2.1, 2.2.2)
   - the outcome (remediation created, Case A + B)
   - the task keys and release Epic/Task keys
   - dedup results (none)
   - an ADF @mention of the issue reporter (the PSIRT analyst)
   - the Comment Footnote

## Summary

**TC-8021 is affected and stays open, with remediation required.**

- Supported 2.2.x versions 2.2.0–2.2.2 ship vulnerable quinn-proto (0.11.9 or 0.11.12, below 0.11.14). 2.2.3 and later are fixed.
- Affects Versions should be corrected from RHTPA 2.0.0 to RHTPA 2.2.0, 2.2.1, 2.2.2.
- Stream 2.1.x (2.1.0, 2.1.1 on 0.11.9) is also affected. It gets a cross-stream comment and 2 preemptive tasks.
- Stream 2.2.x gets 2 Case B tasks: dependency bump and downstream propagation.
- Step 7 found no concurrent quinn-proto triage, so triage continued without the overlap label.

Caveats:
- The matrix is 151 days old.
- External CVE data and lifecycle data were unavailable.
- Sibling, preemptive and release Jira searches were not executed.
- The task's TC-8021 differs from the mock file's TC-8001.
