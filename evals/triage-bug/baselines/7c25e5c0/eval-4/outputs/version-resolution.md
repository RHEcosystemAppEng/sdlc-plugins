# Affects Version Resolution: ACME-510

## Step 4.5.1 -- Check Existing Field

The `Affects Version/s` field on ACME-510 is currently set to **(none)**.
The field is not already populated, so version resolution proceeds.

## Step 4.5.2 -- Extract Version from Description

Parsed the **Environment / Version** section of the bug description:

```
Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14
```

**Extracted version identifier**: `0.9.0`

Source: The "Product version" line in the Environment / Version section.

## Step 4.5.3 -- Discover Available Jira Versions

Available versions retrieved from the ACME project:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## Step 4.5.4 -- Match

Matching extracted version `0.9.0` against available Jira versions using
substring matching:

- `0.9.0` vs `RHTPA 0.9.0` -- **MATCH** (substring "0.9.0" found in "RHTPA 0.9.0")
- `0.9.0` vs `RHTPA 1.0.0` -- no match
- `0.9.0` vs `RHTPA 1.1.0` -- no match

**Result**: Single match found -- **RHTPA 0.9.0** (Jira ID: 62643)

## Step 4.5.5 -- Confirm with User

```
Extracted version info: "0.9.0"
Matched Jira version: RHTPA 0.9.0 (ID: 62643)

Set this as the Affects Version on ACME-510? (yes/no/skip)
```

Upon user confirmation, the following Jira update would be issued:

- **Action**: Set Affects Version/s on ACME-510 to RHTPA 0.9.0 (ID: 62643)
- **MCP call** (simulated): `mcp__jira__editIssue(issueIdOrKey="ACME-510", fields={"versions": [{"id": "62643"}]})`
