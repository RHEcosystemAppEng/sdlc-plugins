# Step 4.5 -- Affects Version Resolution: ACME-500

## Step 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **already populated** with the value `0.9.0`, as recorded during Step 1 metadata extraction.

Per the skill's Step 4.5.1 logic, when `affectsVersions` is already set, the skill MUST NOT silently overwrite or skip the field. Instead, it must display the current value and present the user with three options:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

### Decision Flow

- **If user chooses "1. Keep"**: Skip sub-steps 4.5.2 through 4.5.5 entirely. Proceed directly to Step 5 (Generate Task). The existing value `0.9.0` remains unchanged on the issue.

- **If user chooses "2. Replace"**: Continue to sub-step 4.5.2 to extract a new version from the description, then 4.5.3 to discover available Jira versions, 4.5.4 to match, and 4.5.5 to confirm. The old value is cleared and replaced with the new confirmed value.

- **If user chooses "3. Augment"**: Continue to sub-steps 4.5.2-4.5.5 as with Replace, but when updating the field in 4.5.5, merge the new version(s) with the existing `0.9.0` rather than replacing it. The `edit_issue` call would include both the existing and new version(s) in the `versions` array.

### Environment / Version Section Analysis

Note: The bug description does NOT contain an `### **Environment / Version**` section. If the user chose "2. Replace" or "3. Augment", sub-step 4.5.2 would find no version information in the description body. This would trigger sub-step 4.5.6 (Flag gap), posting a comment:

> "Affects Version could not be determined from the bug description -- please set manually."

However, since the field is already populated and the user is presented with the Keep/Replace/Augment prompt FIRST, the most likely and recommended action is **"1. Keep"** -- the existing value of `0.9.0` is already set and should be preserved.

### Key Behavior: No Silent Overwrite

The critical requirement tested by this eval is that the skill:
1. **Detects** that `affectsVersions` is already set (value: `0.9.0`)
2. **Presents** the Keep/Replace/Augment options to the user
3. **Does NOT** silently overwrite the existing value
4. **Does NOT** silently skip version resolution without acknowledging the existing value
5. **Waits** for user input before proceeding

This ensures human oversight over version field changes, preventing accidental data loss when a reporter or project manager has already set the correct version.
