# Step 4.5 -- Affects Version Resolution: ACME-500

## 4.5.1 -- Check Existing Field

The bug's `affectsVersions` field was recorded in Step 1 metadata extraction as **already populated**.

**Current value:** `0.9.0`

### User Prompt

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

**Resolution:** The existing value `0.9.0` is displayed to the user. The skill does NOT silently overwrite or skip the existing value. Execution pauses here and waits for user input before proceeding.

### Option Outcomes

- **If user chooses 1 (Keep):** The current Affects Version/s value of `0.9.0` is retained as-is. Steps 4.5.2 through 4.5.6 are skipped entirely. Proceed directly to Step 5 (Generate Task).

- **If user chooses 2 (Replace):** Proceed to Step 4.5.2 to extract a version from the description's Environment / Version section. Since that section is missing from the bug description, this would fall through to Step 4.5.6 (Flag gap) unless the user provides a version manually during the confirmation step (4.5.5).

- **If user chooses 3 (Augment):** Proceed to Step 4.5.2 to extract additional version(s). Any new version(s) confirmed by the user in Step 4.5.5 would be merged with the existing `0.9.0` value using:
  ```
  jira.edit_issue(ACME-500, fields={
    "versions": [
      {"name": "0.9.0"},
      {"id": "<new-version-id>"}
    ]
  })
  ```

## 4.5.2 -- Extract Version from Description (conditional)

The bug description does not contain a `### **Environment / Version**` section. If the user chose Replace or Augment, version extraction from the description would yield no result, falling through to Step 4.5.6 (Flag gap) or prompting the user to select from available Jira versions manually.

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

Then present available versions in a table for user selection.

## 4.5.4 -- Match (conditional)

Would compare extracted version text against available Jira version names using substring matching.

## 4.5.5 -- Confirm with User (conditional)

Would present matched version(s) and ask for confirmation (yes/no/skip).

## 4.5.6 -- Flag Gap (conditional)

If no version can be extracted from the description and user chose Replace or Augment, a comment would be posted:
```
jira.add_comment(ACME-500, "Affects Version could not be determined from the
bug description -- please set manually.")
```

## Summary

The key behavior demonstrated here is that the skill **detects the existing Affects Version/s value** of `0.9.0` already set on ACME-500, **presents it to the user**, and **offers three explicit options** (Keep, Replace, Augment) rather than silently overwriting or ignoring the existing value. The skill waits for user input before proceeding.
