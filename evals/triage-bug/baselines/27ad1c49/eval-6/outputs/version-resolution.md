# Step 4.5 -- Affects Version Resolution: ACME-500

## 4.5.1 -- Check Existing Field

The bug issue ACME-500 has the `affectsVersions` Jira field **already populated**.

**Current value**: 0.9.0

Per Step 1 metadata extraction, `Affects Version/s: 0.9.0` was recorded on the issue. The skill detects this existing value and must present it to the user before proceeding.

### User Prompt

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

### Behavior

The skill **WAITS for user input** at this point. It does NOT silently overwrite the existing value, nor does it silently skip version resolution. The three options are:

1. **Keep** -- Accept the current value `0.9.0` as-is. Skip sub-steps 4.5.2 through 4.5.5 entirely and proceed directly to Step 5 (Generate Task). The Jira field remains unchanged.

2. **Replace** -- Clear the current `0.9.0` value and determine a new value. This would proceed to sub-step 4.5.2 (extract version from description). However, since the Environment / Version section is **missing** from the bug description, sub-step 4.5.2 would find no version information to extract, and the flow would fall through to sub-step 4.5.6 (gap flagging), which would post a comment:
   > "Affects Version could not be determined from the bug description -- please set manually."

3. **Augment** -- Keep the current `0.9.0` value and add additional versions alongside it. This would also proceed to sub-step 4.5.2 to extract additional version info. Again, the missing Environment / Version section means no additional version can be extracted, leading to sub-step 4.5.6 gap flagging.

### Key Observations

- The `affectsVersions` field is populated from Jira issue metadata, NOT from the bug description body. These are independent data sources.
- The Environment / Version description section is missing, but this does not affect the existing Jira field value.
- For Options 2 (Replace) and 3 (Augment), the missing description section creates a secondary issue: no version text can be extracted from the description to use as a replacement or augmentation value.
- The most likely user choice is **1. Keep**, since the field is already correctly set and the description lacks additional version information.

### Resolution (Awaiting User Input)

**No action taken on the Affects Version field.** The skill is paused at this step, waiting for the user to choose one of the three options. No Jira API calls are made to modify the `versions` field until the user responds.

## Sub-steps 4.5.2 through 4.5.6 -- Conditional on User Choice

These sub-steps are NOT executed unless the user chooses Option 2 (Replace) or Option 3 (Augment):

- **4.5.2 (Extract version from description)**: Would attempt to parse the Environment / Version section. Since this section is missing from ACME-500, no version pattern can be extracted. Flow would skip to 4.5.6.
- **4.5.3 (Discover available Jira versions)**: Would call `jira.getJiraIssueTypeMetaWithFields` to list available project versions. Not reached if 4.5.2 yields nothing.
- **4.5.4 (Match)**: Would compare extracted text against available versions. Not reached.
- **4.5.5 (Confirm with user)**: Would present matched version for confirmation. Not reached.
- **4.5.6 (Flag gap)**: Would be triggered if Options 2 or 3 are chosen, since no version info can be extracted from the description. Would post a comment on ACME-500:
  > "Affects Version could not be determined from the bug description -- please set manually."
