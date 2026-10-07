# Step 4.5 -- Affects Version Resolution

## Step 4.5.1 -- Check existing Affects Version

The `Affects Version/s` field on ACME-510 is **(none)** -- not populated.
Proceeding to version extraction.

## Step 4.5.2 -- Extract version identifier from Environment / Version

The **Environment / Version** section contains:

> Product version: 0.9.0
> OS: RHEL 9.2
> Deployment: OpenShift 4.14

Extracted version identifier: **0.9.0**

## Step 4.5.3 -- Available Jira versions

The following versions are available in the ACME Jira project:

| Jira ID | Name          | Released | Release Date |
|---------|---------------|----------|--------------|
| 62643   | RHTPA 0.9.0   | yes      | 2025-06-15   |
| 62644   | RHTPA 1.0.0   | yes      | 2025-09-01   |
| 62645   | RHTPA 1.1.0   | no       | 2026-01-15   |

## Step 4.5.4 -- Substring matching

Matching extracted version "0.9.0" against available Jira version names:

- "RHTPA 0.9.0" -- **MATCH** (substring "0.9.0" found in "RHTPA 0.9.0")
- "RHTPA 1.0.0" -- no match
- "RHTPA 1.1.0" -- no match

Matched version: **RHTPA 0.9.0** (Jira ID: 62643)

## Step 4.5.5 -- Confirmation prompt

The following prompt would be presented to the user:

> The Environment / Version section reports **Product version: 0.9.0**.
> The Affects Version/s field on ACME-510 is currently not set.
>
> I found a matching Jira version: **RHTPA 0.9.0** (ID: 62643, released 2025-06-15).
>
> Would you like me to set the Affects Version on ACME-510 to **RHTPA 0.9.0**?
