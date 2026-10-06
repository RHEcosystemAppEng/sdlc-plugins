# Step 4.5 -- Affects Version Resolution

## Step 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field was recorded during Step 1 metadata extraction.

**Detection result**: The `affectsVersions` field is already populated with one or more values.

- **Existing value**: 0.9.0

Because the field is already populated, the skill presents the following prompt to the user rather than attempting to extract and set a new version:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep — leave the current value and skip to Step 5
2. Replace — clear and set a new value
3. Augment — add additional versions alongside the current ones

Choose (1/2/3):
```

**Action**: The skill stops and waits for user input before proceeding.

- If the user chooses **1. Keep**: skip sub-steps 4.5.2 through 4.5.6 and proceed directly to Step 5 (Generate Task). The existing value "0.9.0" remains unchanged.
- If the user chooses **2. Replace**: proceed to sub-step 4.5.2 to extract a version from the description, then 4.5.3 to discover available Jira versions, 4.5.4 to match, and 4.5.5 to confirm with the user before clearing the existing value and setting the new one.
- If the user chooses **3. Augment**: proceed to sub-steps 4.5.2 through 4.5.5 as with Replace, but merge the new version(s) with the existing "0.9.0" rather than clearing it.

The skill does NOT silently overwrite or skip the existing value. It requires explicit user input to determine how to handle the pre-existing Affects Version/s.
