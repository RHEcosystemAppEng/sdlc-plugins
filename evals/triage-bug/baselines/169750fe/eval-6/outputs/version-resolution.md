# Affects Version Resolution -- Step 4.5

## 4.5.1 -- Check Existing Field

The `affectsVersions` field on ACME-500 is **already populated** with a value recorded during Step 1 metadata extraction.

**Existing value:** 0.9.0

Per the skill protocol (Step 4.5.1), when `affectsVersions` is already populated, the skill must display the current value and present the user with three options rather than silently overwriting or skipping:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

**The skill WAITS for user input at this point.** It does not:
- Silently skip the Affects Version step
- Silently overwrite the existing value
- Proceed to sub-step 4.5.2 without user confirmation

## Decision Tree Based on User Choice

### If user chooses "1. Keep"

- The existing value "0.9.0" is retained as-is on ACME-500.
- Sub-steps 4.5.2 through 4.5.6 are skipped entirely.
- Proceed directly to Step 5 (Generate Task).

### If user chooses "2. Replace"

- The existing value "0.9.0" will be cleared.
- Proceed to sub-step 4.5.2 to extract version from the description's Environment / Version section.
- Note: In this case, the Environment / Version section is missing from the description, so sub-step 4.5.2 would find no version text and fall through to sub-step 4.5.6 (gap flagging), unless the user provides a version manually.
- Continue through sub-steps 4.5.3 (discover available Jira versions), 4.5.4 (match), 4.5.5 (confirm with user).

### If user chooses "3. Augment"

- The existing value "0.9.0" is retained.
- Proceed to sub-step 4.5.2 to extract additional version info from the description.
- Any newly matched versions would be merged with the existing "0.9.0" value.
- The `versions` field update would include both the existing and new version entries.
- Continue through sub-steps 4.5.3, 4.5.4, 4.5.5.

## Key Behavior

The critical aspect of Step 4.5.1 is that the skill **respects the existing value** and **defers to the user**. The three-option prompt ensures that:

1. Pre-existing version metadata is never silently lost (no overwrite without consent)
2. Pre-existing version metadata is never silently ignored (the user is informed it exists)
3. The user retains full control over whether to keep, replace, or augment the value
4. The workflow does not stall -- the user can quickly choose "Keep" to move forward
