# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Triage Decision: Case C -- Close as Not a Bug (not affected)

### Rationale

The version impact analysis shows that **no supported product version** ships a vulnerable version of serde_json. The CVE-2026-28940 fix threshold is serde_json 1.0.135. All versions across both the 2.1.x and 2.2.x streams ship serde_json >= 1.0.137, which is above the fix threshold.

| Stream | Versions checked | Minimum serde_json version found | Fix threshold | Result |
|--------|-----------------|----------------------------------|---------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | 1.0.137 | 1.0.135 | NOT AFFECTED |
| 2.2.x | 2.2.0 -- 2.2.4 | 1.0.138 | 1.0.135 | NOT AFFECTED |

### VEX Justification

Since the VEX Justification custom field is configured (`customfield_12345`), set it to:

**Component not Present** (the vulnerable version of serde_json is not included in any supported release -- all shipped versions are above the fix threshold).

## Proposed Jira Actions

The following Jira mutations would be performed (each requiring engineer confirmation in interactive mode):

### 1. Add comment documenting the triage finding

Post to TC-8002:

> No supported versions ship a vulnerable version of serde_json.
> Version impact analysis shows all versions ship serde_json >= 1.0.137,
> which is above the affected range (versions before 1.0.135).
>
> | Version | serde_json | Affected? |
> |---------|-----------|-----------|
> | 2.1.0 | 1.0.137 | NO |
> | 2.1.1 | 1.0.137 | NO |
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | 1.0.138 | NO (retag of 2.2.1) |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |
>
> Closing as Not a Bug -- not affected.

### 2. Set VEX Justification custom field

```
jira.edit_issue("TC-8002", fields={
  "customfield_12345": "Component not Present"
})
```

### 3. Correct Affects Versions

The PSIRT-assigned Affects Version is `RHTPA 2.2.0`, but since no versions are actually affected, remove all Affects Versions:

```
Current: [RHTPA 2.2.0]
Proposed: [] (empty -- no versions affected)
```

Alternatively, retain the PSIRT-assigned value for traceability and document in the closing comment that the version is not actually affected.

### 4. Transition to Closed

```
jira.transition_issue("TC-8002", resolution="Not a Bug")
```

### 5. Assign to current user

```
jira.edit_issue("TC-8002", assignee=<current-user-account-id>)
```

### 6. Add ai-cve-triaged label

```
jira.edit_issue("TC-8002", fields={
  "labels": ["CVE-2026-28940", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

## Steps Skipped or Not Applicable

| Step | Reason |
|------|--------|
| Step 1.7 (Embargo Check) | CVSS 5.3 is below the 7.0 threshold; no embargo policy check needed |
| Step 4 (Duplicate/Sibling Check) | No external Jira calls permitted in this eval |
| Step 5 (Lifecycle Check) | No external product pages call permitted in this eval |
| Step 6 (Already Fixed Check) | No sibling issues to cross-reference |
| Step 7 (Concurrent Triage) | Upstream Affected Component custom field not configured |
| Step 7.5 (Release Jira) | No remediation tasks needed (Case C) |
| Step 8 (Remediation) | Case C -- no supported versions affected; no remediation tasks created |

## Summary

TC-8002 (CVE-2026-28940) is a false positive for this product. The vulnerable serde_json versions (before 1.0.135) were never shipped in any supported product version. All versions ship serde_json 1.0.137 or later. The recommended action is to close the Vulnerability issue as "Not a Bug" with VEX Justification "Component not Present" and add the `ai-cve-triaged` label.
