# Step 7 -- Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision: Case C -- Close as Not a Bug

No supported versions ship a vulnerable version of serde_json. The version impact analysis confirms that **all** supported versions across both streams (2.1.x and 2.2.x) ship serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerability (serde_json < 1.0.135) does not affect any shipped product version.

## Rationale

The CVE describes a stack overflow vulnerability in serde_json versions before 1.0.135. Lock file inspection at every pinned source commit in the supportability matrix shows:

- Stream 2.1.x: serde_json 1.0.137 (both versions)
- Stream 2.2.x: serde_json 1.0.138 -- 1.0.139 (all five versions)

Since the minimum serde_json version shipped (1.0.137) already exceeds the fix threshold (1.0.135), no remediation is needed. No remediation tasks should be created.

## Proposed Jira Actions

The following actions should be taken on TC-8002, pending engineer confirmation:

### 1. Add Close Comment

Post a comment to TC-8002 documenting the version impact evidence:

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
> All supported versions ship serde_json >= 1.0.137, which is outside the affected range (< 1.0.135). The fix (recursion depth limit) has been present in all shipped versions since their initial release.
>
> Closing as Not a Bug (not affected).

The comment must include the Comment Footnote per `shared/comment-footnote.md` and an @mention of the issue reporter.

### 2. Transition to Closed

- Resolution: **Not a Bug**

### 3. Set VEX Justification

The VEX Justification custom field (`customfield_12345`) is configured in Security Configuration. Set it to:

- **Value**: `Component not Present`
- **Rationale**: The vulnerable version of serde_json (< 1.0.135) is not present in any supported product version. All versions ship a patched version (>= 1.0.137) that includes the recursion depth limit fix.

```
jira.edit_issue("TC-8002", fields={
  "customfield_12345": "Component not Present"
})
```

### 4. Assign to Current User

Assign TC-8002 to the current user to indicate ownership of the triage decision.

### 5. Add ai-cve-triaged Label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged and prevent re-triage.

## Actions NOT Taken

- **No remediation tasks created** -- not needed since no versions are affected
- **No Affects Versions correction** -- the current Affects Version (RHTPA 2.2.0) will be cleared or left as-is depending on engineer preference, since the product is not actually affected
- **No cross-stream remediation** -- no streams are affected, so Case B does not apply
