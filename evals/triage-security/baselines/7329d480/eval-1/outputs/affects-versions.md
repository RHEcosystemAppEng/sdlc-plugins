# Step 3 -- Affects Versions Correction

## Current Affects Versions

| Jira Field Value |
|------------------|
| RHTPA 2.0.0 |

## Analysis

The current Affects Versions value **RHTPA 2.0.0** is incorrect:

1. **No 2.0.x stream exists** -- the configured Version Streams are 2.1.x and 2.2.x. There is no stream covering a 2.0.0 product version, so RHTPA 2.0.0 is not a valid version for this product.
2. **Issue is scoped to 2.2.x** -- the summary suffix `[rhtpa-2.2]` scopes this issue to the 2.2.x stream only. Affects Versions should reflect only 2.2.x versions that are actually affected based on lock file evidence.
3. **Lock file evidence** shows the following 2.2.x versions ship vulnerable quinn-proto (< 0.11.14):
   - RHTPA 2.2.0 (quinn-proto 0.11.9)
   - RHTPA 2.2.1 (quinn-proto 0.11.12)
   - RHTPA 2.2.2 (retag of 2.2.1, same quinn-proto 0.11.12)
4. **2.2.3 and 2.2.4 are NOT affected** -- they ship quinn-proto 0.11.14 (the fixed version).

## Proposed Correction

**Remove:**
- RHTPA 2.0.0 (invalid -- no 2.0.x stream exists)

**Add:**
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

**Corrected Affects Versions:** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Proposed Jira Mutation

```
jira.edit_issue("TC-8001", versions=[
  { "name": "RHTPA 2.2.0" },
  { "name": "RHTPA 2.2.1" },
  { "name": "RHTPA 2.2.2" }
])
```

This replaces the entire Affects Versions field (removing RHTPA 2.0.0 and setting the corrected values). Requires engineer confirmation before execution.
