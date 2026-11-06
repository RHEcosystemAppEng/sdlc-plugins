# Step 4.5 — Affects Version Resolution (ACME-510)

## 4.5.1 — Check existing field

`Affects Version/s` on ACME-510 is **(none)**, so `affectsVersions` is empty.
The keep/replace/augment prompt is **skipped**. Continue to extraction.

## 4.5.2 — Extract version from description

Environment / Version section content:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Pattern scan:

| Line | Candidate | Classification |
|---|---|---|
| `Product version: 0.9.0` | `0.9.0` | **Product version.** Version keyword ("Product version") followed by an explicit semver. This is the extracted version |
| `OS: RHEL 9.2` | `9.2` | Operating system version. Not a product version, ignored |
| `Deployment: OpenShift 4.14` | `4.14` | Platform version. Not a product version, ignored |

**Extracted version: `0.9.0`**

## 4.5.3 — Discover available Jira versions

The equivalent call (simulated, not executed) would be:

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "ACME",
  issueTypeId: "10020"
)
```
→ `fields.versions.allowedValues`

(REST fallback: `python3 scripts/jira-client.py get_versions ACME`)

Available Jira versions (from the mock issue data):

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## 4.5.4 — Match

Substring match of `0.9.0` against version names:

| Jira ID | Name | Contains "0.9.0"? |
|---|---|---|
| 62643 | RHTPA 0.9.0 | **Yes** |
| 62644 | RHTPA 1.0.0 | No |
| 62645 | RHTPA 1.1.0 | No |

Exactly **one match**: `RHTPA 0.9.0` (ID `62643`), released 2025-06-15. It is unambiguous, so there is no list of candidates to choose from.

## 4.5.5 — Confirmation prompt shown to the user

```
Extracted version info: "0.9.0" (from "Product version: 0.9.0" in Environment / Version)
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

Handling of each answer:
- **yes**: update the field using the discovered ID (not a hardcoded value):
  ```
  jira.edit_issue("ACME-510", fields={
    "versions": [{"id": "62643"}]
  })
  ```
  (REST fallback: `python3 scripts/jira-client.py update_issue ACME-510 --fields-json '{"versions": [{"id": "62643"}]}'`)
  Nothing to merge: the field was empty, so this is not an augment.
- **no**: show the available-versions table above. Ask the user to pick one (62643 / 62644 / 62645) or type a version manually.
- **skip**: leave Affects Version unset and go to Step 5.

## 4.5.6 — Gap flagging

**Not triggered.** A version was extracted and it matched a Jira version, so no "Affects Version could not be determined" comment is posted.
