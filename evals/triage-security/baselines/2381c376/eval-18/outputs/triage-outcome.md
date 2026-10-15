# Triage Outcome -- Re-run of TC-8001 Produces No New Mutations

## Outcome: No-op (all triage artifacts already present)

A second invocation of triage-security on TC-8001 (CVE-2026-31812, quinn-proto)
produces **zero new Jira mutations**. Every artifact created by the prior triage
run is detected during the re-run and its corresponding write is skipped.

## Why the Second Run Produces No New Mutations

### 1. The issue is already fully triaged

The prior run completed the entire triage workflow successfully. The
`ai-cve-triaged` label on TC-8001 is the top-level marker that signals
"this issue has already been through the triage-security workflow." While
the label alone does not block re-entry (the skill allows re-triage for
verification), every downstream step also has its own idempotency guard.

### 2. Each step has independent idempotency

The triage-security skill is designed so that each step checks for existing
artifacts before proposing mutations:

- **Step 0.8 (Assign/Transition)**: The issue is already `In Progress`, which
  is past the `Assigned` target status. The skill detects this and skips the
  transition. Assignment is already set.

- **Step 3 (Affects Versions Correction)**: The current Affects Versions
  (`RHTPA 2.2.0, RHTPA 2.2.1`) already matches what the version impact analysis
  would produce for the 2.2.x stream. No correction is needed, so no correction
  comment is posted.

- **Step 4 (Duplicate/Sibling/Overlap Check)**: Existing issue links are
  checked before creating new ones (the skill reads `issuelinks` from Step 1
  and checks for matching `type.name` and key before proposing a link). All
  relevant links already exist.

- **Step 8 (Remediation)**: The two remediation tasks (TC-8100 upstream
  backport, TC-8101 downstream propagation) are already linked to TC-8001 via
  Depend links. The skill detects these existing remediation tasks and skips
  task creation for the 2.2.x stream. No duplicate tasks are created.

- **Post-Triage Summary**: The `ai-cve-triaged` label is already present (no
  label add needed). The post-triage summary comment already exists (no
  duplicate comment posted). The issue is already `In Progress` (no transition
  needed).

### 3. Read-only steps still execute

The re-run does perform all read-only analysis steps (data extraction, version
impact analysis, external CVE enrichment, lifecycle checks). These steps produce
no Jira mutations -- they gather and validate data. The re-run confirms:

- The version impact table is unchanged (RHTPA 2.2.0 and 2.2.1 remain affected;
  2.2.3+ remain unaffected)
- The Affects Versions are still correct
- The existing remediation tasks still cover the required scope
- No new sibling or duplicate issues have appeared

### 4. No proposed actions

Because every mutation target already has a matching pre-existing artifact, the
re-run would produce the following proposed action list:

| Proposed Action | Pre-existing Artifact | Result |
|----------------|----------------------|--------|
| Assign to current user | Assignee already set | SKIPPED |
| Transition to Assigned | Status is In Progress (past Assigned) | SKIPPED |
| Correct Affects Versions | Already RHTPA 2.2.0, RHTPA 2.2.1 | SKIPPED |
| Post Affects Versions correction comment | Correction not needed | SKIPPED |
| Create upstream backport task | TC-8100 exists with Depend link | SKIPPED |
| Create downstream propagation task | TC-8101 exists with Depend link | SKIPPED |
| Link upstream task to CVE (Depend) | TC-8001 -> TC-8100 link exists | SKIPPED |
| Link downstream task to CVE (Depend) | TC-8001 -> TC-8101 link exists | SKIPPED |
| Link downstream blocked by upstream (Blocks) | TC-8101 -> TC-8100 link exists | SKIPPED |
| Post description digest comment | Digest comment already present | SKIPPED |
| Add ai-cve-triaged label | Label already present | SKIPPED |
| Post post-triage summary comment | Summary comment already present | SKIPPED |
| Transition to In Progress | Already In Progress | SKIPPED |

**Total proposed mutations: 0**

## Design Rationale

The triage-security skill achieves idempotency through artifact detection at
each step rather than through a single "already triaged" gate. This design
supports partial re-runs (where a prior triage failed partway through) by
allowing completed steps to be skipped while incomplete steps proceed. In
the case of TC-8001, the prior triage completed fully, so every step finds
its artifact and every mutation is skipped.

This is consistent with the skill's guardrail that "every Jira mutation
requires explicit confirmation" -- on a re-run, no confirmations are needed
because no mutations are proposed. The re-run serves as a verification pass
that confirms the issue's triage state is complete and consistent.
