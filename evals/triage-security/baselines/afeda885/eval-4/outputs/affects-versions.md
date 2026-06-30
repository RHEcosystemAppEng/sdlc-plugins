# Affects Versions Correction — TC-8004

## Step 3: Affects Versions Analysis

### Current Affects Versions (PSIRT-assigned)

| Jira Version | In Issue? |
|--------------|-----------|
| RHTPA 2.1.0 | YES |
| RHTPA 2.2.0 | YES |

### Version Impact Evidence (from lock file analysis)

| Version | Stream | h2 Version | Affected? |
|---------|--------|------------|-----------|
| 2.1.0 | 2.1.x | 0.4.5 | **YES** |
| 2.1.1 | 2.1.x | 0.4.5 | **YES** |
| 2.2.0 | 2.2.x | 0.4.8 | NO |
| 2.2.1 | 2.2.x | 0.4.8 | NO |
| 2.2.2 | 2.2.x | -- | NO (retag of 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO |
| 2.2.4 | 2.2.x | 0.4.9 | NO |

### Correction Required

The issue is **unscoped** (no stream suffix), so Affects Versions should include
all actually affected versions across all streams.

**PSIRT incorrectly included RHTPA 2.2.0**: the 2.2.x stream ships h2 >= 0.4.8,
which is at or above the fix threshold. RHTPA 2.2.0 is NOT affected.

**PSIRT missed RHTPA 2.1.1**: version 2.1.1 also ships h2 0.4.5 (vulnerable) but
was not included in the original Affects Versions.

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

### Changes

| Action | Version | Reason |
|--------|---------|--------|
| KEEP | RHTPA 2.1.0 | h2 0.4.5 < 0.4.8 -- affected |
| ADD | RHTPA 2.1.1 | h2 0.4.5 < 0.4.8 -- affected but missing from PSIRT assignment |
| REMOVE | RHTPA 2.2.0 | h2 0.4.8 >= 0.4.8 -- not affected (ships patched version) |

### Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

### Correction Comment (to be posted on TC-8004)

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 — AFFECTED (< 0.4.8)
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 — AFFECTED (< 0.4.8) [added]
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 — NOT AFFECTED (>= 0.4.8) [removed]

This is an unscoped issue — Affects Versions scoped to all actually affected
versions across all streams. The 2.2.x stream ships h2 >= 0.4.8 and is not affected.
```
