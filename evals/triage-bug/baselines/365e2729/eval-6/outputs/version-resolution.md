# Step 4.5 – Affects Version Resolution: ACME-500

## 4.5.1 – Check existing field

Step 1 found that the Bug's `affectsVersions` (`versions`) field is **already populated**:

- Existing Affects Version/s: **`0.9.0`**

The field already has a value, so the skill does **not** overwrite it and does **not** skip
it silently. It shows the current value and asks the user how to proceed:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep — leave the current value and skip to Step 5
2. Replace — clear and set a new value
3. Augment — add additional versions alongside the current ones

Choose (1/2/3):
```

**Execution pauses here until the user answers.** No `jira.edit_issue` call is made before
the user responds.

## What happens for each choice

| Choice | Behaviour |
|---|---|
| **1. Keep** | Skip sub-steps 4.5.2–4.5.6. ACME-500 keeps `0.9.0` unchanged. Continue to Step 5. |
| **2. Replace** | Run 4.5.2–4.5.5: extract a version from the description, discover Jira versions with `getJiraIssueTypeMetaWithFields(projectIdOrKey: "ACME", issueTypeId: "10020")`, match, confirm with the user, then `jira.edit_issue("ACME-500", fields={"versions": [{"id": "<new-version-id>"}]})` with the new value only. |
| **3. Augment** | Same discovery, match and confirm flow, then merge: `jira.edit_issue("ACME-500", fields={"versions": [{"id": "<existing-0.9.0-id>"}, {"id": "<additional-version-id>"}]})`, keeping `0.9.0`. |

### Note for Replace / Augment

ACME-500's description has **no** `### **Environment / Version**` section (see
bug-parsing.md), so sub-step 4.5.2 cannot pull a version from the description. If the user
picks Replace or Augment, the skill would:

- show the available Jira versions list (from 4.5.3) and ask the user to select one, or enter
  one by hand, following the "no" path of 4.5.5; or
- if the user gives no selection, fall back to 4.5.6 and post the gap comment
  ("Affects Version could not be determined from the bug description — please set
  manually.", plus the Comment Footnote). For Replace this would leave the field cleared, so
  the existing value should be kept until the user explicitly provides a replacement.

## Outcome for this eval

No user input is available in this non-interactive eval, so the prompt above is the final
state of Step 4.5. The recommended default is **1. Keep**. The reporter's `0.9.0` is
consistent with the bug: the plan-feature convention lookup defect exists in that release,
and nothing in the investigation contradicts it. No Jira mutation is made to the
Affects Version field. Triage continues to Step 5.
