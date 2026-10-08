# Idempotency Check -- Re-Run Analysis for TC-8001

This document analyzes every pre-existing triage artifact detected during a
second run of `/sdlc-workflow:triage-security` on TC-8001, and explains why
each step produces no new mutations.

## Summary of Pre-Existing Artifacts

| Artifact | Present? | Evidence |
|----------|----------|----------|
| `ai-cve-triaged` label | YES | Labels include `ai-cve-triaged` |
| Status: In Progress | YES | Issue status is `In Progress` |
| Remediation task TC-8100 (upstream backport) | YES | Depend link exists |
| Remediation task TC-8101 (downstream propagation) | YES | Depend link exists |
| Description digest comment | YES | Comment #1: `sha256-md:a1b2c3...` |
| Post-triage summary comment | YES | Comment #2: triage complete summary |
| Affects Versions corrected | YES | Set to RHTPA 2.2.0, RHTPA 2.2.1 |
| Assignee set | YES | engineer-a@example.com |

## Step-by-Step Idempotency Analysis

### Step 0 -- Validate Project Configuration
- **Detection**: Configuration is valid (Security Configuration section present in CLAUDE.md with Product Lifecycle, Version Streams, Source Repositories).
- **Action**: Proceed. No mutation. This step is read-only.

### Step 0.3 -- Matrix Staleness Check
- **Detection**: `security-matrix-mock.md` has `Last-Updated: 2026-06-28T10:00:00Z`. This is within the 14-day threshold relative to the triage date context.
- **Action**: Proceed without warning. No mutation. Read-only check.

### Step 0.5 -- Jira Access Initialization
- **Detection**: Jira access method resolved (MCP or REST API).
- **Action**: No mutation. Connection setup only.

### Step 0.7 -- Assign and Transition to Assigned
- **Detection**: Issue status is `In Progress`, which is past `Assigned`. The skill's status-aware handling notes: "If the issue is already in Assigned or any later status, skip the transition silently."
- **Action**: Assignment still proceeds (re-assigns to current user), but the transition is SKIPPED because the issue is already past `Assigned` status. Assignment is idempotent -- re-assigning the same user produces no visible change.
- **Mutation**: None (or no-op re-assignment).

### Step 1 -- Data Extraction
- **Detection**: All fields parsed successfully (see data-extraction.md). The issue already has complete metadata from the prior triage.
- **Action**: Read-only data extraction. No mutation.
- **Status-aware handling**: The issue is in `In Progress` status. The skill warns: "This issue is already in In Progress. It may be actively worked on." The engineer must confirm to proceed with re-triage (e.g., to verify version impact or update Affects Versions).

### Step 1.5 -- External CVE Data Enrichment
- **Detection**: External APIs queried for CVE-2026-31812.
- **Action**: Read-only enrichment. No mutation. Cross-validation of fix threshold (0.11.14) against external sources.

### Step 1.7 -- Embargo Check
- **Detection**: CVSS is 7.5 (High, >= 7.0 threshold). However, no Embargo policy URL is configured in the mock CLAUDE.md Security Configuration.
- **Action**: SKIPPED entirely because no Embargo policy URL is configured. No mutation.

### Step 2 -- Version Impact Analysis
- **Detection**: Lock file data analyzed. Version impact table built (identical to prior run).
- **Action**: Read-only analysis. No mutation. The version impact table matches the prior triage results exactly.

### Step 3 -- Affects Versions Correction
- **Detection**: Current Affects Versions are `RHTPA 2.2.0, RHTPA 2.2.1`. Version impact table (scoped to 2.2.x) shows the same versions as affected. **Affects Versions are already correct.**
- **Action**: SKIPPED. "If Affects Versions are already correct: note this and proceed without changes." No mutation.

### Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

#### Step 4.1 -- Same-stream duplicates
- **Detection**: JQL search for sibling Vulnerability issues with label `CVE-2026-31812`. No same-stream duplicates expected (this is the canonical issue for stream 2.2.x).
- **Action**: No duplicates found. No mutation.

#### Step 4.2 -- Cross-stream coordination
- **Detection**: Search for different-stream siblings. Any sibling links already exist from the prior run (if applicable).
- **Action**: Link creation is idempotent -- "Check for existing link before creating one." Existing links are detected and skipped: "Related link to [sibling-key] already exists -- skipping." No mutation.

#### Step 4.3 -- Cross-CVE overlap detection
- **Detection**: Search for Vulnerability issues with same Upstream Affected Component (`quinn-proto`), PS Component (`pscomponent:org/rhtpa-server`), and Stream (`rhtpa-2.2`). Any overlap links and comments from the prior run already exist.
- **Action**: If overlapping CVEs exist, link creation checks for existing links first (idempotent). Comments from prior run already present. No new mutation.

#### Step 4.4 -- Preemptive task reconciliation
- **Detection**: Search for preemptive tasks with label `security-preemptive` and `CVE-2026-31812`. If any were reconciled in the prior run, the `security-preemptive` label was already removed and the Depend link was already created.
- **Action**: No matching preemptive tasks found (already reconciled or never existed). No mutation.

### Step 5 -- Version Lifecycle Check
- **Detection**: Affected versions (RHTPA 2.2.0, RHTPA 2.2.1) checked against product lifecycle page.
- **Action**: Read-only check. Lifecycle status is the same as the prior run. No mutation.

### Step 6 -- Already Fixed Check
- **Detection**: Cross-reference resolved siblings. No resolved siblings that change the outcome.
- **Action**: Read-only check. No mutation.

### Step 7 -- Concurrent Triage Detection
- **Detection**: Search for in-progress triages on the same upstream component (`quinn-proto`). The current issue itself is `In Progress`, but it is excluded by `key != TC-8001`.
- **Action**: No concurrent triages detected (or same results as prior run). No mutation.

### Step 7.5 -- Release Jira Orchestration
- **Detection**: Search for release Epic and release Task for stream 2.2.x. If created in the prior run, they already exist.
- **Action**: "If an existing release Epic is found, use this Epic." "If a release Task exists, use it." Find-or-create is idempotent. No new creation.

#### Step 7.5.3 -- Cross-CVE dedup check
- **Detection**: Inspect release Task's issue links for existing remediation Tasks covering `quinn-proto`. TC-8100 and TC-8101 are already linked.
- **Action**: Existing coverage detected. No new mutation.

### Step 8 -- Remediation (Case B)
- **Detection**: Two remediation tasks already exist:
  - TC-8100: upstream backport (Depend link to TC-8001, status In Progress)
  - TC-8101: downstream propagation (Depend link to TC-8001, Blocks TC-8100, status Open)
- **Action**: The existing Depend links from TC-8001 to TC-8100 and TC-8101 are already present. Creating duplicate tasks would be incorrect. The skill detects that remediation tasks already exist for this CVE/stream combination through the issue's existing `issuelinks` array (fetched in Step 1). **No new remediation tasks created.**
- **Mutation**: None. The correct task count (2 for Cargo ecosystem) already exists.

### Case A -- Cross-stream impact
- **Detection**: Issue is scoped to 2.2.x. Other streams (2.1.x) may also be affected (quinn-proto 0.11.9 in both 2.1.0 and 2.1.1). However, any cross-stream comments and preemptive tasks from the prior run already exist.
- **Action**: Cross-stream impact comment already posted (if applicable). Preemptive tasks already created (if applicable). No new mutation.

### Post-Triage Summary
- **Detection**: The `ai-cve-triaged` label is already present on the issue. The post-triage summary comment already exists (Comment #2).
- **Label**: `ai-cve-triaged` already in labels array. Adding it again is a no-op (label sets are idempotent in Jira).
- **Summary comment**: A post-triage summary comment already exists from the prior run. Posting a duplicate summary would create noise. The skill should detect the existing summary and skip posting a new one.
- **Mutation**: None. Both the label and summary comment are already present.

## Idempotency Mechanisms

The triage-security skill achieves idempotency through several mechanisms:

1. **Label-based triage marker**: The `ai-cve-triaged` label signals that triage has been completed. Discovery mode filters these out of the untriaged list.

2. **Status-aware handling**: The issue is in `In Progress` status, triggering a warning that the issue is already being worked on. The engineer must explicitly confirm to proceed with re-triage.

3. **Link existence checks**: Before creating any Jira link (Related, Depend, Blocks), the skill checks the existing `issuelinks` array for a matching link. If found, it skips creation with a log message.

4. **Affects Versions comparison**: Step 3 compares current vs proposed Affects Versions. If they already match, no update is performed.

5. **Existing remediation detection**: The issue's `issuelinks` already contain Depend links to TC-8100 and TC-8101. The skill can detect that remediation tasks exist for this CVE/stream combination and skip creation.

6. **Release Jira find-or-create pattern**: Step 7.5 searches before creating, reusing existing Epics and Tasks.

7. **Comment deduplication**: The description digest comment and post-triage summary comment already exist, preventing duplicate postings.
