# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Case C -- No Supported Versions Affected

**Recommendation: Close as Not a Bug (not affected).**

All supported versions ship serde_json at or above the fix threshold of 1.0.135. The vulnerability (stack overflow on deeply nested input in serde_json < 1.0.135) does not affect any shipped version of the product.

### Evidence Summary

| Stream | Versions checked | serde_json range shipped | Fix threshold | Affected? |
|--------|-----------------|--------------------------|---------------|-----------|
| 2.1.x | 2.1.0, 2.1.1 | 1.0.137 | 1.0.135 | NO |
| 2.2.x | 2.2.0 -- 2.2.4 | 1.0.138 -- 1.0.139 | 1.0.135 | NO |

The lowest serde_json version found across all streams and versions is 1.0.137, which is already 2 patch versions above the fix threshold (1.0.135).

## Proposed Jira Actions

The following actions would be performed on TC-8002 after engineer confirmation:

### 1. Add comment documenting triage result

Post a comment to TC-8002 with the version impact analysis:

> No supported versions ship a vulnerable version of serde_json. Version impact analysis shows all versions ship serde_json >= 1.0.137, which is above the affected range (< 1.0.135). All supported versions ship the fix introduced in serde_json 1.0.135 (configurable recursion limit defaulting to 128 levels of nesting).

### 2. Transition to Closed with resolution "Not a Bug"

Close TC-8002 with resolution "Not a Bug" since no supported version is affected.

### 3. Set VEX Justification

Set `customfield_12345` (VEX Justification) to **"Component not Present"** -- the vulnerable package version (serde_json < 1.0.135) is not shipped in any supported version. Although serde_json is present in the dependency tree, it is at fixed versions (>= 1.0.137) that do not contain the vulnerability.

### 4. Add the ai-cve-triaged label

Add the `ai-cve-triaged` label to TC-8002 to mark the issue as triaged and prevent re-processing in future discovery queries.

### 5. Post-triage summary comment

Post a summary comment to TC-8002 documenting:
- Version impact table (all versions NOT affected)
- Affects Versions: no correction needed (the issue's scope is 2.2.x and no 2.2.x versions are affected)
- Triage outcome: Closed as Not a Bug
- VEX Justification: Component not Present
- @mention of the issue reporter (PSIRT analyst) for visibility

## Steps Not Applicable

- **Step 3 (Affects Versions Correction)**: Not needed -- the issue will be closed, not remediated. PSIRT-claimed RHTPA 2.2.0 is not actually affected.
- **Step 4 (Duplicate/Sibling Check)**: No remediation tasks to create, so sibling coordination is informational only. No action required.
- **Step 5 (Version Lifecycle Check)**: Not needed -- no versions are affected regardless of lifecycle status.
- **Step 6 (Already Fixed Check)**: Not needed -- the vulnerability was never present in any shipped version (the fix predates all supported releases).
- **Step 7 (Concurrent Triage Detection)**: Not applicable -- no Upstream Affected Component custom field configured.
- **Step 8 (Remediation)**: No remediation tasks needed -- Case C applies (close as Not a Bug).
