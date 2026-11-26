# Step 4.5 – Affects Version Resolution: ACME-510

## 4.5.1 – Check existing field

`Affects Version/s` on ACME-510 is **(none)**. The `affectsVersions` field is empty, so the keep/replace/augment prompt is not shown. Continue to 4.5.2.

## 4.5.2 – Extract version from description

Environment / Version section content:
```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

| Candidate | Pattern | Is product version? |
|---|---|---|
| `0.9.0` | Version keyword ("Product version:") followed by an explicit semver | **yes** |
| `9.2` | Follows "RHEL" (OS version) | no. This is the operating system version, not the product version |
| `4.14` | Follows "OpenShift" (platform version) | no. This is the deployment platform version, not the product version |

**Extracted version: `0.9.0`**

## 4.5.3 – Discover available Jira versions

Call (not executed in this eval):
```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```
→ `versions.allowedValues`
(REST fallback: `python3 scripts/jira-client.py get_versions ACME`)

Available Jira versions (from the mock issue data):

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

Exactly one candidate: **RHTPA 0.9.0 (ID: 62643)**. The OS and platform versions (`9.2`, `4.14`) were excluded and match nothing anyway.

## 4.5.5 – Confirmation prompt shown to the user

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

- **yes**: set the field with the discovered ID:
  ```
  jira.edit_issue("ACME-510", fields={
    "versions": [{"id": "62643"}]
  })
  ```
  (REST fallback: `python3 scripts/jira-client.py update_issue ACME-510 --fields-json '{"versions": [{"id": "62643"}]}'`)
- **no**: show the available-versions table above and ask the user to pick one (62643 / 62644 / 62645) or type a version.
- **skip**: leave Affects Version unset and continue to Step 5.

No write happens until the user confirms. In this eval, no Jira call was made.

## 4.5.6 – Gap flagging

**Not triggered.** A version was extracted and it matched an available Jira version, so no "Affects Version could not be determined" comment is needed.
