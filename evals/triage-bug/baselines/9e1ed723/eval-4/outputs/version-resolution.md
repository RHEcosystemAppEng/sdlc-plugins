# Step 4.5 – Affects Version Resolution: ACME-510

## 4.5.1 – Check existing field

`affectsVersions` on ACME-510 is **empty**, as recorded in Step 1 ("Affects Version/s: (none)").
There is nothing to keep, replace, or augment, so the Keep/Replace/Augment prompt is skipped.

## 4.5.2 – Extract version from description

Source is the **Environment / Version** section:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

| Candidate | Pattern | Product version? |
|---|---|---|
| `0.9.0` | Explicit version number after the "Product version:" keyword | **Yes**. This is the extracted version |
| `9.2` | Follows "RHEL" (OS) | No. This is the OS version |
| `4.14` | Follows "OpenShift" (platform) | No. This is the deployment platform version |

**Extracted version: `0.9.0`**

## 4.5.3 – Discover available Jira versions

The skill would call:

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```

It would then read `versions.allowedValues`. REST fallback: `python3 scripts/jira-client.py get_versions ACME`.
In eval mode the versions come from the mock issue file:

```
Available Jira versions:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |
```

## 4.5.4 – Match

Substring match of `0.9.0` against the version names:

| Jira version | Contains `0.9.0`? |
|---|---|
| RHTPA 0.9.0 (62643) | **Yes** |
| RHTPA 1.0.0 (62644) | No |
| RHTPA 1.1.0 (62645) | No |

There is exactly one match: **RHTPA 0.9.0 (ID: 62643)**. It is released (2025-06-15).

## 4.5.5 – Confirm with user

Prompt shown to the user:

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

- **yes**: set the field.
- **no**: ask the user to pick from the available versions table above, or to enter a version by hand.
- **skip**: leave Affects Version unset and go to Step 5.

If the user confirms, the skill would make this call (not executed in eval mode). The ID comes from discovery, not a hardcoded value:

```
jira.edit_issue("ACME-510", fields={
  "versions": [{"id": "62643"}]
})
```

REST fallback: `python3 scripts/jira-client.py update_issue ACME-510 --fields-json '{"versions": [{"id": "62643"}]}'`

## 4.5.6 – Flag gap

**Not triggered.** A version was extracted and it matched a Jira version, so no gap comment is posted.
