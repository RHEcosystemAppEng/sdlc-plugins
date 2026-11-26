# Step 4.5 — Affects Version Resolution (ACME-500)

## 4.5.1 — Check existing field

Step 1 recorded that the Bug's `affectsVersions` field (the Jira `versions` field) **already has one value**:

- `0.9.0`

Because the field is already set, the skill does **not** extract or set a version automatically. It shows the current value and asks the user what to do:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep — leave the current value and skip to Step 5
2. Replace — clear and set a new value
3. Augment — add additional versions alongside the current ones

Choose (1/2/3):
```

**Execution pauses here until the user answers.** The existing value is not overwritten, cleared, or skipped silently. No `jira.edit_issue` call is made on the `versions` field before the user chooses.

## What happens for each choice

### 1. Keep
- Sub-steps 4.5.2 to 4.5.6 are skipped.
- No `jira.edit_issue` call is made. `Affects Version/s` stays `[0.9.0]`.
- No gap comment is posted.
- Go to Step 5 (Generate Task).

### 2. Replace
- 4.5.2 (extract from description): the Bug description has **no `### **Environment / Version**` section** (see `bug-parsing.md`), so no version can be extracted from it. The user is asked to pick from the available Jira versions or type one in.
- 4.5.3 (discover versions): `jira.getJiraIssueTypeMetaWithFields(projectIdOrKey: "ACME", issueTypeId: "10020")` is called, or the REST fallback `python3 scripts/jira-client.py get_versions ACME`. The skill reads `versions.allowedValues` (`id`, `name`, `released`, `releaseDate`) and shows them as a table. This was not executed in the eval, so no real IDs are available.
- 4.5.4 / 4.5.5: the skill matches the user's selection to a Jira version ID and asks for confirmation (yes/no/skip). Then it calls:
  ```
  jira.edit_issue("ACME-500", fields={"versions": [{"id": "<selected-version-id>"}]})
  ```
- 4.5.6: if nothing usable is provided or matched, the skill posts the gap comment "Affects Version could not be determined from the bug description — please set manually." with the Comment Footnote (sdlc-workflow/triage-bug v0.14.0).

### 3. Augment
- Same discovery and confirmation flow as Replace.
- The update **merges** the new version(s) with the existing one:
  ```
  jira.edit_issue("ACME-500", fields={"versions": [{"id": "<id-of-0.9.0>"}, {"id": "<additional-version-id>"}]})
  ```
  The ID for `0.9.0` comes from the discovered `allowedValues`. It is not hardcoded.

## Eval outcome

- Existing value found: **yes** (`0.9.0`).
- The value was shown to the user with **Keep / Replace / Augment** options.
- Current state: **waiting for the user's choice.** No change has been made to the field. If the user chooses Keep, which is the likely choice since the reporter set it and nothing in the investigation contradicts it, `Affects Version/s` stays `0.9.0` and triage moves on to Step 5.
