# Triage Outcome -- TC-8002

## Decision: Close as Not a Bug (Not Affected)

This is **Case C** per the triage-security skill: no supported versions are affected.

### Rationale

CVE-2026-28940 affects serde_json versions **before 1.0.135**. Lock file analysis at every pinned commit across both supported version streams shows that all product versions ship serde_json **1.0.137 or later**, well above the fix threshold.

| Version | serde_json | Affected? |
|---------|-----------|-----------|
| 2.1.0 | 1.0.137 | NO |
| 2.1.1 | 1.0.137 | NO |
| 2.2.0 | 1.0.138 | NO |
| 2.2.1 | 1.0.138 | NO |
| 2.2.2 | 1.0.138 | NO (retag of 2.2.1) |
| 2.2.3 | 1.0.139 | NO |
| 2.2.4 | 1.0.139 | NO |

The vulnerability does not affect any shipped product version. The fix (1.0.135) was already present in the dependency tree before the earliest supported version (2.1.0, built 2025-09-15) was released.

### Affects Versions Correction (Step 3)

**Current Affects Versions**: RHTPA 2.2.0
**Proposed Affects Versions**: (empty -- remove RHTPA 2.2.0)

RHTPA 2.2.0 ships serde_json 1.0.138, which is not vulnerable. The PSIRT-assigned Affects Version is incorrect and should be removed. Since no versions are affected, the Affects Versions field should be cleared entirely.

### Duplicate / Sibling Check (Step 4)

Proposed action: Search JQL `project = TC AND labels = 'CVE-2026-28940' AND issuetype = 10024 AND key != TC-8002` to identify sibling issues. Since this issue will be closed as Not a Bug, sibling issues covering other streams (if any) would also be candidates for closure with the same rationale (no stream ships a vulnerable version).

### Version Lifecycle Check (Step 5)

Would verify lifecycle status at https://access.example.com/product-life-cycle/rhtpa. Since the outcome is "not affected" regardless of lifecycle status, this check does not change the triage decision.

### Already Fixed Check (Step 6)

Not applicable -- the product was never vulnerable in the first place (the fixed version was already in the dependency tree before any product version shipped). This is distinct from an "already fixed" scenario where a sibling resolved the issue; here, the vulnerability simply never existed in shipped product versions.

## Proposed Jira Actions

The following actions are presented for engineer confirmation. No mutations would be executed without explicit approval.

### 1. Remove incorrect Affects Version

```
Proposed: jira.edit_issue("TC-8002", fields={
  "versions": []
})
```

Rationale: RHTPA 2.2.0 is not affected (ships serde_json 1.0.138, fix threshold is 1.0.135). Remove the PSIRT-assigned Affects Version.

### 2. Add triage comment

```
Proposed: jira.add_comment("TC-8002", 
  "No supported versions ship a vulnerable version of serde_json. 
   Version impact analysis:

   | Version | serde_json | Affected? |
   |---------|-----------|-----------|
   | 2.1.0   | 1.0.137   | NO        |
   | 2.1.1   | 1.0.137   | NO        |
   | 2.2.0   | 1.0.138   | NO        |
   | 2.2.1   | 1.0.138   | NO        |
   | 2.2.2   | 1.0.138   | NO (retag of 2.2.1) |
   | 2.2.3   | 1.0.139   | NO        |
   | 2.2.4   | 1.0.139   | NO        |

   All supported versions ship serde_json >= 1.0.137 which is outside the 
   affected range (versions before 1.0.135). The fix was already present in 
   the dependency tree before any supported product version was built.

   CVE: CVE-2026-28940
   CVSS: 5.3 (Medium)
   Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk

   @reporter-mention (ADF mention node for the issue reporter)")
```

### 3. Set VEX Justification

```
Proposed: jira.edit_issue("TC-8002", fields={
  "customfield_12345": "Component not Present"
})
```

Rationale: While the serde_json package IS present in the build, no version ships a vulnerable version of it. The vulnerable component (serde_json < 1.0.135) is not present in any shipped product version. The VEX Justification custom field (customfield_12345) is configured in this project.

Note: An alternative justification of "Vulnerable Code not Present" could also apply since the patched version (1.0.135+) contains the fix that removes the vulnerable code path. The recommended value is "Component not Present" per the skill's default guidance -- the vulnerable version of the component is not shipped.

### 4. Transition to Closed

```
Proposed: jira.transition_issue("TC-8002", resolution="Not a Bug")
```

### 5. Assign to current user

```
Proposed: jira.edit_issue("TC-8002", fields={
  "assignee": {"accountId": "<current-user-account-id>"}
})
```

### 6. Add ai-cve-triaged label

```
Proposed: jira.edit_issue("TC-8002", fields={
  "labels": ["CVE-2026-28940", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

## No Remediation Tasks Required

Since no supported versions are affected, no remediation tasks are created. This is Case C of the triage-security skill's remediation decision tree.

## Cross-Stream Impact

The version impact analysis covered both configured streams (2.1.x and 2.2.x). Neither stream is affected. No cross-stream remediation or notifications are required.
