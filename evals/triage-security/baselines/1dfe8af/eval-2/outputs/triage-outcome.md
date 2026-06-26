# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Close as Not a Bug (Not Affected)

This is **Case C** from the triage-security skill: no supported versions are affected.

The version impact analysis shows that **all** supported product versions (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) ship serde_json >= 1.0.135, which is at or above the fix threshold for CVE-2026-28940. The vulnerable range (serde_json < 1.0.135) was never included in any supported release.

## Remediation Tasks

**None.** No remediation tasks should be created because no supported versions are affected.

## Proposed Jira Actions

The following Jira mutations would be proposed to the engineer for confirmation:

### 1. Add triage comment with version impact evidence

Post a comment to TC-8002 documenting the version impact analysis:

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
> All supported versions ship serde_json >= 1.0.137, which is outside the affected range (< 1.0.135). The vulnerable version was never shipped.

### 2. Transition to Closed with resolution "Not a Bug"

Close TC-8002 with resolution "Not a Bug" since the product is not affected by this vulnerability.

### 3. Set VEX Justification

Set the VEX Justification custom field (`customfield_12345`) to **"Component not Present"**.

Rationale: The vulnerable version of serde_json (< 1.0.135) is not present in any supported product version. All versions ship a fixed version (1.0.137 or later), so the vulnerable component version was never included. "Component not Present" is the appropriate VEX justification because the specific vulnerable version of the package is not shipped.

### 4. Add `ai-cve-triaged` label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged.

### 5. Assign to current user

Assign TC-8002 to the current user upon closure.

## Rationale

The PSIRT auto-created this Vulnerability issue based on a CVE scan that flagged serde_json as a dependency of the rhtpa-server component. However, the actual lock file analysis at each pinned source commit shows that the product has always shipped serde_json 1.0.137 or later -- versions that already include the recursion limit fix introduced in 1.0.135. The PSIRT scan likely matched the package name without performing a version comparison against shipped builds.

No cross-stream impact exists because no stream is affected. No sibling issues need attention for the same reason.
