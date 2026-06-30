# Step 3 - Affects Versions Correction: TC-8001

## Current vs Proposed

| Attribute | Value |
|-----------|-------|
| Current Affects Versions (PSIRT-assigned) | RHTPA 2.0.0 |
| Issue stream scope | 2.2.x (from summary suffix `[rhtpa-2.2]`) |

## Problem

PSIRT assigned `RHTPA 2.0.0` as the Affects Version, but there is no 2.0.x version stream in the project configuration. The Version Streams table only contains 2.1.x and 2.2.x streams. The PSIRT-assigned version is incorrect.

## Version Impact (scoped to 2.2.x stream)

| Version | quinn-proto | Affected? | Include in Affects Versions? |
|---------|-------------|-----------|------------------------------|
| 2.2.0 | 0.11.9 | YES | YES |
| 2.2.1 | 0.11.12 | YES | YES |
| 2.2.2 | 0.11.12 | YES | YES (retag of 2.2.1) |
| 2.2.3 | 0.11.14 | NO | NO (ships fixed version) |
| 2.2.4 | 0.11.14 | NO | NO (ships fixed version) |

Note: Versions 2.1.0 and 2.1.1 are also affected but belong to stream 2.1.x, which is outside this issue's scope. Cross-stream impact is handled in Step 7 Case B.

## Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: Lock file analysis at pinned commits from security-matrix.md shows quinn-proto versions 0.11.9 and 0.11.12 in versions 2.2.0 through 2.2.2, all of which are below the fix threshold of 0.11.14. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 and are not affected. The original PSIRT-assigned version `RHTPA 2.0.0` does not correspond to any configured version stream and is incorrect. Correction is scoped to the 2.2.x stream per the issue suffix `[rhtpa-2.2]`.

## Jira Mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})

jira.add_comment("TC-8001",
  "Corrected Affects Versions: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
  Based on lock file analysis at pinned commits from security-matrix.md.
  Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
  RHTPA 2.0.0 does not match any configured version stream and was removed.")
```
