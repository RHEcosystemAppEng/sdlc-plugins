# Step 4.5 – Affects Version Resolution: ACME-500

## 4.5.1 – Check existing field

Step 1 recorded that the Bug's `affectsVersions` (`versions`) field is **already populated**
with one value: **`0.9.0`**.

Because the field is already set, the skill does **not** silently overwrite it and does **not**
silently skip it. It displays the current value and asks the user:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep — leave the current value and skip to Step 5
2. Replace — clear and set a new value
3. Augment — add additional versions alongside the current ones

Choose (1/2/3):
```

**Status: awaiting user input.** No `jira.edit_issue` call is made on the `versions` field until
the user picks an option.

## What happens after each choice

| Choice | Behaviour |
|---|---|
| 1. Keep | Leave `versions = [0.9.0]` untouched. Skip 4.5.2–4.5.6 entirely. Proceed to Step 5. No Jira mutation, no gap comment. |
| 2. Replace | Continue to 4.5.2. The new value replaces (does not merge with) `0.9.0`, after user confirmation in 4.5.5. |
| 3. Augment | Continue to 4.5.2. The confirmed version(s) are merged with the existing `0.9.0`, e.g. `versions: [{"id": "<id-of-0.9.0>"}, {"id": "<new-id>"}]`. |

### Replace / Augment path detail

- **4.5.2 – Extract from description:** The description has no `### **Environment / Version**`
  section (see bug-parsing.md), so no version identifier can be extracted from the description
  body. Per the skill this leads to 4.5.6 (gap flag) — but since the field is already populated,
  the more useful action is to let the user pick from the available versions list in 4.5.3/4.5.5
  ("no" -> select from list or enter manually).
- **4.5.3 – Discover versions:** would call
  `jira.getJiraIssueTypeMetaWithFields(projectIdOrKey: "ACME", issueTypeId: "10020")`
  (REST fallback: `python3 scripts/jira-client.py get_versions ACME`) and read the `versions`
  field's `allowedValues` (id, name, released, releaseDate). Not executed in this eval (no
  external calls); no version list is available in the fixtures, so none is fabricated here.
- **4.5.4 / 4.5.5 – Match & confirm:** substring-match any user-provided version text against
  `allowedValues[].name`, present candidates, ask `Set this as the Affects Version on ACME-500?
  (yes/no/skip)`, then `jira.edit_issue("ACME-500", fields={"versions": [...]})` using IDs from
  4.5.3 (never hardcoded).
- **4.5.6 – Gap flag:** only if the user chose Replace/Augment and no version could be determined.
  The existing `0.9.0` value means there is no "unknown version" gap on the issue as it stands.

## Recommended default

**1. Keep.** The existing value `0.9.0` is consistent with the bug report (component sdlc-workflow,
reported against 0.9.0) and nothing in the description contradicts it. Final decision is the
user's.
