# Step 4.5 -- Affects Version Resolution: ACME-500

## 4.5.1 -- Check Existing Field

The bug issue ACME-500 already has the `Affects Version/s` field populated.

**Existing value recorded in Step 1**: `0.9.0`

Per Step 4.5.1 of the triage-bug procedure, when `affectsVersions` is already populated
with one or more versions, the skill must display the existing value(s) and present
the user with three options. The skill does NOT silently overwrite or skip the existing value.

### User Prompt (would be presented)

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

### Option Analysis

**Option 1 -- Keep**: The existing value `0.9.0` would be left as-is. Steps 4.5.2 through
4.5.5 would be skipped entirely, and the skill would proceed directly to Step 5 (Generate Task).
This is the recommended path when the reporter has already correctly identified the affected version.

**Option 2 -- Replace**: The existing value would be cleared. The skill would then proceed
to Step 4.5.2 to attempt version extraction from the Environment / Version section of the
description. Since this section is missing from ACME-500's description, the skill would
fall through to Step 4.5.6 (gap flagging) and post a comment asking the user to set the
version manually. Alternatively, the skill would present the available Jira versions
(from Step 4.5.3) for the user to select from.

**Option 3 -- Augment**: The existing value `0.9.0` would be retained, and additional
versions would be merged alongside it. The skill would proceed to Step 4.5.2 through 4.5.5
to discover and confirm additional affected versions. The final `edit_issue` call would
include both the existing and new version(s) in the `versions` array.

### Resolution

The skill awaits user input before proceeding. No modification to the Affects Version/s
field is made without explicit user confirmation.

Since the Environment / Version section is missing from the bug description (noted in
Step 1 parsing), and the Affects Version/s field is already set to `0.9.0`, the most
appropriate recommendation for the user is **Option 1 -- Keep**, which preserves the
existing value and proceeds to Task generation.

### Why the Skill Must Not Skip or Overwrite

The triage-bug procedure explicitly requires user interaction at this decision point:

1. **No silent overwrite**: If the skill were to run Steps 4.5.2-4.5.5 without checking
   the existing value, it could replace a carefully set version with an incorrect extraction.
2. **No silent skip**: If the skill skipped Step 4.5 entirely because a value exists, the
   user would have no opportunity to correct an incorrect existing value or add additional
   affected versions.
3. **User agency**: The three-option prompt ensures the user retains control over version
   metadata while benefiting from the skill's automated version discovery capabilities.
