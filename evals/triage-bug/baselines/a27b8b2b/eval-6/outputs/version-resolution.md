# Step 4.5 -- Affects Version Resolution: ACME-500

## Step 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field was recorded in Step 1 metadata extraction.

**Existing value detected**: Yes

The Affects Version/s field on ACME-500 is already populated with: **0.9.0**

Per the skill specification (Step 4.5.1), when the field is already populated, the user must be presented with options rather than silently overwriting or skipping.

### User Prompt

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

### Resolution

**Awaiting user input.** The skill does NOT silently overwrite the existing value and does NOT skip without user confirmation.

- If the user chooses **1. Keep**: The current value "0.9.0" is retained. Sub-steps 4.5.2 through 4.5.6 are skipped entirely. Proceed to Step 5.
- If the user chooses **2. Replace**: Proceed to sub-step 4.5.2 to extract a new version from the description. Since the Environment / Version section is missing from the bug description, sub-step 4.5.2 would find no version information, which would trigger sub-step 4.5.6 (gap flagging) to post a comment asking for manual version entry.
- If the user chooses **3. Augment**: Proceed to sub-step 4.5.2 to extract additional version(s). The new version(s) would be merged with the existing "0.9.0" value. Again, since Environment / Version is missing, this would trigger sub-step 4.5.6.

## Sub-steps 4.5.2--4.5.6 (Conditional)

These sub-steps are only executed if the user chooses "Replace" or "Augment" in Step 4.5.1.

### Step 4.5.2 -- Extract version from description (if Replace or Augment)

The **Environment / Version** section is missing from the bug description. No version text can be extracted from this section.

**Result**: No version pattern found. Skip to sub-step 4.5.6 (gap flagging).

### Step 4.5.3 -- Discover available Jira versions (if Replace or Augment)

Would call:
```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```
to retrieve available versions. Not executed in this eval.

### Step 4.5.4 -- Match (if Replace or Augment)

Skipped -- no version text extracted in sub-step 4.5.2.

### Step 4.5.5 -- Confirm with user (if Replace or Augment)

Skipped -- no match to confirm.

### Step 4.5.6 -- Flag gap (if Replace or Augment)

Since no version information could be extracted from the description, a comment would be posted:

```
jira.add_comment(ACME-500, "Affects Version could not be determined from the
bug description -- please set manually.")
```

With the Comment Footnote appended.

## Summary

| Check | Result |
|-------|--------|
| affectsVersions already populated? | Yes -- "0.9.0" |
| Step 4.5.1 triggered? | Yes -- existing value detected |
| Options presented to user? | Yes -- Keep / Replace / Augment |
| Silent overwrite? | No -- user input required |
| Silent skip? | No -- user input required |
| Environment / Version section present? | No -- missing from description |
| Sub-steps 4.5.2--4.5.6 needed? | Only if user chooses Replace or Augment |
