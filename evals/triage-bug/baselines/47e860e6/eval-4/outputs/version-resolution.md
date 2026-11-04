# Step 4.5 — Affects Version Resolution: ACME-510

## 4.5.1 — Check existing field

- `affectsVersions` (`versions` field) on ACME-510: **(none). Not populated.**
- No keep/replace/augment prompt is needed. Continue to 4.5.2.

## 4.5.2 — Extract version from description

Environment / Version section content:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Version pattern analysis:

| Line | Candidate | Product version? | Decision |
|---|---|---|---|
| `Product version: 0.9.0` | `0.9.0` | Yes. Version keyword followed by an explicit semver. | **Extracted** |
| `OS: RHEL 9.2` | `9.2` | No. This is the operating system version. | Ignored |
| `Deployment: OpenShift 4.14` | `4.14` | No. This is the platform version. | Ignored |

**Extracted version: `0.9.0`**

## 4.5.3 — Discover available Jira versions

The skill would call:

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```

It would then read `fields.versions.allowedValues`. The REST fallback is `python3 scripts/jira-client.py get_versions ACME`. The values below come from the mock issue file. No live call was made.

Available Jira versions:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 — Match

Substring match of `0.9.0` against the version names:

| Jira version | Contains `0.9.0`? |
|---|---|
| RHTPA 0.9.0 (62643) | **Yes** |
| RHTPA 1.0.0 (62644) | No |
| RHTPA 1.1.0 (62645) | No |

Result: **one match**, `RHTPA 0.9.0` (ID 62643). There is no ambiguity, so the user does not need to pick between candidates.

The OS and platform numbers (`9.2`, `4.14`) were excluded from matching. Neither would have matched any listed version anyway.

## 4.5.5 — Confirmation prompt presented to the user

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

The user has not answered yet. This is the action for each reply:

- **yes**: update the field using the discovered version ID:
  ```
  jira.edit_issue("ACME-510", fields={
    "versions": [{"id": "62643"}]
  })
  ```
  REST fallback: `python3 scripts/jira-client.py update_issue ACME-510 --fields-json '{"versions": [{"id": "62643"}]}'`
- **no**: show the available versions table above and ask the user to pick one (62643 / 62644 / 62645) or type a version name.
- **skip**: leave Affects Version unset and continue to Step 5.

## 4.5.6 — Flag gap

**Not applicable.** A version was extracted (`0.9.0`) and it matched a Jira version (`RHTPA 0.9.0`). The skill does not post the "Affects Version could not be determined" comment.
