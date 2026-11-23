# Idempotency Check: TC-8001 (re-run of triage-security)

Each triage mutation the skill would normally perform is checked against the issue's current state, which came from the Step 1 `get_issue` / remote-links data. If the artifact already exists, the mutation is skipped and the reason is logged.

## Summary

| # | Artifact / mutation | Skill step | Pre-existing evidence | Decision |
|---|---|---|---|---|
| 1 | `ai-cve-triaged` label | Post-Triage Summary §1 | Labels: `CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged` | **SKIP**: label already present; do not add again |
| 2 | Status transition (Assigned / In Progress) | Step 0.8, Step 8 | Status = **In Progress** | **SKIP**: already in a post-triage state; no transition |
| 3 | Assignment to current user | Step 0.8 | Assignee = engineer-a@example.com | **SKIP if current user is engineer-a** (no-op). If a different engineer is running the triage, that person owns the issue, so assignment would be a reassignment, which requires explicit confirmation and is not done automatically |
| 4 | Remediation task: upstream backport (2.2.x) | Step 8 Case B | Depend link to **TC-8100**: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]", labels `ai-generated-jira, Security, CVE-2026-31812`, In Progress | **SKIP**: existing task covers this CVE + stream + library |
| 5 | Remediation task: downstream propagation (2.2.x) | Step 8 Case B | Depend link to **TC-8101**: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]", same labels, Open | **SKIP**: existing task covers this CVE + stream |
| 6 | Depend link CVE to TC-8100 | Step 8 / remediation-templates linkage | `issuelinks` contains `Depend` to TC-8100 | **SKIP**: "Depend link to TC-8100 already exists — skipping" |
| 7 | Depend link CVE to TC-8101 | Step 8 linkage | `issuelinks` contains `Depend` to TC-8101 | **SKIP**: "Depend link to TC-8101 already exists — skipping" |
| 8 | Blocks link TC-8101 to TC-8100 (downstream blocked by upstream) | Step 8 linkage | TC-8101 has `Blocks: TC-8100` | **SKIP**: intra-stream Blocks link already exists |
| 9 | Description digest comment | Remediation Task Creation (`shared/description-digest-protocol.md`) | Comment 1: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4…b2`, posted by sdlc-workflow/triage-security | **SKIP**: digest already recorded. The digest is posted only right after a task is *created*. No task is created in this run, so no digest is posted |
| 10 | Post-triage summary comment | Post-Triage Summary §2 | Comment 2: "Triage complete for CVE-2026-31812 (quinn-proto)…", with Comment Footnote (v0.11.1) | **SKIP**: summary already posted; no duplicate summary |
| 11 | Affects Versions correction + correction comment | Step 3 | Affects Versions = RHTPA 2.2.0, RHTPA 2.2.1 (prior run already corrected them, per the summary) | **No duplicate correction.** The prior correction stands. See the discrepancy note below about RHTPA 2.2.2 |
| 12 | Remote links (GHSA, CVE record, upstream PR) | (read-only) | Present | No action; the skill never writes remote links |

## Per-step notes

- **Step 4.1 / 4.2 (siblings)**: the sibling JQL search cannot run in this eval. Any Related link to a sibling would first check `issuelinks` for an existing `Related` link and skip it if found. No Related links exist on TC-8001 today, so nothing is duplicated.
- **Step 4.3 / 7 / 7.5.3**: skipped. They are gated on the Upstream Affected Component, PS Component, and Stream fields being declared in Security Configuration, and those fields are not declared there.
- **Step 4.4 (preemptive reconciliation)**: TC-8100 and TC-8101 do not carry `security-preemptive`, so there is nothing to reconcile and no label removal.
- **Step 5 (lifecycle)**: 2.2.x is the current, latest stream, so it is assumed supported. A lifecycle close does not apply.
- **Step 6 (already fixed)**: TC-8001 itself has open remediation (TC-8100 In Progress, TC-8101 Open). The fix has not shipped to the affected versions, so no already-fixed close.
- **Step 7.5 (release Jira)**: the prior run did not record a release Epic or Task. The release flow is interactive and per-release-family. Its only purpose here would be to link already-existing remediation tasks, and it would need explicit engineer confirmation to create anything. Nothing is created automatically.
- **Step 8 (remediation)**: Case B applies (2.2.x is affected). For each in-scope stream, the existing-remediation check finds Depend-linked Tasks that match CVE label `CVE-2026-31812`, library `quinn-proto`, and stream `[rhtpa-2.2]`. They also match the expected pair for a Cargo source dependency: upstream backport + downstream propagation. The stream therefore counts as **already remediated** and task creation is skipped. Task count check: 2 existing tasks, and the Cargo classification requires exactly 2.

## Discrepancy found during re-verification (not an idempotency skip)

The lock-file re-verification (Step 2) shows that **RHTPA 2.2.2** is a backend retag of 2.2.1. It ships `v0.4.8`, which contains quinn-proto 0.11.12 (< 0.11.14), so it is **affected**. The current Affects Versions (2.2.0, 2.2.1) and the prior summary ("2.2.2 and later … not affected") both leave it out.

- This is **new evidence**, not a duplicate of a prior artifact. Under the skill's rules ("Do not assume PSIRT Affects Versions are correct"; "Handle retags explicitly"), the run must **present** the proposed change `Current: [RHTPA 2.2.0, RHTPA 2.2.1] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` to the engineer.
- It is **not executed automatically**. Every Jira mutation needs explicit confirmation, so nothing is written unless the engineer approves.
- Existing remediation TC-8100/TC-8101 still covers it. The fix lands on `release/0.4.z`, and 2.2.3+ already ship 0.11.14, so no extra remediation task is needed either way.

## Cross-stream observation (not an idempotency skip)

Stream 2.1.x (2.1.0, 2.1.1) ships quinn-proto 0.11.9 and is also affected. Case A for a scoped issue would require a sibling-CVE search before deciding on a cross-stream comment or preemptive tasks. The prior run's artifacts show no cross-stream comment. In a live re-run, the sibling search would run first. If a 2.1.x companion CVE exists, nothing is needed. Otherwise, the cross-stream comment and preemptive tasks would be proposed to the engineer for confirmation. They are not created automatically in this run.
