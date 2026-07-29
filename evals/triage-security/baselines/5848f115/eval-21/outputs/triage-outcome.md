# Triage Outcome -- TC-8020

## Issue Summary

- **Issue**: TC-8020
- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Fix threshold**: >= 0.11.14
- **CVSS**: 7.5 (High)
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Steps Completed

### Step 0 -- Configuration Validation
All required configuration sections are present in CLAUDE.md: Repository Registry, Jira Configuration, Code Intelligence, and Security Configuration (with Product Lifecycle, Version Streams, and Source Repositories). Configuration is valid.

Extracted values:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Upstream Affected Component custom field: customfield_10632 (configured -- Steps 4.3 and 7 are active)

### Step 0.3 -- Matrix Staleness Check
The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`, which is 31 days ago (as of 2026-07-29). This exceeds the 14-day staleness threshold. A staleness warning would be presented to the engineer with options to refresh, proceed anyway, or stop.

### Step 0.7 -- Assign and Transition
The issue would be assigned to the current user and transitioned from "New" to "Assigned" status.

### Step 1 -- Data Extraction
All critical fields were successfully parsed. See `outputs/data-extraction.md` for the full extraction table. The issue is scoped to stream 2.2.x. Ecosystem is Cargo (source dependency).

### Step 1.5 -- External CVE Data Enrichment
External CVE APIs (MITRE CVE API and OSV.dev) would be queried for structured version range data to cross-validate the Jira description. The fix threshold from external sources would be compared against the Jira-parsed value of 0.11.14.

### Step 1.7 -- Embargo Check
CVSS is 7.5 (>= 7.0 threshold). However, no Embargo policy URL is configured in Security Configuration, so this step is skipped.

### Step 2 -- Version Impact Analysis
Version impact analysis based on lock file data at pinned commits:

**Stream 2.2.x (in scope):**

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO |
| RHTPA 2.2.4 | 0.11.14 | NO |

**Stream 2.1.x (out of scope, cross-stream awareness):**

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |

### Step 3 -- Affects Versions Correction
PSIRT-assigned Affects Versions: `[RHTPA 2.0.0]`
This is **incorrect** -- RHTPA 2.0.0 does not correspond to any configured stream.

Proposed correction (scoped to 2.2.x stream): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fix version) and are not affected.

### Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check
A JQL search for sibling Vulnerability issues with label CVE-2026-31812 would be performed. Any same-stream duplicates would be flagged, and cross-stream companions would be linked with "Related" type.

Step 4.3 (Cross-CVE overlap) is active because the Upstream Affected Component field is configured.

### Step 5 -- Version Lifecycle Check
The product lifecycle page at the configured URL would be checked to verify all affected versions are still supported.

### Step 6 -- Already Fixed Check
Resolved sibling issues would be cross-referenced. The fix was introduced in version 2.2.3 (build v0.4.11), but versions 2.2.0, 2.2.1, and 2.2.2 remain affected.

### Step 7 -- Concurrent Triage Detection
See `outputs/concurrent-triage.md` for full analysis.

**Result**: Concurrent triage detected. TC-8019 is actively being triaged by engineer-b@example.com and also targets the `quinn-proto` upstream component. The engineer must choose one of three options before proceeding:

1. **Wait** -- pause until TC-8019's triage completes
2. **Skip** -- skip remediation task creation
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

## Triage Decision

### Classification: Case B (Affected) with Case A (Cross-Stream Impact) -- BLOCKED by Step 7

The triage analysis shows:
- **Within 2.2.x scope**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are not affected (they ship the fix).
- **Cross-stream**: Stream 2.1.x is also fully affected (all versions ship quinn-proto 0.11.9), triggering Case A cross-stream impact notification.

### What would happen after Step 7 resolution

If the engineer chooses **Proceed** (or **Wait** and later re-runs):

1. **Case A -- Cross-stream impact comment**: A comment would be posted on TC-8020 noting that stream 2.1.x is also affected. If no sibling CVE Jira exists for stream 2.1.x, preemptive remediation tasks would be created for that stream with the `security-preemptive` label and "Related" link type.

2. **Case B -- Remediation task creation for 2.2.x**: Since Cargo is a source dependency ecosystem, **2 tasks** would be created:
   - **Upstream backport task**: Bump quinn-proto to >= 0.11.14 on the `release/0.4.z` branch of `rhtpa-backend`
   - **Downstream propagation task**: Update `artifacts.lock.yaml` in `rhtpa-release.0.4.z` to reference a backend build that includes the fix. This task would be blocked by the upstream backport task (link type "Blocks").
   
   Both tasks would be linked to TC-8020 with "Depend" link type.

3. **Post-triage actions**:
   - Add `ai-cve-triaged` label to TC-8020
   - Post summary comment with version impact table, Affects Versions correction, remediation task links, and @mention of the issue reporter
   - If Proceed was chosen, also add `concurrent-triage-overlap` label

### Current Status

**Triage is paused at Step 7.** The concurrent triage on TC-8019 (same upstream component `quinn-proto`, status In Progress, assignee engineer-b@example.com) requires engineer input before remediation tasks can be created. The three options (Wait, Skip, Proceed) have been presented. No Jira mutations for task creation should occur until the engineer responds.
