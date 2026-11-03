# Step 4.5 – Affects Version Resolution for ACME-510

## 4.5.1 – Check existing field

- `affectsVersions` on ACME-510: **(none)**, so the field is empty.
- No keep/replace/augment prompt is needed. Go straight to 4.5.2.

## 4.5.2 – Extract version from description

Source: the **Environment / Version** section parsed in Step 1:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

| Candidate | Pattern | Is it the product version? |
|---|---|---|
| `0.9.0` | Version keyword followed by a number (`Product version: 0.9.0`), explicit semver | **Yes**. This is the extracted product version |
| `9.2` | Follows `RHEL` (operating system) | No. Environment detail, not the product |
| `4.14` | Follows `OpenShift` (deployment platform) | No. Environment detail, not the product |

**Extracted version: `0.9.0`**

## 4.5.3 – Discover available Jira versions

Call that would be made (not executed in this eval):

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```
REST fallback: `python3 scripts/jira-client.py get_versions ACME`

`versions.allowedValues` (from the mock issue data):

Available Jira versions:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 – Match

Substring match of `0.9.0` against the version names:

| Jira version | Contains "0.9.0"? |
|---|---|
| RHTPA 0.9.0 (62643) | **yes** |
| RHTPA 1.0.0 (62644) | no |
| RHTPA 1.1.0 (62645) | no |

There is exactly one match, **RHTPA 0.9.0 (ID: 62643)**. No other candidates need to be shown.

## 4.5.5 – Confirm with user

Prompt shown to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

- **yes**: set the field with the version ID found in 4.5.3:
  ```
  jira.edit_issue("ACME-510", fields={
    "versions": [{"id": "62643"}]
  })
  ```
  REST fallback: `python3 scripts/jira-client.py update_issue ACME-510 --fields-json '{"versions": [{"id": "62643"}]}'`
- **no**: show the available versions table above and ask the user to pick one (62643 / 62644 / 62645) or type a version.
- **skip**: leave Affects Version unset and go on to Step 5.

This is a replace-from-empty case, so there are no existing versions to merge.

## 4.5.6 – Flag gap

**Not triggered.** A version was extracted (`0.9.0`) and it matched a Jira version, so no "Affects Version could not be determined" comment is posted.
