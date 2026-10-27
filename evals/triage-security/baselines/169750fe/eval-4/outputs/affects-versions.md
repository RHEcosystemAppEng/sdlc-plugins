# Step 3 -- Affects Versions Correction: TC-8004

## Current Affects Versions (PSIRT-assigned)

RHTPA 2.1.0, RHTPA 2.2.0

## Lock File Evidence

Based on the version impact analysis, the actual impact is:

| Version | h2 version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | **YES** -- ships h2 < 0.4.8 |
| RHTPA 2.1.1 | 0.4.5 | **YES** -- ships h2 < 0.4.8 |
| RHTPA 2.2.0 | 0.4.8 | **NO** -- ships h2 >= 0.4.8 (fixed version) |
| RHTPA 2.2.1 | 0.4.8 | **NO** -- ships h2 >= 0.4.8 |
| RHTPA 2.2.2 | -- | **NO** -- retag of 2.2.1 |
| RHTPA 2.2.3 | 0.4.9 | **NO** -- ships h2 >= 0.4.8 |
| RHTPA 2.2.4 | 0.4.9 | **NO** -- ships h2 >= 0.4.8 |

## Correction Required

The PSIRT-assigned Affects Versions are **incorrect**:

- **RHTPA 2.2.0 should be REMOVED** -- this version ships h2 0.4.8 (the fixed version) and is not affected.
- **RHTPA 2.1.1 should be ADDED** -- this version ships h2 0.4.5 and is affected but was not included by PSIRT.

## Corrected Affects Versions

**RHTPA 2.1.0, RHTPA 2.1.1**

Only 2.1.x versions are affected. All 2.2.x versions ship h2 >= 0.4.8 and are not vulnerable.

## Proposed Jira Update

```
jira.edit_issue("TC-8004", {
  "versions": [
    { "name": "RHTPA 2.1.0" },
    { "name": "RHTPA 2.1.1" }
  ]
})
```

## Affects Versions Correction Comment

The following comment would be posted to TC-8004:

> **Affects Versions correction** (lock file evidence):
>
> Removed: RHTPA 2.2.0 (ships h2 0.4.8 -- at fix threshold, not affected)
> Added: RHTPA 2.1.1 (ships h2 0.4.5 -- within affected range < 0.4.8)
>
> Corrected Affects Versions: RHTPA 2.1.0, RHTPA 2.1.1
>
> Evidence: `git show <tag>:Cargo.lock` for each pinned source commit in the supportability matrix.
> All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8 and are not affected by CVE-2026-33501.
