# Affects Version Resolution: ACME-510

## Step 4.5: Affects Version Resolution

### Sub-step 4.5.1: Existing Field Check

The Affects Version/s field on ACME-510 is currently **(none)** -- the field is not already set. Skipping existing-field-check since there is no value to preserve.

### Sub-step 4.5.2: Version Extraction

Source section: **Environment / Version**

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

Extracted version identifier: **0.9.0**

Extraction method: Parsed the "Product version:" line from the Environment / Version section. The value "0.9.0" follows standard semantic versioning format (MAJOR.MINOR.PATCH).

### Sub-step 4.5.3: Available Jira Versions

The following versions are configured in the Jira project ACME:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

### Sub-step 4.5.4: Version Matching

Matching extracted version "0.9.0" against available Jira versions using substring matching:

- "RHTPA 0.9.0" -- **MATCH** (contains substring "0.9.0")
- "RHTPA 1.0.0" -- no match
- "RHTPA 1.1.0" -- no match

**Matched version**: RHTPA 0.9.0 (Jira ID: 62643)

Match type: Substring match -- the extracted version string "0.9.0" appears within the Jira version name "RHTPA 0.9.0".

### Sub-step 4.5.5: Confirmation Prompt

The following confirmation would be presented to the user:

> The Environment / Version section reports **Product version: 0.9.0**, which matches Jira version **RHTPA 0.9.0** (ID: 62643, released 2025-06-15).
>
> The Affects Version/s field on ACME-510 is currently empty.
>
> **Set Affects Version to "RHTPA 0.9.0" on ACME-510?** (y/n)

Upon user confirmation, the Jira API call would be:
```
PUT /rest/api/3/issue/ACME-510
{
  "fields": {
    "versions": [{ "id": "62643" }]
  }
}
```
