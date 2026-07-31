# Step 4.5 -- Affects Version Resolution: ACME-500

## 4.5.1 -- Check Existing Field

The `affectsVersions` field on ACME-500 was recorded during Step 1 metadata extraction.

**Existing value detected**: The Affects Version/s field is already populated with **0.9.0**.

Since the field is already set, the skill presents the following prompt to the user before proceeding:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

### Option Outcomes

- **Option 1 (Keep)**: The current value "0.9.0" is preserved as-is. Steps 4.5.2 through 4.5.6 are skipped entirely. Proceed directly to Step 5 (Generate Task).

- **Option 2 (Replace)**: The current value "0.9.0" is cleared. Proceed to Step 4.5.2 to extract a new version from the description's Environment / Version section (if present), then through Steps 4.5.3-4.5.5 to discover available Jira versions, match, confirm with the user, and set the replacement value.

- **Option 3 (Augment)**: The current value "0.9.0" is retained. Proceed to Steps 4.5.2-4.5.5 to identify additional version(s) to add. When updating the field, merge the new version(s) with the existing "0.9.0" so all values are preserved.

## Resolution

The skill waits for user input at this point. It does NOT silently overwrite or skip the existing value.

### Note on Environment / Version Section

The bug description for ACME-500 does not contain an Environment / Version section. If the user selects Option 2 (Replace) or Option 3 (Augment), Step 4.5.2 would find no version information to extract from the description, and Step 4.5.6 (Flag Gap) would apply -- posting a comment that Affects Version could not be determined from the bug description. For Option 2 this would mean the existing value is cleared with no replacement (the user would need to set it manually). For Option 3 no additional versions would be added and the existing value remains.

Given that "0.9.0" is already set and the description lacks version info, Option 1 (Keep) is the most practical choice for this bug.
