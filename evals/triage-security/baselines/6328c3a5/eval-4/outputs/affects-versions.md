# Affects Versions Correction — TC-8004

## Step 3: Affects Versions Analysis

### Current PSIRT-Assigned Affects Versions

| Jira Version | In Issue? |
|--------------|-----------|
| RHTPA 2.1.0 | Yes |
| RHTPA 2.2.0 | Yes |

### Version Impact Evidence (from lock file analysis)

| Jira Version | h2 Version | Affected? | Should Be in Affects Versions? |
|--------------|------------|-----------|-------------------------------|
| RHTPA 2.1.0 | 0.4.5 | **YES** | **YES** |
| RHTPA 2.1.1 | 0.4.5 | **YES** | **YES** |
| RHTPA 2.2.0 | 0.4.8 | NO | NO |
| RHTPA 2.2.1 | 0.4.8 | NO | NO |
| RHTPA 2.2.2 | _(retag)_ | NO | NO |
| RHTPA 2.2.3 | 0.4.9 | NO | NO |
| RHTPA 2.2.4 | 0.4.9 | NO | NO |

### Correction Required

The PSIRT-assigned Affects Versions are **incorrect**:

- **RHTPA 2.2.0** should be **removed** -- version 2.2.0 ships h2 0.4.8, which is the fixed version and is NOT affected.
- **RHTPA 2.1.1** should be **added** -- version 2.1.1 ships h2 0.4.5, which is within the vulnerable range (< 0.4.8).

### Proposed Correction

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Rationale**: Since this issue is **unscoped** (no stream suffix), Affects Versions should include all actually affected versions across all streams. Lock file analysis at pinned commits from the supportability matrix confirms that only 2.1.x versions ship the vulnerable h2 dependency (0.4.5 < 0.4.8). All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.

### Scope Note

This is an unscoped issue covering all streams. The Affects Versions correction includes only versions that are actually affected based on lock file evidence, regardless of stream. The 2.2.x stream versions are excluded because they ship the patched h2 dependency.
