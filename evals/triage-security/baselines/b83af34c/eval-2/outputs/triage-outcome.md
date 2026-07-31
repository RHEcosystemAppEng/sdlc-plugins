# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Case C -- Close as Not a Bug (not affected)

The version impact analysis shows **NO** (not affected) for **all** supported versions across both streams. Every version ships serde_json at a version that is at or above the fix threshold of 1.0.135:

- 2.1.0: serde_json 1.0.137 (not affected)
- 2.1.1: serde_json 1.0.137 (not affected)
- 2.2.0: serde_json 1.0.138 (not affected)
- 2.2.1: serde_json 1.0.138 (not affected)
- 2.2.2: retag of 2.2.1, same serde_json 1.0.138 (not affected)
- 2.2.3: serde_json 1.0.139 (not affected)
- 2.2.4: serde_json 1.0.139 (not affected)

Per Step 8 Case C of the triage-security skill, the recommendation is to close the issue.

## Proposed Jira Actions

### 1. Add closing comment to TC-8002

The following comment documents the version impact evidence:

> No supported versions ship a vulnerable version of serde_json.
>
> Version impact analysis for CVE-2026-28940 (serde_json < 1.0.135):
>
> | Version | serde_json Version | Affected? |
> |---------|--------------------|-----------|
> | 2.1.0 | 1.0.137 | NO |
> | 2.1.1 | 1.0.137 | NO |
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | 1.0.138 (retag of 2.2.1) | NO |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json >= 1.0.135, which is outside the affected range (versions before 1.0.135). The vulnerable version of serde_json is not present in any supported product version.

### 2. Transition TC-8002 to Closed with resolution "Not a Bug"

```
jira.transition_issue(TC-8002, <closed-transition-id>, resolution="Not a Bug")
```

### 3. Set VEX Justification

The VEX Justification custom field (customfield_12345) is configured. Set it to **"Component not Present"**.

Rationale: The lock file analysis shows that the vulnerable package version (serde_json < 1.0.135) is not included in any supported product version. All versions ship serde_json at 1.0.137 or later, which is above the fix threshold. Per the VEX Justification table in the skill, "Component not Present" is the default when "the lock file or SBOM analysis shows the vulnerable package version is not included."

```
jira.edit_issue(TC-8002, fields={
  "customfield_12345": {"value": "Component not Present"}
})
```

### 4. Add ai-cve-triaged label

```
jira.edit_issue(TC-8002, fields={
  "labels": ["CVE-2026-28940", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

## Remediation Tasks

**None created.** Case C does not create any remediation tasks. There is no upstream backport task and no downstream propagation task, because no supported version is affected.

## Cross-Stream Impact

Not applicable. This is a Case C closure (no versions affected in any stream), so no cross-stream impact analysis is needed -- the vulnerability does not affect any stream.
