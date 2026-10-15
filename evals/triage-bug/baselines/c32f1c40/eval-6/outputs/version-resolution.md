# Step 4.5 -- Affects Version Resolution: ACME-500

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field is **already populated**.

**Current value**: 0.9.0

Per the triage-bug skill (Step 4.5.1), when the field is already set, the user
must be presented with options before any modification.

### User Prompt

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

**Action required**: Awaiting user input before proceeding.

- If **1. Keep**: Skip sub-steps 4.5.2 through 4.5.6 and proceed directly to Step 5 (Generate Task). The existing value `0.9.0` remains unchanged.
- If **2. Replace**: Proceed to sub-step 4.5.2 to extract a version from the description, then 4.5.3 to discover available Jira versions, 4.5.4 to match, and 4.5.5 to confirm with user before clearing and setting a new value.
- If **3. Augment**: Proceed to sub-steps 4.5.2 through 4.5.5, then merge the new version(s) with the existing `0.9.0` value when updating the field.

## 4.5.2 -- Version Extraction (conditional on user choice 2 or 3)

The bug description does **not** contain an `### **Environment / Version**` section.
However, the issue metadata already records `Affects Version/s: 0.9.0`.

If the user chose Replace or Augment, the absence of an Environment / Version
section in the description means no new version can be extracted from the
description body. In that case:

- The existing metadata value `0.9.0` serves as the only version reference.
- Sub-step 4.5.6 (gap flagging) would apply for the description-extraction path,
  but since the field already has a value, the gap flag is informational only.

## 4.5.3 -- Discover Available Jira Versions (conditional)

Would call:
```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```
to retrieve available versions for matching.

## 4.5.4 -- Match (conditional)

Would match extracted version `0.9.0` against available Jira version names
using substring matching.

## 4.5.5 -- Confirm (conditional)

Would present matched version and ask for confirmation before updating.

## Resolution

The existing `Affects Version/s: 0.9.0` value is detected and presented to the user
with Keep/Replace/Augment options. The skill does **not** silently overwrite or skip
the existing value -- it waits for explicit user input before taking any action on
the field.
