# Triage Outcome: TC-8001 (Re-Run -- No New Mutations)

## Outcome

**The second run of `triage-security` on TC-8001 produces zero new Jira mutations.**

All triage artifacts created by the prior run are detected during re-execution, and every mutation step is skipped. The skill is idempotent: re-running it on a fully triaged issue results in the same final state with no side effects.

## Why No Mutations Are Produced

### 1. The issue is already past the initial triage entry point

The issue's current status is **In Progress** (not New). Per the skill's status-aware handling (SKILL.md, "Status-aware handling" section), when an issue is in In Progress status, the skill warns the user that the issue may be actively worked on and asks whether to proceed or skip. If the user proceeds, the skill executes the triage steps but each step detects existing artifacts and produces no mutations.

Step 0.7 (Assign and Transition) skips the Assigned transition because the issue is already past Assigned status. The assignment update is a no-op because the issue is already assigned.

### 2. The `ai-cve-triaged` label signals completed triage

The presence of the `ai-cve-triaged` label on the issue is the primary marker that triage has been completed. This label is added as the final step of the triage workflow (Post-Triage Summary, item 1). During the re-run:

- The Post-Triage Summary step detects that the label already exists and does not attempt to add it again.
- In discovery mode, this label would exclude the issue from the "untriaged" JQL query (`labels NOT IN (ai-cve-triaged)`), so TC-8001 would not even appear as a candidate for triage.

### 3. Remediation tasks already exist and are linked

The two remediation tasks created by the prior run (TC-8100 for upstream backport, TC-8101 for downstream propagation) are visible in the issue's `issuelinks` array:

- **TC-8100** -- linked via Depend, summary matches the upstream backport template for quinn-proto on the rhtpa-2.2 stream, carries the `CVE-2026-31812` and `ai-generated-jira` labels.
- **TC-8101** -- linked via Depend, summary matches the downstream propagation template, carries the same labels, and is blocked by TC-8100.

When Step 8 (Remediation) evaluates whether to create tasks, it finds that remediation tasks for this CVE and stream already exist. The existing Depend links from TC-8001 to both tasks confirm they are properly linked. The skill does not create duplicate tasks.

### 4. Affects Versions are already correct

The current Affects Versions on the issue (RHTPA 2.2.0, RHTPA 2.2.1) match the expected values from the version impact analysis:

- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- affected (< 0.11.14)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- affected (< 0.11.14)
- RHTPA 2.2.2 (v0.4.9): retag of 2.2.1 -- affected but 2.2.2 may not have a registered Jira version
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- not affected (fixed)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- not affected (fixed)

Since the issue is scoped to the 2.2.x stream, only RHTPA 2.2.0 and RHTPA 2.2.1 should be in Affects Versions (versions actually shipping the vulnerable dependency). This matches the current state. Step 3 detects no correction is needed and skips the `edit_issue` call.

### 5. Post-triage summary and digest comments already exist

The issue's comment history contains both the description digest comment and the post-triage summary comment, both posted by `sdlc-workflow/triage-security` during the prior run. The re-run detects these by their content patterns:

- Description digest: identified by the `[sdlc-workflow] Description digest:` prefix
- Post-triage summary: identified by content pattern ("Triage complete for CVE-2026-31812") and author attribution

Neither comment is re-posted.

### 6. All issue links are already present

Every link that the skill would create during triage already exists on the issue:

| Link | Type | From | To | Present? |
|------|------|------|----|----------|
| Remediation link | Depend | TC-8001 | TC-8100 | Yes |
| Remediation link | Depend | TC-8001 | TC-8101 | Yes |
| Blocking link | Blocks | TC-8100 | TC-8101 | Yes |

The skill's idempotent link-creation pattern (check `issuelinks` array before calling `create_link`) prevents duplicate link creation.

## Idempotency Mechanism

The triage-security skill achieves idempotency through multiple detection mechanisms at each step:

1. **Label check** (`ai-cve-triaged`) -- guards against re-processing in discovery mode
2. **Status check** (In Progress) -- triggers a user warning and optional skip
3. **Link inspection** -- before creating any issue link, the skill checks the existing `issuelinks` array for a matching link type and target key
4. **Comment pattern matching** -- before posting comments, the skill checks for existing comments with matching content patterns
5. **Field comparison** -- before editing fields (Affects Versions), the skill compares current values against proposed values and skips if they match
6. **Task existence check** -- before creating remediation tasks, the skill checks for existing linked tasks with matching CVE label and stream scope

These checks ensure that running the skill multiple times on the same issue converges to the same final state without producing duplicate artifacts or spurious Jira notifications.
