# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Case C -- No Supported Versions Affected

**Recommendation: Close as "Not a Bug" (not affected)**

All supported product versions across both streams (2.1.x and 2.2.x) ship serde_json >= 1.0.137, which is above the CVE fix threshold of 1.0.135. No version ships a vulnerable copy of serde_json. The vulnerability was already remediated in the dependency before any tracked release was built.

## Evidence

| Stream | Versions Checked | Minimum serde_json | Fix Threshold | Affected? |
|--------|------------------|--------------------|---------------|-----------|
| 2.1.x | 2.1.0, 2.1.1 | 1.0.137 | 1.0.135 | NO |
| 2.2.x | 2.2.0 -- 2.2.4 | 1.0.138 | 1.0.135 | NO |

Even the earliest release in the oldest stream (2.1.0, build tag v0.3.8) ships serde_json 1.0.137, two patch versions above the fix.

## Proposed Jira Actions

The following actions would be performed on TC-8002 (each requiring engineer confirmation before execution):

### 1. Add triage comment

Post a summary comment documenting the version impact analysis:

> No supported versions ship a vulnerable version of serde_json. Version impact analysis shows all versions ship serde_json >= 1.0.137, which is outside the affected range (versions before 1.0.135).
>
> Version Impact for CVE-2026-28940 (serde_json < 1.0.135):
>
> | Version | serde_json | Affected? |
> |---------|-----------|-----------|
> | 2.1.0 | 1.0.137 | NO |
> | 2.1.1 | 1.0.137 | NO |
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | -- | NO (retag of 2.2.1) |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json at or above the fixed version (1.0.135).

The comment would include an @mention of the issue reporter (PSIRT analyst) and the standard comment footnote.

### 2. Set VEX Justification

Set `customfield_12345` (VEX Justification) to **"Vulnerable Code not Present"**.

Rationale: The serde_json package IS present in all versions (it appears in Cargo.lock), but all shipped versions contain the fix (>= 1.0.135). The vulnerable code (unbounded recursion during deserialization) was removed in version 1.0.135 via the configurable recursion limit. Since the shipped versions include this fix, the vulnerable code path does not exist in the shipped binaries.

### 3. Transition to Closed

Transition TC-8002 to **Closed** with resolution **"Not a Bug"**.

### 4. Add label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged.

### 5. Affects Versions correction

The current Affects Versions field contains "RHTPA 2.2.0". Since no versions are actually affected, the Affects Versions correction would note that the PSIRT-assigned version is inaccurate -- RHTPA 2.2.0 is not actually vulnerable to this CVE. The correction would be presented to the engineer before any changes.

Note: Since the outcome is closure as "Not a Bug", the Affects Versions field may be left as-is or cleared depending on team policy, since the issue is being closed anyway.

## Steps Not Applicable

The following steps are skipped or not applicable due to the Case C outcome:

- **Step 4 (Duplicate/Sibling Check)**: Would be performed in a live triage but no Jira access available in this eval
- **Step 5 (Version Lifecycle Check)**: Not applicable since no versions are affected
- **Step 6 (Already Fixed Check)**: Not applicable since no versions are affected
- **Step 7 (Concurrent Triage Detection)**: Not applicable since no remediation tasks will be created
- **Step 8 Case A (Cross-stream impact)**: Not applicable -- no streams are affected
- **Step 8 Case B (Remediation tasks)**: Not applicable -- no remediation needed
- **Embargo Check (Step 1.7)**: Skipped -- no Embargo policy URL is configured in Security Configuration, and CVSS 5.3 (Medium) is below the threshold (>= 7.0)

## No Remediation Tasks Needed

Since all supported versions already ship the patched version of serde_json, no remediation tasks are required. This is a clean Case C closure.
