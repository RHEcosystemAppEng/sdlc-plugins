# Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision: Close as Not a Bug

**Case C applies**: No supported versions in the 2.2.x stream (or any other stream) ship a vulnerable version of serde_json. All versions ship serde_json >= 1.0.135, which is at or above the fixed version. The vulnerability (affecting versions before 1.0.135) does not apply.

## Evidence Summary

- CVE-2026-28940 affects serde_json versions **before 1.0.135**
- The earliest serde_json version found across all supported product versions is **1.0.137** (in the 2.1.x stream)
- The 2.2.x stream (in scope for this issue) ships serde_json **1.0.138** or **1.0.139** across all versions (2.2.0 through 2.2.4)
- Every supported version ships a patched version of serde_json

## Proposed Jira Actions

The following Jira mutations would be proposed to the engineer for confirmation:

### 1. Affects Versions Correction (Step 3)

The current Affects Versions field lists "RHTPA 2.2.0". Since no versions in the 2.2.x stream are actually affected by this CVE, the Affects Versions should remain as-is for PSIRT tracking purposes (the version indicates what was scanned, not what is vulnerable). The close resolution makes clear the product is not affected.

### 2. Add Triage Comment

Post a comment to TC-8002:

> No supported versions ship a vulnerable version of serde_json.
>
> Version impact analysis (2.2.x stream):
>
> | Version | serde_json | Affected? |
> |---------|-----------|-----------|
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | 1.0.138 | NO (retag of 2.2.1) |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json >= 1.0.138, which is above the fixed version (1.0.135). The vulnerability (stack overflow on deeply nested input, affecting versions before 1.0.135) does not apply to any shipped version.
>
> Closing as Not a Bug (not affected).

### 3. Set VEX Justification

Set `customfield_12345` (VEX Justification) to **"Component not Present"**.

Rationale: The vulnerable version of serde_json (< 1.0.135) is not present in any supported product version. All shipped versions include the patched version. Per the skill methodology, "Component not Present" is the default when lock file analysis shows the vulnerable package version is not included.

### 4. Transition to Closed

Transition TC-8002 to **Closed** with resolution **"Not a Bug"**.

### 5. Assign to Current User

Assign TC-8002 to the current user (triage engineer).

### 6. Add ai-cve-triaged Label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged and prevent re-triage.

## Steps Not Applicable

- **Step 4 (Duplicate/Sibling Check)**: Would search for sibling issues with the CVE-2026-28940 label. No siblings referenced in the issue data. In a live triage, JQL would be run to confirm.
- **Step 5 (Version Lifecycle Check)**: Not needed since no versions are affected. Even if versions were EOL, the outcome would remain "close as Not a Bug."
- **Step 6 (Already Fixed Check)**: Not applicable -- the issue is being closed because no versions are affected, not because a sibling already fixed it.
- **Step 7 Remediation Tasks**: No remediation tasks are needed. No versions are affected, so Case C (close as Not a Bug) applies. No upstream backport or downstream propagation tasks are created.

## Summary

TC-8002 reports CVE-2026-28940 (serde_json stack overflow on deeply nested input) against the RHTPA 2.2.x stream. Lock file analysis at every pinned source commit in the 2.2.x supportability matrix shows that all versions ship serde_json 1.0.138 or 1.0.139, both well above the fix threshold of 1.0.135. The 2.1.x stream is likewise unaffected (ships 1.0.137). The recommendation is to close TC-8002 as "Not a Bug" with VEX Justification "Component not Present", add the ai-cve-triaged label, and post a summary comment with the version impact evidence.
