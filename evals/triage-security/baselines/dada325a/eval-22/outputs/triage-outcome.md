# Triage Outcome: TC-8021 (CVE-2026-31812, quinn-proto)

**Decision: AFFECTED.** Stream 2.2.x versions 2.2.0, 2.2.1 and 2.2.2 ship a vulnerable quinn-proto. Affects Versions must be corrected. **Case A** applies (cross-stream impact on 2.1.x), followed by **Case B** remediation for 2.2.x. The issue must not be closed.

## Step summary

| Step | Result |
|---|---|
| 0 Config | Valid. Upstream Affected Component = customfield_10632. PS Component, Stream, ProdSec ID and Embargo URL are not configured. |
| 0.3 Staleness | Matrix is 131 days old (last updated 2026-06-28). Warning shown; eval proceeds with the existing matrix. |
| 0.8 Assign | Would assign to the current user and move New → Assigned (simulated). |
| 1 Extraction | CVE-2026-31812, quinn-proto < 0.11.14, fixed in 0.11.14, CVSS 7.5. Scoped to `[rhtpa-2.2]` → 2.2.x. Ecosystem: Cargo. |
| 1.5 Enrichment | MITRE and OSV not queried. Used Jira description data, with lower confidence. |
| 1.7 Embargo | Skipped: no embargo policy URL configured. |
| 2 Impact | 2.1.0, 2.1.1, 2.2.0, 2.2.1 and 2.2.2 (retag) are affected. 2.2.3 and 2.2.4 are not. |
| 3 Affects Versions | Correction needed (see below). |
| 4 Duplicates/siblings | JQL not executed. No sibling data supplied, so assume none. 4.3 skipped (PS Component/Stream fields not configured). 4.4: no preemptive tasks supplied. |
| 5 Lifecycle | Product pages not fetched. Assume the 2.2.x and 2.1.x versions are supported (needs engineer check). |
| 6 Already fixed | No resolved siblings, so this does not apply. |
| 7 Concurrent triage | JQL returned 0 results. Proceed silently with no overlap label. |
| 7.5 Release Jira | Find or create "RHTPA 2.2.x Release Tasks" Epic and "RHTPA <version> CVE triage" Task. Each needs individual engineer confirmation. |
| 8 Remediation | Case A + Case B (see below). |

## Step 3 – Affects Versions correction (needs confirmation)

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

- RHTPA 2.0.0 is wrong. No 2.0.x stream exists, and PSIRT's suffix says 2.2.
- The correction covers 2.2.x only. 2.1.0 and 2.1.1 are affected but belong to a 2.1.x companion issue.
- 2.2.3 and 2.2.4 are left out because they ship quinn-proto 0.11.14, which is fixed.
- Version IDs would come from `getJiraIssueTypeMetaWithFields` (project TC, issue type 10024), filtered by the `RHTPA` prefix. If any of these versions has no Jira entry, flag it to the project admin.
- Comment (with Comment Footnote): "Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]. Based on lock file analysis at pinned commits from security-matrix.md. Scoped to stream 2.2.x per issue suffix." No ProdSec @mention, because no account ID is configured.

## Step 8 – Remediation

There are no concurrent triages and no Step 7.5.3 dedup match is known, so the decision tree continues. Supported versions are affected and the issue is scoped.

### Case A: cross-stream impact (2.1.x)

2.1.0 and 2.1.1 (tags v0.3.8 and v0.3.12) ship quinn-proto 0.11.9, so they are affected.
1. Cross-stream comment on TC-8021 (with footnote): "Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. These streams are tracked by companion issues (see Related links) or may require separate PSIRT triage."
2. Search for a 2.1.x sibling CVE Jira (label CVE-2026-31812, suffix `[rhtpa-2.1]`):
   - If one exists: create no tasks; link it as Related.
   - If none exists: create **preemptive** 2.1.x tasks with the `security-preemptive` label, linked **Related** to TC-8021. That means an upstream backport on `release/0.3.z` (no 2.1.x tag ships the fix) plus downstream propagation in rhtpa-release.0.3.z, linked by Blocks. Then post the preemptive-task list comment.

### Case B: remediation for 2.2.x (Cargo, source dependency, 2 tasks)

- The latest 2.2.x release, **RHTPA 2.2.3/2.2.4 (backend v0.4.11/v0.4.12), already ships quinn-proto 0.11.14**. The fix is in production for this stream; only the older patch releases 2.2.0–2.2.2 are vulnerable.
- Upstream `release/0.4.z` HEAD was not verified with `git show` because the data is not in the eval inputs. If it ships ≥ 0.11.14, use the **"fix available"** variant:
  1. **Dependency bump / verification task** (rhtpa-backend, `release/0.4.z`): confirm quinn-proto ≥ 0.11.14 at HEAD (`cargo update -p quinn-proto` if needed).
  2. **Downstream propagation task** (rhtpa-release.0.4.z), blocked by task 1: make sure the next 2.2.x build pins a backend tag ≥ v0.4.11. This is already true for v0.4.12.
- Link both tasks to TC-8021 with **Depend**. Link task 1 → task 2 with **Blocks**. Link both to the release Task with **Blocks**, and link TC-8021 to the release Task with **Related**.
- Labels include `CVE-2026-31812` and `ai-generated-jira`. Post a description digest comment after each task is created.
- **Engineer judgment point:** the fix already shipped in 2.2.3, so the engineer may treat the 2.2.x tasks as lightweight verification and tell customers to upgrade to ≥ 2.2.3. The skill's decision tree still classifies this as Case B (affected), not Case C, because 2.2.0–2.2.2 are supported and vulnerable.

### Not applicable

- **Case C / VEX:** not applicable, because affected supported versions exist. The VEX field (customfield_12345) is not set.
- **Duplicate/EOL/already-fixed closures:** none triggered.

## Post-triage (after confirmations)

- Add the label `ai-cve-triaged` to TC-8021.
- Post a summary comment with: the impact table, the Affects Versions correction, the outcome (affected, remediation created), task keys, release Epic and Task keys, dedup results (none), an @mention of the reporter, and the Comment Footnote.
- Note: the due date (2026-07-15) has already passed. Raise this with the engineer.

## Caveats (no fabricated data)

- All dependency versions come from the mock lock-file table, not from live `git show`.
- Not available in the eval inputs: development stream, upstream branch HEADs, sibling issues, lifecycle status, and Jira version IDs. Each is marked unverified above.
- The matrix is 131 days stale, so newer releases may exist.
