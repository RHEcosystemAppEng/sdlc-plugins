# Step 4.5 – Affects Version Resolution: ACME-500

## 4.5.1 – Check existing field

Step 1 recorded that `affectsVersions` (Jira `versions` field) on ACME-500 is **already populated**:

- Affects Version/s: **0.9.0**

Because the field already has a value, the skill does NOT set it automatically. It shows the current value and asks the user:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep — leave the current value and skip to Step 5
2. Replace — clear and set a new value
3. Augment — add additional versions alongside the current ones

Choose (1/2/3):
```

## Resolution

- **Selected / default action: 1. Keep.** No other version information exists that conflicts with or adds to the existing value. The description has no Environment / Version section, so nothing can be extracted to replace or augment with (see 4.5.2 below). The current value 0.9.0 is consistent with the bug report.
- Sub-steps 4.5.2–4.5.6 are **skipped** under "Keep":
  - No `getJiraIssueTypeMetaWithFields` / `get_versions` call is made.
  - No `jira.edit_issue(ACME-500, fields={"versions": [...]})` mutation is made. The existing value is left untouched and NOT overwritten.
  - No "Affects Version could not be determined" gap comment is posted. The field is already set, so there is no gap, even though the description lacks an Environment / Version section.
- Proceed to Step 5.

## If the user had chosen otherwise (for reference)

- **Replace**: run 4.5.2 (extract from Environment / Version). The section is absent, so nothing can be extracted -> 4.5.6 gap handling, or the user picks a version from the 4.5.3 list. The new value is set by Jira version ID from 4.5.3 (never hardcoded).
- **Augment**: same discovery and matching. The chosen version IDs are **merged** with the existing 0.9.0 entry in the `versions` array, so the existing entry is kept.

## Final state

| Field | Before | After |
|---|---|---|
| Affects Version/s | 0.9.0 | 0.9.0 (unchanged — kept) |
| Jira mutations performed | — | none |
| Gap comment posted | — | no |
