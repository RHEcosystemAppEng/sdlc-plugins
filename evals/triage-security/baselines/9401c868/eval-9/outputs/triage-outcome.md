# Triage Outcome: TC-8011 (CVE-2026-45678)

## Summary

**Decision: Case B -- Affected, create new remediation tasks**

The cross-CVE overlap analysis (Step 4.3) found a related CVE (TC-8012 / CVE-2026-43210) affecting the same upstream component (webpack) in the same stream (rhtpa-2.2). However, the existing remediation task TC-8013 bumps webpack only to 5.96.1, which does **not** meet the current CVE's fix threshold of 5.98.0.

Because no existing remediation covers CVE-2026-45678, new remediation tasks must be created.

## Rationale

1. **CVE-2026-45678** requires webpack >= 5.98.0 to resolve the arbitrary code execution vulnerability via loader chain path traversal.
2. **TC-8013** (the only existing remediation for webpack in this stream) bumps webpack to 5.96.1 -- this was sufficient for CVE-2026-43210 (ReDoS, fix threshold >= 5.96.0) but falls short of the 5.98.0 threshold needed for CVE-2026-45678.
3. The version gap (5.96.1 vs 5.98.0) means a new, independent remediation is required.

## Remediation Plan

- **Ecosystem**: npm (source dependency)
- **Stream**: 2.2.x (scoped per issue suffix `[rhtpa-2.2]`)
- **Tasks per stream**: 2 (dependency bump + downstream propagation)

### Task 1: Dependency Bump (upstream)

- **Summary**: Remediate CVE-2026-45678: update webpack to 5.98.0 (rhtpa-2.2)
- **Repository**: rhtpa-ui (source repo, per component label pscomponent:org/rhtpa-ui)
- **Action**: `npm update webpack` or explicitly pin webpack >= 5.98.0 in package.json
- **Labels**: ai-generated-jira, Security, CVE-2026-45678
- **Link**: Depend on TC-8011

### Task 2: Downstream Propagation

- **Summary**: Propagate CVE-2026-45678 fix: update rhtpa-ui ref in rhtpa-release.0.4.z (rhtpa-2.2)
- **Repository**: rhtpa-release.0.4.z (Konflux release repo for 2.2.x stream)
- **Action**: Update the rhtpa-ui source reference to the commit/tag that includes the webpack bump
- **Labels**: ai-generated-jira, Security, CVE-2026-45678
- **Link**: Blocked by Task 1, Depend on TC-8011

## Cross-Stream Impact (Case A Check)

The issue is scoped to stream 2.2.x (`[rhtpa-2.2]`). Stream 2.1.x also exists in the Version Streams configuration. A full version impact analysis across all streams would be needed to determine if 2.1.x is also affected. If 2.1.x ships webpack < 5.98.0 and has no CVE Jira for CVE-2026-45678, preemptive remediation tasks would be created for that stream with the `security-preemptive` label and a "Related" link to TC-8011.

## Release Jira Orchestration (Step 7.5)

After remediation tasks are created, they would be linked to the release Task for the 2.2.x stream (pattern: "RHTPA 2.2.5 CVE triage" under a "RHTPA 2.2.5 Release Tasks" Epic, based on next patch version after 2.2.4 in the supportability matrix).

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8011
2. Post summary comment to TC-8011 with version impact table, remediation task links, and @mention of the reporter
3. Transition TC-8011 to In Progress
