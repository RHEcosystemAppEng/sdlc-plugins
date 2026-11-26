# Step 4.5 – Affects Version Resolution (ACME-510)

## 4.5.1 – Check existing field

The Affects Version/s (`versions`) field on ACME-510 is **(none)**, so it is not populated.
The keep/replace/augment prompt is skipped and resolution continues at 4.5.2.

## 4.5.2 – Extract version from description

Source is the **Environment / Version** section:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

| Line | Pattern matched | Treated as product version? |
|---|---|---|
| `Product version: 0.9.0` | version keyword + explicit semver `0.9.0` | **Yes**, extracted |
| `OS: RHEL 9.2` | OS release number | No, operating-system environment detail |
| `Deployment: OpenShift 4.14` | platform release number | No, deployment-platform detail |

**Extracted version:** `0.9.0`

## 4.5.3 – Discover available Jira versions

Would call:

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```

The call reads `fields.versions.allowedValues`. The REST fallback would be `python3 scripts/jira-client.py get_versions ACME`.

In this eval, the versions come from the issue fixture:

```
Available Jira versions:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |
```

## 4.5.4 – Match

Substring match of `0.9.0` against each version name:

| Jira ID | Name | Contains "0.9.0"? |
|---|---|---|
| 62643 | RHTPA 0.9.0 | **Yes** |
| 62644 | RHTPA 1.0.0 | No |
| 62645 | RHTPA 1.1.0 | No |

There is exactly one match: **RHTPA 0.9.0 (ID: 62643)**, a released version (2025-06-15).
There is no ambiguity, so only one candidate is presented.

## 4.5.5 – Confirm with user

Prompt presented to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

Handling of each answer:

- **yes**: set the field using the discovered version ID (not a hardcoded name):
  ```
  jira.edit_issue("ACME-510", fields={
    "versions": [{"id": "62643"}]
  })
  ```
  This is a plain set, not an augment, because the field was empty.
- **no**: show the available-versions table above and ask the user to pick one
  (62643 / 62644 / 62645) or enter a version manually. Then set `versions` to the chosen ID.
- **skip**: leave Affects Version unset and go on to Step 5.

## 4.5.6 – Gap flagging

**Not triggered.** A version was extracted and it matched an available Jira version. No
"Affects Version could not be determined" comment is posted.
