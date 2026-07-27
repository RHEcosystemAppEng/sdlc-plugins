# Triage Outcome: TC-8002 (CVE-2026-28940)

## Triage Decision: Case C -- No Supported Versions Affected

**Recommendation: Close as Not a Bug (not affected).**

No supported version ships a vulnerable version of serde_json. All versions across both the 2.1.x and 2.2.x streams ship serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerability (stack overflow on deeply nested JSON input) does not apply to any shipped product version.

## Evidence Summary

| Stream | Versions Checked | serde_json Range Found | Affected? |
|--------|-----------------|----------------------|-----------|
| 2.1.x | 2.1.0, 2.1.1 | 1.0.137 | NO |
| 2.2.x | 2.2.0 -- 2.2.4 | 1.0.138 -- 1.0.139 | NO |

The lowest serde_json version found across all streams is **1.0.137**, which is **2 patch versions above** the fix threshold of 1.0.135.

## VEX Justification

Since the VEX Justification custom field is configured (`customfield_12345`), it should be set to:

**"Component not Present"** -- the vulnerable version of serde_json (< 1.0.135) is not present in any supported product version. All versions ship a patched release.

Note: While the serde_json package itself is present, the *vulnerable version range* (< 1.0.135) is not present in any shipped version. This aligns with the VEX "Component not Present" justification because the vulnerable component (serde_json < 1.0.135) is not shipped.

## Proposed Jira Actions

The following Jira mutations would be performed (each requiring engineer confirmation):

### 1. Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions (`RHTPA 2.2.0`) is incorrect -- version 2.2.0 ships serde_json 1.0.138, which is not vulnerable.

- **Current**: `[RHTPA 2.2.0]`
- **Proposed**: `[]` (empty -- no versions are affected)

Since this is a Case C closure, the Affects Versions correction is informational but moot -- the issue will be closed as not affected.

### 2. Add Triage Comment

Post a comment to TC-8002 documenting the version impact analysis:

```
No supported versions ship a vulnerable version of serde_json.
Version impact analysis:

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0   | 1.0.137    | NO        | ships patched version |
| 2.1.1   | 1.0.137    | NO        | ships patched version |
| 2.2.0   | 1.0.138    | NO        | ships patched version |
| 2.2.1   | 1.0.138    | NO        | ships patched version |
| 2.2.2   | --         | NO        | retag of 2.2.1 |
| 2.2.3   | 1.0.139    | NO        | ships patched version |
| 2.2.4   | 1.0.139    | NO        | ships patched version |

All supported versions ship serde_json >= 1.0.137, which is outside the
affected range (< 1.0.135). Closing as Not a Bug.

@reporter (PSIRT analyst)

[sdlc-workflow:triage-security]
```

### 3. Set VEX Justification

```
jira.edit_issue("TC-8002", fields={
  "customfield_12345": "Component not Present"
})
```

### 4. Transition to Closed

```
jira.transition_issue("TC-8002", resolution="Not a Bug")
```

### 5. Add `ai-cve-triaged` Label

```
jira.edit_issue("TC-8002", fields={
  "labels": ["CVE-2026-28940", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

## Steps Not Applicable

- **Step 4 (Duplicate/Sibling Check)**: Would search for sibling issues with same CVE label -- informational only since outcome is Case C closure.
- **Step 5 (Version Lifecycle Check)**: Not needed since no versions are affected.
- **Step 6 (Already Fixed Check)**: Not applicable -- the vulnerability was never present in any shipped version (different from "was present and was fixed").
- **Step 7 (Concurrent Triage Detection)**: Not applicable since no remediation tasks are being created (Upstream Affected Component field is also not configured).
- **Step 8 Case A/B (Remediation Tasks)**: Not applicable -- no remediation needed since no versions are affected.

## Summary

TC-8002 (CVE-2026-28940, serde_json stack overflow) is **not affected** in any supported product version. All shipped versions include serde_json >= 1.0.137, well above the 1.0.135 fix threshold. The recommended action is to close the issue as "Not a Bug" with VEX justification "Component not Present" and add the `ai-cve-triaged` label.
