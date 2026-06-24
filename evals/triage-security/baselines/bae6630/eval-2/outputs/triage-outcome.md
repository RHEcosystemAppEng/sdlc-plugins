# Triage Outcome — TC-8002

## Decision: Close as Not a Bug (Not Affected)

**CVE-2026-28940** (serde_json stack overflow on deeply nested input) does **not** affect any supported product version. This is **Case C** from the triage-security skill: no supported versions ship a vulnerable version of the dependency.

### Rationale

- The vulnerability affects serde_json versions **before 1.0.135**.
- The **lowest** serde_json version found across all supported product versions is **1.0.137** (streams 2.1.0 and 2.1.1).
- The scoped stream (2.2.x) ships serde_json **1.0.138–1.0.139** across all versions.
- All supported versions are already patched — the fixed version (1.0.135) was available before any currently supported release was built.

### Proposed Jira Actions

The following Jira mutations would be proposed to the engineer for confirmation:

#### 1. Affects Versions Correction (Step 3)

The current Affects Versions (`RHTPA 2.2.0`) is incorrect — version 2.2.0 ships serde_json 1.0.138, which is not vulnerable.

- **Current**: `[RHTPA 2.2.0]`
- **Proposed**: `[]` (empty — no versions are affected)

Since the recommendation is to close as Not a Bug, the Affects Versions field would be cleared or left as-is depending on project conventions. The close comment documents the evidence.

#### 2. Add Triage Comment

Post a summary comment to TC-8002:

> No supported versions ship a vulnerable version of serde_json.
> Version impact analysis:
>
> | Stream | Version | serde_json | Affected? |
> |--------|---------|------------|-----------|
> | 2.1.x | 2.1.0 | 1.0.137 | NO |
> | 2.1.x | 2.1.1 | 1.0.137 | NO |
> | 2.2.x | 2.2.0 | 1.0.138 | NO |
> | 2.2.x | 2.2.1 | 1.0.138 | NO |
> | 2.2.x | 2.2.2 | 1.0.138 | NO (retag of 2.2.1) |
> | 2.2.x | 2.2.3 | 1.0.139 | NO |
> | 2.2.x | 2.2.4 | 1.0.139 | NO |
>
> All supported versions ship serde_json >= 1.0.137, which is above the fix
> threshold of 1.0.135. The vulnerability (CVE-2026-28940) does not affect
> this product.

#### 3. Set VEX Justification

Since the VEX Justification custom field is configured (`customfield_12345`), set it to:

- **Value**: `Vulnerable Code not Present`

Justification: While serde_json is a dependency in all supported versions, the shipped versions (1.0.137+) all include the fix for CVE-2026-28940 (the recursion limit introduced in 1.0.135). The vulnerable code path (unbounded recursion during deserialization) is not present in the shipped versions.

Note: `Component not Present` would be incorrect here because serde_json IS present in the dependency tree — it is simply at a version that already contains the fix.

#### 4. Transition to Closed

- **Resolution**: Not a Bug
- **Assignee**: Set to current user

#### 5. Add `ai-cve-triaged` Label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged and prevent re-triage.

### No Remediation Tasks Required

Since no supported versions are affected, no remediation tasks (upstream backport or downstream propagation) are needed. No cross-stream impact to report — the 2.1.x stream is also not affected.

### Summary of Triage Steps Completed

| Step | Name | Result |
|------|------|--------|
| 0 | Validate Configuration | Passed — all required sections present |
| 1 | Data Extraction | CVE-2026-28940, serde_json < 1.0.135, scoped to 2.2.x |
| 1.5 | External CVE Enrichment | Skipped (eval mode — used Jira description data) |
| 2 | Version Impact Analysis | All versions ship serde_json >= 1.0.137 — none affected |
| 3 | Affects Versions Correction | RHTPA 2.2.0 incorrectly listed — should be cleared |
| 4 | Duplicate/Sibling Check | Not performed (no Jira access in eval mode) |
| 5 | Version Lifecycle Check | Not performed (no web access in eval mode) |
| 6 | Already Fixed Check | N/A — no versions are affected regardless |
| 7 | Remediation | Case C: Close as Not a Bug — no remediation needed |
