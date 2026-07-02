# Triage Outcome -- TC-8002

## Triage Decision: Case C -- No Supported Versions Affected

CVE-2026-28940 affects serde_json versions before 1.0.135. Lock file analysis across all supported product versions shows that every version ships serde_json >= 1.0.137, which is above the fix threshold. The vulnerable version of serde_json was never included in any supported release.

**Recommendation: Close TC-8002 as "Not a Bug" (not affected).**

## Steps 3-6 Summary

### Step 3 -- Affects Versions Correction

The issue's scoped stream is 2.2.x. Within stream 2.2.x, no versions are affected (all ship serde_json >= 1.0.138). The PSIRT-assigned Affects Version "RHTPA 2.2.0" is incorrect -- version 2.2.0 ships serde_json 1.0.138 and is NOT vulnerable.

PROPOSAL: Remove RHTPA 2.2.0 from Affects Versions (no versions should be listed as affected).

Since the outcome is Case C (close as Not a Bug), the Affects Versions correction is superseded by the closure action.

### Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

PROPOSAL: Search JQL: `project = TC AND labels = 'CVE-2026-28940' AND issuetype = 10024 AND key != TC-8002`

No sibling issues are known from the provided data. No duplicates or companions detected.

Step 4.3 (Cross-CVE overlap detection): Skipped -- Upstream Affected Component custom field is not configured in Security Configuration.

Step 4.4 (Preemptive task reconciliation): PROPOSAL: Search JQL: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-28940' ORDER BY created DESC`

No preemptive tasks known from provided data.

### Step 5 -- Version Lifecycle Check

PROPOSAL: Fetch product lifecycle page at https://access.example.com/product-life-cycle/rhtpa to verify support status of streams 2.1.x and 2.2.x.

Since no versions are affected, lifecycle status does not change the outcome (Case C closure proceeds regardless).

### Step 6 -- Already Fixed Check

No resolved sibling issues found. However, this step is moot because no versions are affected -- there is nothing to check for prior fixes.

### Step 7 -- Concurrent Triage Detection

Skipped -- Upstream Affected Component custom field is not configured in Security Configuration.

## Proposed Jira Actions

All actions below are PROPOSALS requiring engineer confirmation before execution.

### 1. Add triage comment to TC-8002

PROPOSAL: Post a comment to TC-8002 with the version impact analysis and closure rationale.

```
No supported versions ship a vulnerable version of serde_json.
Version impact analysis:

| Version | serde_json | Affected? |
|---------|------------|-----------|
| 2.1.0   | 1.0.137    | NO        |
| 2.1.1   | 1.0.137    | NO        |
| 2.2.0   | 1.0.138    | NO        |
| 2.2.1   | 1.0.138    | NO        |
| 2.2.2   | 1.0.138    | NO (retag of 2.2.1) |
| 2.2.3   | 1.0.139    | NO        |
| 2.2.4   | 1.0.139    | NO        |

All supported versions ship serde_json >= 1.0.137 which is outside the
affected range (< 1.0.135). The fix (recursion limit, introduced in 1.0.135)
is already present in all shipped versions.

@<reporter> (PSIRT reporter mention via ADF mention node)

---
[triage-security | sdlc-workflow]
```

### 2. Close TC-8002 as "Not a Bug"

PROPOSAL: Transition TC-8002 to Closed with resolution "Not a Bug".

```
jira.transition_issue("TC-8002", <closed-transition-id>)
# Resolution: "Not a Bug"
```

### 3. Set VEX Justification

PROPOSAL: Set the VEX Justification field (customfield_12345) to "Vulnerable Code not Present".

Rationale: serde_json IS shipped in all product versions, but at versions (1.0.137+) that include the fix for CVE-2026-28940. The vulnerable code path (unbounded recursion during deserialization) was removed in 1.0.135, and all shipped versions are at or above this threshold. The vulnerable code is not present in any shipped version.

```
jira.edit_issue("TC-8002", fields={
  "customfield_12345": {"value": "Vulnerable Code not Present"}
})
```

### 4. Add ai-cve-triaged label

PROPOSAL: Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged.

```
jira.edit_issue("TC-8002", fields={
  "labels": ["CVE-2026-28940", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 5. Assign to current user

PROPOSAL: Assign TC-8002 to the current user (already proposed in Step 0.7).

## Remediation Tasks

**None required.** No supported versions are affected. No remediation tasks are created.

## Cross-Stream Impact

Checked all configured streams (2.1.x and 2.2.x). No versions in any stream are affected by CVE-2026-28940. No cross-stream impact exists.

## Summary

TC-8002 (CVE-2026-28940, serde_json < 1.0.135) is not a real vulnerability for this product. All supported versions across both the 2.1.x and 2.2.x streams ship serde_json at version 1.0.137 or higher, which already includes the stack overflow fix introduced in 1.0.135. The recommended action is to close the issue as "Not a Bug" with VEX justification "Vulnerable Code not Present", and no remediation tasks are needed.
