# Step 4.5 -- Affects Version Resolution: ACME-500

## 4.5.1 -- Check Existing Field

The `affectsVersions` field on ACME-500 was recorded during Step 1 metadata extraction as **already populated** with the value `0.9.0`.

Per the skill protocol, when the field is already populated, the user must be presented with three options. The skill must NOT silently overwrite or skip the existing value -- it must wait for user input.

### User Prompt

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

### Option Behaviors

**Option 1 -- Keep:**
- Leave the current `affectsVersions` value (`0.9.0`) unchanged on ACME-500.
- Skip sub-steps 4.5.2 through 4.5.6 entirely.
- Proceed directly to Step 5 (Generate Task).

**Option 2 -- Replace:**
- Clear the existing `affectsVersions` value.
- Proceed to sub-step 4.5.2 to extract a version from the description.
- Since the Environment / Version section is missing from the bug description (noted in Step 1), sub-step 4.5.2 would find no version pattern, triggering sub-step 4.5.6 (gap flagging).
- Alternatively, the user could select from available Jira versions (sub-step 4.5.3) and confirm manually.
- The Jira API call to set the new value would be:
  ```
  jira.edit_issue("ACME-500", fields={
    "versions": [{"id": "<selected-version-id>"}]
  })
  ```

**Option 3 -- Augment:**
- Retain the existing `affectsVersions` value (`0.9.0`).
- Proceed to sub-step 4.5.2 to extract additional version(s) from the description.
- Since the Environment / Version section is missing, the user would need to select additional versions from the available Jira versions list (sub-step 4.5.3).
- The Jira API call would merge new version(s) with the existing one:
  ```
  jira.edit_issue("ACME-500", fields={
    "versions": [
      {"name": "0.9.0"},
      {"id": "<additional-version-id>"}
    ]
  })
  ```

## 4.5.2 -- Extract Version from Description (conditional)

The **Environment / Version** section is **missing** from the bug description (as recorded in Step 1). No version pattern can be extracted from the description body.

If the user chose Replace or Augment, this sub-step would yield no result, and the flow would proceed to sub-step 4.5.3 (discover available Jira versions) for manual selection, or sub-step 4.5.6 (gap flagging).

## 4.5.3 -- Discover Available Jira Versions (conditional)

Would call:
```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```
or REST fallback:
```
python3 scripts/jira-client.py get_versions ACME
```

The available versions would be presented in a table for the user to select from.

## 4.5.6 -- Gap Flagging (conditional)

If Replace or Augment was chosen and no version could be extracted from the description (sub-step 4.5.2 found nothing) and the user did not manually select a version, a gap comment would be posted:

```
jira.add_comment("ACME-500", "Affects Version could not be determined from the
bug description -- please set manually.")
```

## Resolution Summary

The existing `Affects Version/s: 0.9.0` on ACME-500 is detected and surfaced to the user with three options (Keep, Replace, Augment). The skill does not silently overwrite or skip the value. The user's choice determines the subsequent flow. Since the Environment / Version section is absent from the description, Replace or Augment paths would rely on manual version selection from the Jira project's available versions.
