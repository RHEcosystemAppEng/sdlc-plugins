# Step 4.5 -- Affects Version Resolution

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is already populated. This was recorded during Step 1 metadata extraction.

**Current value:** `Affects Version/s: 0.9.0`

Per Step 4.5.1 of the skill, when the field is already populated, the user must be presented with options:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

### Resolution

Since the Affects Version/s field is already set to `0.9.0` on ACME-500, the skill detects
this pre-existing value and presents the Keep/Replace/Augment prompt to the user before
proceeding.

**How each option would be handled:**

- **Option 1 (Keep):** The existing value `0.9.0` is preserved as-is. Steps 4.5.2 through
  4.5.5 are skipped entirely. Proceed directly to Step 5 (Generate Task).

- **Option 2 (Replace):** Continue to Step 4.5.2 to extract version information from the
  Environment / Version section (which is missing in this bug -- see note below), then
  Steps 4.5.3-4.5.5 to discover, match, and confirm a new version. The existing value
  would be cleared and replaced.

- **Option 3 (Augment):** Continue to Steps 4.5.2-4.5.5 to identify additional versions.
  Any confirmed version would be merged with the existing `0.9.0` using:
  ```
  jira.edit_issue(ACME-500, fields={
    "versions": [{"name": "0.9.0"}, {"name": "<additional-version>"}]
  })
  ```

### Note on Missing Environment / Version Section

The bug description does not contain an `### **Environment / Version**` section. If the user
chose Option 2 (Replace) or Option 3 (Augment), Step 4.5.2 would find no version text to
extract from the description, and Step 4.5.6 (Flag gap) would apply -- a comment would be
posted on the Bug:

> "Affects Version could not be determined from the bug description -- please set manually."

However, since the field is already populated, the recommended path is **Option 1 (Keep)**,
which preserves the existing `0.9.0` value without requiring version extraction from the
description.

### Steps Skipped (assuming Keep)

- 4.5.2 (Extract version from description) -- skipped
- 4.5.3 (Discover available Jira versions) -- skipped
- 4.5.4 (Match) -- skipped
- 4.5.5 (Confirm with user) -- skipped
- 4.5.6 (Flag gap) -- not applicable
