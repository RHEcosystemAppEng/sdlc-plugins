# Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision: Case C -- No Supported Versions Affected

**Close as "Not a Bug" (not affected).**

The version impact analysis shows that **no supported versions** ship a vulnerable version of serde_json. All supported versions across both the 2.1.x and 2.2.x streams ship serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerable range (versions before 1.0.135) was never present in any shipped product release.

- Earliest serde_json version found: **1.0.137** (in 2.1.0 and 2.1.1)
- Fix threshold: **1.0.135**
- All versions ship a patched dependency.

## Affects Versions Correction

The PSIRT-assigned Affects Versions field lists **RHTPA 2.2.0**. Lock file analysis confirms that RHTPA 2.2.0 ships serde_json 1.0.138, which is NOT vulnerable. The Affects Versions field is **incorrect** -- no versions should be listed as affected.

**Proposed action**: Remove RHTPA 2.2.0 from Affects Versions (clear the field), since no supported versions are actually affected.

## VEX Justification

**Value**: Component not Present

**Rationale**: The vulnerable package version (serde_json < 1.0.135) is not included in any supported product version. All versions ship serde_json >= 1.0.137, which is well above the fix threshold. Per the skill definition, "Component not Present" is the default when lock file analysis shows the vulnerable package version is not included.

## Proposed Jira Actions

The following Jira mutations would be performed (each requiring engineer confirmation):

### 1. Add `ai-cve-triaged` label
Add the label `ai-cve-triaged` to TC-8002 to mark it as triaged.

### 2. Clear Affects Versions
Remove RHTPA 2.2.0 from the Affects Versions field, since no versions are actually affected by this CVE.

### 3. Post triage summary comment
Add a comment to TC-8002 documenting:
- The version impact table (all versions NOT affected)
- The Affects Versions correction (removed RHTPA 2.2.0)
- The triage outcome (closed as Not a Bug -- not affected)
- @mention of the issue reporter

Example comment:
```
No supported versions ship a vulnerable version of serde_json.

Version impact analysis for CVE-2026-28940 (serde_json < 1.0.135):

| Version | serde_json | Affected? |
|---------|------------|-----------|
| 2.1.0   | 1.0.137    | NO        |
| 2.1.1   | 1.0.137    | NO        |
| 2.2.0   | 1.0.138    | NO        |
| 2.2.1   | 1.0.138    | NO        |
| 2.2.2   | 1.0.138    | NO (retag of 2.2.1) |
| 2.2.3   | 1.0.139    | NO        |
| 2.2.4   | 1.0.139    | NO        |

All supported versions ship serde_json >= 1.0.137, which is outside the affected range (< 1.0.135).

Affects Versions corrected: removed RHTPA 2.2.0 (not actually affected).

Closing as Not a Bug -- VEX Justification: Component not Present.
```

### 4. Set VEX Justification field
Set `customfield_12345` (VEX Justification) to "Component not Present".

### 5. Transition to Closed
Transition TC-8002 to **Closed** with resolution **Not a Bug**.

## Remediation Tasks

**None required.** No supported versions are affected, so no remediation tasks need to be created. No upstream backport or downstream propagation is needed.

## Cross-Stream Impact

No cross-stream impact. The 2.1.x stream is also not affected (serde_json 1.0.137 across all versions). No cross-stream notices or proactive remediation tasks are needed.
