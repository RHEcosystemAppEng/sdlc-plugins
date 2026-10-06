# Triage Outcome — TC-8002 (CVE-2026-28940)

## Decision: Case C — No Supported Versions Affected

**Recommendation: Close as Not a Bug (not affected)**

All supported product versions across both the scoped stream (2.2.x) and the cross-stream (2.1.x) ship serde_json >= 1.0.137, which is above the CVE fix threshold of 1.0.135. No remediation is required.

## Evidence Summary

The vulnerability (CVE-2026-28940) affects serde_json versions before 1.0.135. Lock file analysis at every pinned source commit in the supportability matrix confirms that no supported version has ever shipped a vulnerable version of serde_json:

- **2.1.x stream**: all versions ship serde_json 1.0.137
- **2.2.x stream**: versions 2.2.0-2.2.2 ship serde_json 1.0.138; versions 2.2.3-2.2.4 ship serde_json 1.0.139

The minimum serde_json version across all supported builds is 1.0.137, which is 2 patch versions above the fix threshold (1.0.135).

## Proposed Jira Actions

The following Jira mutations would be proposed to the engineer for confirmation:

### 1. Add triage comment to TC-8002

```
No supported versions ship a vulnerable version of serde_json.
Version impact analysis shows all supported versions ship serde_json >= 1.0.137,
which is outside the affected range (< 1.0.135).

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Stream | Version | serde_json | Affected? |
|--------|---------|------------|-----------|
| 2.1.x  | 2.1.0   | 1.0.137    | NO        |
| 2.1.x  | 2.1.1   | 1.0.137    | NO        |
| 2.2.x  | 2.2.0   | 1.0.138    | NO        |
| 2.2.x  | 2.2.1   | 1.0.138    | NO        |
| 2.2.x  | 2.2.2   | 1.0.138    | NO (retag of 2.2.1) |
| 2.2.x  | 2.2.3   | 1.0.139    | NO        |
| 2.2.x  | 2.2.4   | 1.0.139    | NO        |

Closing as Not a Bug — the vulnerable serde_json version (< 1.0.135)
was never shipped in any supported product version.

@<reporter> (PSIRT notification)

[Comment Footnote per shared/comment-footnote.md, skill: triage-security]
```

### 2. Transition TC-8002 to Closed

- **Resolution**: Not a Bug
- **Rationale**: The vulnerable version of serde_json (< 1.0.135) is not present in any supported product version. All versions ship serde_json >= 1.0.137.

### 3. Set VEX Justification

- **Field**: customfield_12345
- **Value**: Component not Present
- **Rationale**: The vulnerable package version (serde_json < 1.0.135) is not included in any supported build. Per skill guidance, "Component not Present" is the default when lock file analysis shows the vulnerable package version is not included.

The Jira API call would be:

```
jira.edit_issue("TC-8002", fields={
  "customfield_12345": "Component not Present"
})
```

### 4. Add `ai-cve-triaged` label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged:

```
jira.edit_issue("TC-8002", fields={
  "labels": ["CVE-2026-28940", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

## Steps Skipped or Not Applicable

| Step | Reason |
|------|--------|
| Step 1.7 (Embargo Check) | No embargo policy URL configured; CVSS 5.3 is below the 7.0 threshold |
| Step 2.3.5 (Dependency Chain) | No affected versions -- chain tracing unnecessary |
| Step 2.5 (Upstream Fix Check) | No affected versions -- upstream check unnecessary |
| Step 3 (Affects Versions Correction) | Issue will be closed; Affects Versions correction is moot |
| Step 4.3 (Cross-CVE Overlap) | Upstream Affected Component field not configured |
| Step 4.4 (Preemptive Reconciliation) | No remediation needed -- no tasks to reconcile |
| Step 5 (Lifecycle Check) | No affected versions -- lifecycle check unnecessary |
| Step 6 (Already Fixed Check) | No affected versions -- already-fixed check unnecessary |
| Step 7 (Concurrent Triage) | Upstream Affected Component field not configured; also no remediation tasks to create |
| Step 8 Case A (Cross-Stream) | No affected versions in any stream |
| Step 8 Case B (Remediation Tasks) | No affected versions -- no remediation needed |

## Conclusion

This is a straightforward Case C closure. The patched dependency (serde_json >= 1.0.135) was already present in all supported product versions before this CVE was filed. The recommended action is to close TC-8002 as "Not a Bug" with VEX Justification "Component not Present" and label `ai-cve-triaged`.
