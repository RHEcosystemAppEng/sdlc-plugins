# Step 4.5 — Affects Version Resolution (ACME-510)

## 4.5.1 — Check existing field

`Affects Version/s` on ACME-510: **(none)**. The field is empty, so the keep/replace/augment
prompt is skipped and resolution continues with extraction.

## 4.5.2 — Extract version from description

Source: the **Environment / Version** section, parsed in Step 1:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

| Candidate text | Pattern | Used? | Reason |
|---|---|---|---|
| `0.9.0` | Explicit version number with a "Product version:" keyword | **Yes** | Labelled as the product version |
| `9.2` | Version number on the OS line | No | OS (RHEL) version, not the product version |
| `4.14` | Version number on the Deployment line | No | Platform (OpenShift) version, not the product version |

**Extracted version: `0.9.0`**

## 4.5.3 — Discover available Jira versions

Call (not executed in this eval):
```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```
REST fallback: `python3 scripts/jira-client.py get_versions ACME`

The `versions` field's `allowedValues`, taken from the mock issue data:

Available Jira versions:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 — Match

Substring match of `0.9.0` against each version name:

| Jira version | Contains `0.9.0`? |
|---|---|
| RHTPA 0.9.0 (62643) | **Yes** |
| RHTPA 1.0.0 (62644) | No |
| RHTPA 1.1.0 (62645) | No |

Result: **exactly one match**, `RHTPA 0.9.0` (ID `62643`, released 2025-06-15). There are no
other candidates, so no disambiguation is needed.

## 4.5.5 — Confirm with user

Prompt shown to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

- **yes**: set the field, using the version ID discovered in 4.5.3 (not a hardcoded value):
  ```
  jira.edit_issue("ACME-510", fields={
    "versions": [{"id": "62643"}]
  })
  ```
  REST fallback: `python3 scripts/jira-client.py update_issue ACME-510 --fields-json '{"versions": [{"id": "62643"}]}'`
  The field was empty, so this is a plain set with nothing to merge.
- **no**: show the available-versions table above and ask the user to pick one or type a
  version manually.
- **skip**: leave Affects Version unset and go to Step 5.

## 4.5.6 — Flag gap

**Not triggered.** A version was extracted and matched, so no "Affects Version could not be
determined" comment is posted to ACME-510.
