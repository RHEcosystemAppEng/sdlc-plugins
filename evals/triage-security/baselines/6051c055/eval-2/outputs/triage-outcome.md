# Triage Outcome — TC-8002 (CVE-2026-28940)

## Decision: Case C — Close as Not a Bug

**No supported versions are affected.** The version impact analysis shows that all supported product versions (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) ship serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerable version range (before 1.0.135) was never included in any supported release.

## Rationale

CVE-2026-28940 affects serde_json versions before 1.0.135. The fix (a configurable recursion limit defaulting to 128 levels of nesting) was introduced in serde_json 1.0.135.

Every supported version ships a serde_json version that already includes this fix:

- Stream 2.1.x ships serde_json 1.0.137
- Stream 2.2.x ships serde_json 1.0.138 or 1.0.139

The PSIRT-assigned Affects Version (RHTPA 2.2.0) is incorrect — version 2.2.0 ships serde_json 1.0.138, which is not vulnerable.

## Proposed Jira Actions

The following Jira mutations would be proposed to the engineer for confirmation:

### 1. Affects Versions Correction (Step 3)

Current Affects Versions: `[RHTPA 2.2.0]`
Proposed Affects Versions: `[]` (empty — no versions are affected)

Since this is a Case C closure, the Affects Versions correction is implicit in the closure action.

### 2. Post Triage Comment

Add comment to TC-8002:

> No supported versions ship a vulnerable version of serde_json. Version impact analysis:
>
> | Version | serde_json | Affected? |
> |---------|------------|-----------|
> | 2.1.0 | 1.0.137 | NO |
> | 2.1.1 | 1.0.137 | NO |
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | 1.0.138 | NO (retag of 2.2.1) |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json >= 1.0.137, which is outside the affected range (< 1.0.135). The fix (recursion limit) has been included since serde_json 1.0.135.

### 3. Close Issue

- Transition TC-8002 to **Closed** with resolution **Not a Bug**.

### 4. Set VEX Justification

Since the VEX Justification custom field is configured (customfield_12345), set it to:

**Component not Present** — the vulnerable version of the package (serde_json < 1.0.135) is not included in any supported product version. All versions ship serde_json >= 1.0.137.

```
jira.edit_issue("TC-8002", fields={
  "customfield_12345": {"value": "Component not Present"}
})
```

Note: "Component not Present" is the appropriate VEX justification because the vulnerable *version* of the component is not present — all shipped versions are at or above the fix threshold.

### 5. Add ai-cve-triaged Label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged.

### 6. Post-Triage Summary Comment

Post a summary comment to TC-8002 documenting the complete triage outcome, including:
- Version impact table
- Triage decision (Case C: Not a Bug)
- VEX justification applied
- @mention of the issue reporter (PSIRT analyst)

## Steps Skipped or Not Applicable

- **Step 1.7 (Embargo Check)**: Skipped — CVSS 5.3 (Medium) is below the embargo threshold (>= 7.0), and no Embargo policy URL is configured.
- **Step 4 (Duplicate/Sibling Check)**: No siblings searched in this eval (mock data). In a real triage, JQL would be run.
- **Step 4.3 (Cross-CVE Overlap)**: Skipped — Upstream Affected Component custom field is not configured.
- **Step 5 (Version Lifecycle Check)**: Not applicable for Case C closure — no affected versions to check lifecycle status for.
- **Step 6 (Already Fixed Check)**: Not applicable — no versions are affected, so "already fixed" is not the right framing. This is "never affected."
- **Step 7 (Concurrent Triage Detection)**: Skipped — Upstream Affected Component custom field is not configured.
- **Step 8 Case A/B (Remediation Tasks)**: Not applicable — no remediation needed since no versions are affected.
