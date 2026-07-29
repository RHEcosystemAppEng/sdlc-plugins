# Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision: Case C -- No Supported Versions Affected

**Recommendation: Close as Not a Bug (not affected)**

The version impact analysis shows that **no supported versions** ship a vulnerable version of serde_json. All versions across both the 2.1.x and 2.2.x streams ship serde_json >= 1.0.135, which is at or above the fix threshold.

| Stream | Versions checked | serde_json range shipped | All patched? |
|--------|-----------------|-------------------------|--------------|
| 2.1.x | 2.1.0, 2.1.1 | 1.0.137 | YES |
| 2.2.x | 2.2.0 -- 2.2.4 | 1.0.138 -- 1.0.139 | YES |

## Proposed Jira Actions

The following Jira mutations would be presented to the engineer for confirmation before execution:

### 1. Affects Versions Correction (Step 3)

- **Current**: RHTPA 2.2.0
- **Proposed**: Remove RHTPA 2.2.0 (version is not actually affected)
- **Rationale**: Lock file analysis at pinned commit v0.4.5 shows serde_json 1.0.138, which is above the fix threshold of 1.0.135. RHTPA 2.2.0 is not affected.

### 2. Close Issue Comment

Post the following comment to TC-8002:

> No supported versions ship a vulnerable version of serde_json. Version impact
> analysis confirms all supported versions ship serde_json >= 1.0.137, which is
> outside the affected range (< 1.0.135).
>
> Version Impact:
>
> | Version | serde_json | Affected? |
> |---------|-----------|-----------|
> | 2.1.0 | 1.0.137 | NO |
> | 2.1.1 | 1.0.137 | NO |
> | 2.2.0 | 1.0.138 | NO |
> | 2.2.1 | 1.0.138 | NO |
> | 2.2.2 | -- | NO (retag of 2.2.1) |
> | 2.2.3 | 1.0.139 | NO |
> | 2.2.4 | 1.0.139 | NO |

The comment would include an @mention of the issue reporter (the PSIRT analyst) and the Comment Footnote per skill requirements.

### 3. Transition to Closed

- **Resolution**: Not a Bug
- **Rationale**: The vulnerable serde_json version range (< 1.0.135) was never shipped in any supported product version

### 4. VEX Justification

Since the VEX Justification custom field is configured (customfield_12345), set it to:

- **Value**: Component not Present
- **Rationale**: The vulnerable version range of serde_json (< 1.0.135) is not present in any supported version. All builds include serde_json >= 1.0.137, which contains the stack overflow fix. The "Component not Present" justification applies because the *vulnerable component version* is not included -- even though serde_json itself is present, the vulnerable version of serde_json is not shipped.

### 5. Add ai-cve-triaged Label

Add the `ai-cve-triaged` label to TC-8002 to mark it as triaged and prevent re-triage.

## Remediation Tasks

**None required.** Since no supported versions are affected (Case C), no remediation tasks are created.

## Steps Completed

| Step | Name | Result |
|------|------|--------|
| 0 | Validate Configuration | PASS -- Security Configuration present with all required fields |
| 0.3 | Matrix Staleness Check | WARNING -- matrix is 31 days old (exceeds 14-day threshold), but data is conclusive |
| 1 | Data Extraction | Parsed CVE-2026-28940, serde_json < 1.0.135, fixed 1.0.135 |
| 1.5 | External CVE Enrichment | Skipped (eval -- no external API calls) |
| 1.7 | Embargo Check | SKIP -- CVSS 5.3 (Medium) is below the 7.0 threshold |
| 2 | Version Impact Analysis | All versions ship serde_json >= 1.0.137 -- none affected |
| 3 | Affects Versions Correction | Proposed: remove RHTPA 2.2.0 (not affected) |
| 4 | Duplicate/Sibling Check | Skipped (eval -- no Jira queries) |
| 5 | Version Lifecycle Check | Skipped (eval -- no WebFetch) |
| 6 | Already Fixed Check | Not applicable -- no versions are affected |
| 7 | Concurrent Triage Detection | SKIP -- Upstream Affected Component field not configured |
| 8 | Remediation | Case C: Close as Not a Bug, set VEX Justification |
