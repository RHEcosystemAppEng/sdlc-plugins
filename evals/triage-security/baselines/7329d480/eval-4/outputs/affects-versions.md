# Affects Versions Correction -- TC-8004

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.1.0
- RHTPA 2.2.0

## Lock File Evidence

| Version | h2 version shipped | Vulnerable (< 0.4.8)? |
|---------|--------------------|------------------------|
| RHTPA 2.1.0 | 0.4.5 | YES |
| RHTPA 2.1.1 | 0.4.5 | YES |
| RHTPA 2.2.0 | 0.4.8 | NO |
| RHTPA 2.2.1 | 0.4.8 | NO |
| RHTPA 2.2.2 | 0.4.8 | NO (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.4.9 | NO |
| RHTPA 2.2.4 | 0.4.9 | NO |

## Proposed Correction

**Remove**: RHTPA 2.2.0 -- ships h2 0.4.8, which is the fixed version (>= 0.4.8). Not affected.

**Add**: RHTPA 2.1.1 -- ships h2 0.4.5, which is vulnerable (< 0.4.8). Missing from PSIRT's assignment.

**Keep**: RHTPA 2.1.0 -- correctly identified as affected (h2 0.4.5).

## Corrected Affects Versions

- RHTPA 2.1.0
- RHTPA 2.1.1

## Rationale

PSIRT assigned Affects Versions based on scan time, not actual dependency analysis. Lock file inspection at pinned source commits reveals:

1. **RHTPA 2.2.0 is not affected**: Backend tag v0.4.5 pins h2 at exactly 0.4.8, which is the fixed version. The 2.2.x stream shipped the patched h2 from its first release.

2. **RHTPA 2.1.1 is missing**: Backend tag v0.3.12 pins h2 at 0.4.5, which is within the affected range (< 0.4.8). This version was omitted by PSIRT but is affected.

The corrected Affects Versions scopes the issue to only the actually affected versions in the 2.1.x stream.

## Jira Mutation (proposed)

```
jira.edit_issue("TC-8004", {
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

This correction requires engineer confirmation before execution.
