# Triage Outcome for TC-8020

## Summary

**Issue**: TC-8020 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: >= 0.11.14
**CVSS**: 7.5 (High)
**Stream scope**: 2.2.x (scoped by summary suffix `[rhtpa-2.2]`)
**Upstream Affected Component**: quinn-proto (customfield_10632)

## Triage Decision: Case B (Affected) + Case A (Cross-stream Impact)

### Rationale

Within the scoped stream (2.2.x), versions **2.2.0, 2.2.1, and 2.2.2** ship quinn-proto versions below the fix threshold of 0.11.14. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and are not affected.

This is **not** Case C (no versions affected), because three supported versions in the 2.2.x stream are affected. Remediation tasks are required.

Additionally, this is **Case A (cross-stream impact)** because the 2.1.x stream (outside this issue's scope) is also affected: both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is below the fix threshold.

## Step-by-Step Triage Trace

### Step 0.8 -- Assign and Transition (Proposed)

- **Proposed action**: Assign TC-8020 to the current user
- **Proposed action**: Transition TC-8020 from `New` to `Assigned`

### Step 1 -- Data Extraction

See `data-extraction.md` for the full parsed CVE data table.

### Step 1.5 -- External CVE Data Enrichment (Simulated)

External CVE databases (MITRE CVE API and OSV.dev) would be queried for CVE-2026-31812 to cross-validate the fix threshold. For this analysis, the Jira description's fix threshold of 0.11.14 is used as the authoritative value.

### Step 1.7 -- Embargo Check

CVSS is 7.5 (High, >= 7.0 threshold). If an Embargo policy URL were configured, an embargo warning gate would fire. No Embargo policy URL is present in the mock Security Configuration, so this step is **skipped**.

### Step 2 -- Version Impact Analysis

See `data-extraction.md` for the version impact table. Summary:
- **2.2.x stream (in scope)**: 2.2.0, 2.2.1, 2.2.2 affected; 2.2.3, 2.2.4 not affected
- **2.1.x stream (out of scope)**: 2.1.0, 2.1.1 affected (cross-stream impact)
- **Upstream fix status**: Fix is available on `release/0.4.z` (2.2.x stream). Fix is NOT available on `release/0.3.z` (2.1.x stream).

### Step 3 -- Affects Versions Correction (Proposed)

**Current**: `[RHTPA 2.0.0]` (incorrect -- no such version in the supportability matrix)
**Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (scoped to 2.2.x stream)

- **Proposed action**: `jira.edit_issue(TC-8020, fields={"versions": [{"id": "<RHTPA-2.2.0-id>"}, {"id": "<RHTPA-2.2.1-id>"}, {"id": "<RHTPA-2.2.2-id>"}]})`
- **Proposed action**: Post Affects Versions correction comment to TC-8020

### Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

- **Step 4.1/4.2**: JQL search for sibling issues with label `CVE-2026-31812` would be performed. No mock sibling data was provided, so we assume no siblings found.
- **Step 4.3**: Cross-CVE overlap detection using `customfield_10632 ~ 'quinn-proto'`. No mock overlap data provided beyond the concurrent triage in Step 7.
- **Step 4.4**: Preemptive task reconciliation. No mock preemptive task data provided. Assumed no existing preemptive tasks.

### Step 5 -- Version Lifecycle Check

Product lifecycle page at `https://access.example.com/product-life-cycle/rhtpa` would be consulted. No mock lifecycle data was provided. Assumed all affected versions (2.2.0, 2.2.1, 2.2.2) are within support lifecycle.

### Step 6 -- Already Fixed Check

No resolved sibling issues found (Step 4 returned no siblings). Proceeding to Step 7.

### Step 7 -- Concurrent Triage Detection

See `concurrent-triage.md` for the full analysis. **TC-8019 is actively being triaged on the same component (quinn-proto) by engineer-b@example.com.** Triage pauses here until the engineer selects Wait, Skip, or Proceed.

### Step 7.5 -- Release Jira Orchestration (Conditional on Step 7)

If the engineer chooses to proceed past Step 7:

For the 2.2.x stream, the release version would be derived from the latest released version in the supportability matrix. The latest is 2.2.4 (build 0.4.12), so the default proposed release version would be **RHTPA 2.2.5**.

- **Proposed action**: Search for existing release Epic matching `RHTPA 2.2.* Release Tasks`
- **Proposed action**: If not found, create release Epic `RHTPA 2.2.5 Release Tasks` (after engineer confirmation)
- **Proposed action**: Search for/create release Task `RHTPA 2.2.5 CVE triage` under the release Epic
- **Step 7.5.3**: Cross-CVE dedup check -- search the release Task's linked remediation Tasks for existing tasks covering `quinn-proto`. If a covering task exists, skip new task creation and link TC-8020 to the existing task instead.

### Step 8 -- Remediation (Conditional on Step 7)

If the engineer proceeds past Step 7 and no dedup match is found in Step 7.5.3:

#### Case B: Remediation tasks for 2.2.x stream (in scope)

Since the upstream fix is **already available** on `release/0.4.z` (Step 2.5 confirms quinn-proto 0.11.14 at the latest tags), the remediation uses the **dependency bump** variant:

**Task 1 -- Dependency bump**:
- **Summary**: `Remediate CVE-2026-31812: update quinn-proto to 0.11.14 (rhtpa-2.2)`
- **Repository**: rhtpa-backend
- **Target branch**: release/0.4.z
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812"]`
- **Description**: Dependency bump task using `cargo update -p quinn-proto` to pull in version >= 0.11.14
- **Coordination guidance**: "This component is public upstream. Coordinate fix with upstream maintainers if the vulnerability is not yet public. Follow your organization's embargo policy before discussing in public channels or PRs."

**Task 2 -- Downstream propagation**:
- **Summary**: `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)`
- **Repository**: rhtpa-release.0.4.z
- **Target branch**: main
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-31812"]`
- **Blocked by**: Task 1 (dependency bump must merge first)
- **Source pinning method**: `artifacts.lock.yaml` (download URL contains tag)

**Jira linkage (proposed)**:
- `Depend`: TC-8020 (inward) --> Task 1 (outward)
- `Depend`: TC-8020 (inward) --> Task 2 (outward)
- `Blocks`: Task 1 (inward) --> Task 2 (outward) (upstream blocks downstream)
- `Blocks`: Task 1 (inward) --> Release Task (outward)
- `Blocks`: Task 2 (inward) --> Release Task (outward)
- `Related`: Release Task (inward) --> TC-8020 (outward)

#### Case A: Cross-stream impact (2.1.x)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since TC-8020 is scoped to 2.2.x, Case A applies.

**Proposed action**: Post cross-stream impact comment on TC-8020:
```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x
based on lock file analysis. This stream is tracked by companion issues
(see Related links) or may require separate PSIRT triage.
```

**Proposed action**: Search for existing CVE Jiras for CVE-2026-31812 scoped to 2.1.x.

- **If a 2.1.x sibling exists**: Link as Related and skip preemptive task creation for 2.1.x.
- **If no 2.1.x sibling exists**: Create preemptive remediation tasks for the 2.1.x stream:

  **Preemptive Task 1 -- Upstream backport** (fix NOT available on release/0.3.z):
  - Summary: `Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1)`
  - Labels: `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`
  - Link type: `Related` to TC-8020 (not Depend, because originating CVE is for a different stream)

  **Preemptive Task 2 -- Downstream propagation**:
  - Summary: `Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)`
  - Labels: `["ai-generated-jira", "Security", "CVE-2026-31812", "security-preemptive"]`

### Post-Triage Summary (Proposed)

After all triage actions complete:

1. **Proposed action**: Add label `ai-cve-triaged` to TC-8020
2. **Proposed action**: Transition TC-8020 to `In Progress`
3. **Proposed action**: Post summary comment to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction: `[RHTPA 2.0.0]` --> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
   - Triage outcome: Case B (remediation) + Case A (cross-stream)
   - Links to all created remediation tasks
   - Release Jira references
   - @mention of the issue reporter (using reporter account ID from Jira issue data)
   - Comment Footnote per `shared/comment-footnote.md`

## Blocking Condition

**Triage is currently blocked at Step 7 (Concurrent Triage Detection).** TC-8019 is actively being triaged on the same upstream component (`quinn-proto`) by `engineer-b@example.com`. The engineer must choose one of:

1. **Wait** -- pause until TC-8019's triage completes, then re-run to detect overlap
2. **Skip** -- skip remediation task creation entirely
3. **Proceed** -- create tasks with `concurrent-triage-overlap` label

All remediation actions described above (Steps 7.5, 8, and Post-Triage) are contingent on the engineer choosing Option 1 (after wait) or Option 3.
