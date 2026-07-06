# Affects Versions Correction -- TC-8004

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.1.0
- RHTPA 2.2.0

## Lock File Evidence

| Version | h2 Version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | YES -- below fix threshold 0.4.8 |
| RHTPA 2.1.1 | 0.4.5 | YES -- below fix threshold 0.4.8 |
| RHTPA 2.2.0 | 0.4.8 | NO -- ships the fixed version |
| RHTPA 2.2.1 | 0.4.8 | NO -- ships the fixed version |
| RHTPA 2.2.2 | (retag of 2.2.1) | NO -- same as 2.2.1 |
| RHTPA 2.2.3 | 0.4.9 | NO -- above fix threshold |
| RHTPA 2.2.4 | 0.4.9 | NO -- above fix threshold |

## Proposed Correction

Since this is an **unscoped** issue (no stream suffix), the Affects Versions should reflect all actually-affected versions across all streams. Based on the lock file analysis:

**Remove:**
- RHTPA 2.2.0 -- ships h2 0.4.8 (the fix version), not affected

**Add:**
- RHTPA 2.1.1 -- ships h2 0.4.5, affected but missing from PSIRT assignment

**Corrected Affects Versions:**
- RHTPA 2.1.0
- RHTPA 2.1.1

## Rationale

PSIRT assigned Affects Versions based on scan time, listing RHTPA 2.1.0 and RHTPA 2.2.0. Lock file analysis at the pinned source commits shows:

1. **RHTPA 2.2.0 is not affected**: the backend tag v0.4.5 pins h2 at version 0.4.8, which is exactly the fix version. RHTPA 2.2.0 should be removed from Affects Versions.

2. **RHTPA 2.1.1 is affected but missing**: the backend tag v0.3.12 pins h2 at version 0.4.5, which is below the fix threshold. RHTPA 2.1.1 should be added to Affects Versions.

The correction scopes Affects Versions to the 2.1.x stream only, since the 2.2.x stream ships the patched h2 version in all releases.

## Proposed Jira Mutation

```
jira.edit_issue("TC-8004", {
  "versions": [
    { "name": "RHTPA 2.1.0" },
    { "name": "RHTPA 2.1.1" }
  ]
})
```

This requires engineer confirmation before execution.
