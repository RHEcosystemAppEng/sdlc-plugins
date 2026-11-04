# TC-8004 — Step 3: Affects Versions Correction

## Scope

The issue is **unscoped** (no stream suffix), so the correction covers every *affected* version across all streams. Under the version impact analysis only the 2.1.x stream is affected. The 2.2.x versions ship h2 >= 0.4.8 and must not be listed.

## 3.1 — Jira version discovery

In real execution: `getJiraIssueTypeMetaWithFields(projectIdOrKey: "TC", issueTypeId: "10024")`, then filter `versions.allowedValues` by prefix `RHTPA`. Version IDs are resolved dynamically at runtime. They are not hardcoded and not invented here, so they appear as `<id of ...>` placeholders.

## 3.2 — Comparison

| Version | Current (PSIRT) | Lock-file verdict | Action |
|---------|-----------------|-------------------|--------|
| RHTPA 2.1.0 | present | YES (h2 0.4.5) | **Keep** |
| RHTPA 2.1.1 | absent | YES (h2 0.4.5) | **Add** |
| RHTPA 2.2.0 | present | NO (h2 0.4.8 = fixed version) | **Remove** |
| RHTPA 2.2.1 / 2.2.2 / 2.2.3 / 2.2.4 | absent | NO | Do not add |

The PSIRT set is partly wrong (it includes the unaffected RHTPA 2.2.0) and incomplete (it is missing RHTPA 2.1.1).

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

If RHTPA 2.1.1 has no matching Jira version, flag "RHTPA 2.1.1 is in the supportability matrix but has no matching Jira version — notify project admin" and continue.

The development stream is not affected or not assessed (see version-impact.md), so no unreleased version is added.

## Proposed mutation (requires engineer confirmation; not executed)

```
jira.edit_issue("TC-8004", fields={
  "versions": [{"id": "<id of RHTPA 2.1.0>"}, {"id": "<id of RHTPA 2.1.1>"}]
})
```

## Proposed comment (requires confirmation)

> Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
> Based on lock file analysis at pinned commits from security-matrix.md (h2 < 0.4.8 is vulnerable):
> - RHTPA 2.1.0 (backend v0.3.8) and RHTPA 2.1.1 (backend v0.3.12) ship h2 0.4.5, so they are affected.
> - RHTPA 2.2.0 (backend v0.4.5) ships h2 0.4.8, the fixed version, so it is not affected and was removed. All later 2.2.x versions ship h2 0.4.8/0.4.9 and are not affected either.
>
> Issue is unscoped (no stream suffix); correction covers all affected versions across all streams.
>
> (No ProdSec @mention: ProdSec Jira account ID not configured.)
>
> ---
> _Comment Footnote per shared/comment-footnote.md (skill: triage-security)_

## Steps 4–6 (affecting the final scope)

- **Step 4 (siblings):** JQL `project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004` returns empty (per the eval assumption). There are no duplicates and no companion trackers, so no links are created.
- **Step 4.3 (cross-CVE overlap):** skipped because the Upstream Affected Component, PS Component, and Stream fields are not configured.
- **Step 4.4 (preemptive reconciliation):** no siblings or preemptive tasks found, so there is nothing to reconcile.
- **Step 5 (lifecycle):** the product pages URL (https://access.example.com/product-life-cycle/rhtpa) was not fetched in the eval. 2.1.x is assumed to be within support. **Verify before task creation**: if 2.1.x is EOL, the remaining affected set is empty and the outcome changes to closure.
- **Step 6 (already fixed):** no resolved siblings, so this does not apply.
