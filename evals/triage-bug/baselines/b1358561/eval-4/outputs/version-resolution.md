# Step 4.5 — Affects Version Resolution (ACME-510)

## 4.5.1 — Check existing field

`affectsVersions` on ACME-510: **(none)** — field is empty. No keep/replace/augment prompt is needed; continue to extraction.

## 4.5.2 — Extract version from description

Source: the **Environment / Version** section parsed in Step 1:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Pattern scan:

| Line | Candidate | Classification |
|---|---|---|
| `Product version: 0.9.0` | `0.9.0` | **Product version** (version keyword + explicit semver) — selected |
| `OS: RHEL 9.2` | `9.2` | Operating system version — environment context, not the product version; ignored |
| `Deployment: OpenShift 4.14` | `4.14` | Platform version — environment context, not the product version; ignored |

Extracted product version: **`0.9.0`**

## 4.5.3 — Discover available Jira versions

Call (not executed in eval):

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

## 4.5.4 — Match

Substring match of `0.9.0` against version names:

| Jira version | Contains `0.9.0`? |
|---|---|
| RHTPA 0.9.0 (62643) | **yes** |
| RHTPA 1.0.0 (62644) | no |
| RHTPA 1.1.0 (62645) | no |

Result: exactly one candidate — **RHTPA 0.9.0 (ID: 62643)**. No ambiguity, so no gap flagging (4.5.6 not triggered).

## 4.5.5 — Confirmation prompt presented to the user

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

- **yes** → update the field
- **no** → ask the user to pick from the Available Jira versions table above or enter a version manually
- **skip** → leave Affects Version unset and continue to Step 5

## Update operation (on "yes"; not executed in eval)

```
jira.edit_issue("ACME-510", fields={
  "versions": [{"id": "62643"}]
})
```

REST fallback: `python3 scripts/jira-client.py update_issue ACME-510 --fields-json '{"versions": [{"id": "62643"}]}'`

The version ID `62643` comes from the version discovery in 4.5.3, not a hardcoded value. This is not an augment, so no merge with existing versions is needed.

## 4.5.6 — Gap flag

Not triggered: a version was extracted and matched. No "Affects Version could not be determined" comment is posted.
