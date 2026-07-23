# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Case C -- Close as Not a Bug (Not Affected)

The version impact analysis shows that **no supported version** ships a vulnerable
version of serde_json. All versions across both streams (2.1.x and 2.2.x) ship
serde_json >= 1.0.137, which is above the fix threshold of 1.0.135.

The vulnerability (stack overflow on deeply nested input, affecting serde_json
versions before 1.0.135) does not apply to any shipped product version.

## Steps 3-7 Summary

### Step 3 -- Affects Versions Correction

The PSIRT-assigned Affects Version is **RHTPA 2.2.0**. Since the version impact
table shows RHTPA 2.2.0 is NOT affected (ships serde_json 1.0.138 >= 1.0.135),
the Affects Versions field should be **cleared** (no versions are affected).

However, since the outcome is to close the issue entirely as Not a Bug, the
Affects Versions correction is moot -- the issue will be closed regardless.

### Step 4 -- Duplicate/Sibling Check

No sibling search performed in this eval (no Jira access). In a live triage,
the skill would search for other Vulnerability issues with the CVE-2026-28940 label.

### Step 5 -- Version Lifecycle Check

Not applicable -- no versions are affected, so lifecycle status does not change the outcome.

### Step 6 -- Already Fixed Check

Not applicable -- the vulnerability was never present in any supported version.
This is distinct from "already fixed" (which implies it was once present and then
patched). The correct classification is "not affected" (Component not Present at
vulnerable version).

### Step 7 -- Concurrent Triage Detection

Upstream Affected Component custom field is not configured in the Security
Configuration. Step 7 is skipped.

## Proposed Jira Actions

The following Jira mutations would be performed after engineer confirmation:

### 1. Add triage comment to TC-8002

```
No supported versions ship a vulnerable version of serde_json.

Version impact analysis (CVE-2026-28940, serde_json < 1.0.135):

| Version | serde_json | Affected? |
|---------|------------|-----------|
| 2.1.0   | 1.0.137    | NO        |
| 2.1.1   | 1.0.137    | NO        |
| 2.2.0   | 1.0.138    | NO        |
| 2.2.1   | 1.0.138    | NO        |
| 2.2.2   | 1.0.138    | NO (retag of 2.2.1) |
| 2.2.3   | 1.0.139    | NO        |
| 2.2.4   | 1.0.139    | NO        |

All supported versions ship serde_json >= 1.0.137, which is outside the
affected range (< 1.0.135). Closing as Not a Bug.
```

### 2. Set VEX Justification

Field: `customfield_12345`
Value: **Component not Present**

Rationale: The vulnerable version of serde_json (< 1.0.135) was never shipped in
any supported product version. All versions ship 1.0.137 or later, which includes
the fix. The "Component not Present" justification applies because the vulnerable
component (serde_json < 1.0.135) is not present in any shipped artifact.

### 3. Transition TC-8002 to Closed

- Resolution: **Not a Bug**
- The issue is not affected -- no remediation is required.

### 4. Add ai-cve-triaged label

Add `ai-cve-triaged` label to TC-8002 to mark it as triaged and prevent
re-processing in future discovery mode queries.

### 5. Post-triage summary comment

Post a final summary comment to TC-8002 including:
- Version impact table (as above)
- Triage outcome: Closed as Not a Bug (not affected)
- VEX Justification: Component not Present
- @mention of the issue reporter (account ID from Jira issue data)
- Comment Footnote per shared/comment-footnote.md (skill: triage-security)

## No Remediation Tasks Created

Since no supported versions are affected, no remediation tasks are needed.
No upstream backport tasks or downstream propagation tasks are required.
