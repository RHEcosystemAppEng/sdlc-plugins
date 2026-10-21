# Step 4.5 -- Affects Version Resolution: ACME-500

## 4.5.1 -- Check Existing Field

The `affectsVersions` field on ACME-500 is **already populated** with the value `0.9.0`. This was recorded during Step 1 metadata extraction.

Because the field is already set, the skill does NOT proceed directly to version extraction or Jira version discovery. Instead, it presents the existing value to the user and asks how to proceed.

### User Prompt

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep -- leave the current value and skip to Step 5
2. Replace -- clear and set a new value
3. Augment -- add additional versions alongside the current ones

Choose (1/2/3):
```

### Option Analysis

| Option | Behavior | Jira API Action |
|--------|----------|-----------------|
| 1. Keep | Accept `0.9.0` as correct. Skip sub-steps 4.5.2 through 4.5.6 entirely. Proceed to Step 5. | None -- no Jira mutation |
| 2. Replace | Clear the current value and run sub-steps 4.5.2-4.5.5 to determine and set a new version. | `jira.edit_issue(ACME-500, fields={"versions": [{"id": "<new-version-id>"}]})` |
| 3. Augment | Keep `0.9.0` and run sub-steps 4.5.2-4.5.5 to find additional affected versions to add alongside. | `jira.edit_issue(ACME-500, fields={"versions": [{"name": "0.9.0"}, {"id": "<additional-version-id>"}]})` -- merges existing with new |

### Key Constraint

The skill MUST NOT silently overwrite or skip the existing Affects Version/s value. It waits for user input before taking any action. This ensures that:

1. Human-set values are respected
2. The user retains control over version metadata
3. No data is lost through silent overwrites

### Environment / Version Section

The bug description does **not** include an `### **Environment / Version**` section. If the user selects option 2 (Replace) or 3 (Augment), sub-step 4.5.2 would find no version text to extract from the description. In that case, sub-step 4.5.6 (gap flagging) would apply -- a comment would be posted on ACME-500 asking the user to set the version manually.

However, since the `affectsVersions` field is already populated, the expected user choice in this scenario is **1. Keep**, which skips all remaining sub-steps and proceeds directly to Step 5.

### Flow Diagram

```
Step 4.5.1: Check existing field
  |
  +-- affectsVersions is populated: [0.9.0]
  |
  +-- Present three options to user
  |
  +-- [1. Keep] --> Skip to Step 5 (no Jira mutation)
  |
  +-- [2. Replace] --> 4.5.2 (extract from description)
  |     +-- No Environment/Version section found
  |     +-- 4.5.6 (flag gap, post comment)
  |
  +-- [3. Augment] --> 4.5.2 (extract from description)
        +-- No Environment/Version section found
        +-- 4.5.6 (flag gap, post comment, keep existing 0.9.0)
```
