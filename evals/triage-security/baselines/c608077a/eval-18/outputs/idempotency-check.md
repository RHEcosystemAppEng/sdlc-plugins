# Idempotency Check: TC-8001 re-run

Every pre-existing triage artifact on TC-8001 was compared against the operation the skill would otherwise
perform. All of them were found and skipped. No operation was re-executed.

| # | Skill operation (step) | Pre-existing artifact detected | Detection evidence | Decision |
|---|---|---|---|---|
| 1 | Assign to current user (Step 0.8.2) | Assignee = engineer-a@example.com | `assignee` field | **Skip** when the current user is engineer-a, the same triager re-running. If a different user re-runs, a reassignment would be proposed and gated by confirmation. It is never silent. |
| 2 | Transition to Assigned (Step 0.8.4) | Status = In Progress, which is later than Assigned | `status` field | **Skip**. The skill skips the transition silently when the status is Assigned or later. |
| 3 | Affects Versions correction (Step 3.2) | Affects Versions = RHTPA 2.2.0, RHTPA 2.2.1, set by the prior run | `versions` field; summary comment says "Affects Versions corrected to RHTPA 2.2.0, RHTPA 2.2.1" | **No re-apply.** This value matches the prior correction, so the same edit and correction comment are not repeated. See the discrepancy note below for RHTPA 2.2.2. |
| 4 | Related links to siblings (Step 4.2) / overlap links (Step 4.3) | None needed. Step 4.3 is skipped because the Upstream Affected Component field is not configured | Config, plus the existing-link check against `issuelinks` | **Skip** (nothing to create). |
| 5 | Preemptive reconciliation (Step 4.4) | Existing Depend tasks TC-8100 and TC-8101 are standard tasks without the `security-preemptive` label | Task labels: ai-generated-jira, Security, CVE-2026-31812 | **Skip**. There is no preemptive label to remove and no link to add. |
| 6 | Concurrent triage (Step 7) / Release dedup (Step 7.5.3) | n/a | Upstream Affected Component field not configured | **Skip**, as the skill prescribes. |
| 7 | Remediation task creation, Case B (Step 8) | TC-8100 (upstream backport to >= 0.11.14 on release/0.4.z [rhtpa-2.2]) and TC-8101 (downstream propagation [rhtpa-2.2]) | Both linked to TC-8001 via **Depend**, both labelled `CVE-2026-31812`, both summaries carry `[rhtpa-2.2]`. This exactly matches the 2-task Cargo pattern for stream 2.2.x | **Skip**. Remediation already exists for stream 2.2.x. Creating tasks again would duplicate TC-8100 and TC-8101. |
| 8 | Description digest comments (remediation-templates / digest protocol) | `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4...a1b2` (2026-07-01T10:00Z) | Comment starting with the marker `[sdlc-workflow] Description digest:` | **Skip**. A digest is posted only immediately after a task is created. No task is created, so no new digest is posted, and the existing digest is not re-posted or altered. |
| 9 | Depend links CVE -> task (Jira Linkage 1) | Depend: TC-8100, Depend: TC-8101 | `issuelinks`, where type.name = "Depend" and outward key matches | **Skip**. The link already exists. |
| 10 | Blocks link upstream -> downstream (Jira Linkage 2) | TC-8101 blocked by TC-8100 | TC-8101 link "Blocks: TC-8100" | **Skip**. The link already exists. |
| 11 | Transition to In Progress (Jira Linkage 5) | Status = In Progress | `status` field | **Skip** ("if not already"). |
| 12 | Task-list comment (Jira Linkage 7) | Covered by the existing post-triage summary ("Remediation tasks created: TC-8100 ..., TC-8101 ...") | Comment history | **Skip**. There are no new tasks to list. |
| 13 | Add `ai-cve-triaged` label (Post-Triage 1) | Label `ai-cve-triaged` is present | `labels` field | **Skip**. Adding it again would be a no-op. |
| 14 | Post-triage summary comment (Post-Triage 2) | "Post-triage summary" comment, AI-generated footnote v0.11.1 (2026-07-01T10:01Z) | Comment history, footnote from sdlc-workflow/triage-security | **Skip**. No new actions were taken in this run, so a second summary would only duplicate the audit trail. |

## Steps that re-run read-only (no artifacts)

- Step 0 config validation, Step 1 extraction and Step 2 version impact are re-evaluated. They are read-only and confirm the issue's current state.
- Step 0.3: the matrix is stale (145 days), so a warning is shown. The interactive matrix refresh is not chosen in this eval and no matrix is written.
- Step 1.5 and Step 5 (MITRE/OSV/lifecycle WebFetch) and the Step 4/4.4 JQL were not executed because this eval allows no external calls. Results are taken from the existing issue state.
- Step 7.5 (release Epic/Task) is not re-run for creation. Remediation for 2.2.x already exists and this run creates no new remediation to link.

## Discrepancies surfaced during re-verification (not auto-applied)

1. **RHTPA 2.2.2 appears affected.** The matrix lists 2.2.2 (build 0.4.9) as a backend retag of v0.4.8. It ships
   quinn-proto 0.11.12, which is below 0.11.14. The prior summary says "RHTPA 2.2.2 and later ship quinn-proto 0.11.14 (not affected)",
   but that contradicts the matrix. Step 3.2 ("correct but incomplete") would *propose*
   `Current: [RHTPA 2.2.0, RHTPA 2.2.1] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
   This is an evidence-driven correction, not a duplicate artifact, and it requires explicit engineer confirmation. It is
   not executed in this run. The matrix is also stale, so the engineer should refresh or verify it before accepting.
   The existing TC-8100 and TC-8101 already fix the 2.2.x stream going forward, so no new task is needed either way.
2. **2.1.x is also affected** (quinn-proto 0.11.9 in v0.3.8 and v0.3.12). TC-8001 is scoped to 2.2.x, so Case A
   applies to 2.1.x: a cross-stream comment or preemptive tasks, unless a sibling CVE Jira exists. The prior summary does not mention it.
   Sibling JQL (Step 4) could not run here, so this is flagged for engineer verification and not mutated.
