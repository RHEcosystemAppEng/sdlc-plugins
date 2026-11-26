# Steps 4–8 – Triage Outcome and Post-Triage Summary: TC-8001

## Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check

- Sibling JQL (not executed in this eval): `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8001`.
- No sibling data was provided, so the result is no same-stream duplicate and no 2.1.x companion issue found. Before creating preemptive tasks, the engineer must re-run this JQL against Jira.
- 4.3 Cross-CVE overlap: **skipped**, because the Upstream Affected Component, PS Component, and Stream custom fields are not configured.
- 4.4 Preemptive reconciliation: no existing `security-preemptive` task for CVE-2026-31812 / rhtpa-2.2 was provided, so there is nothing to reconcile.

## Step 5 – Version Lifecycle Check

The product pages URL (https://access.example.com/product-life-cycle/rhtpa) was not fetched in this eval. All affected versions (2.1.x and 2.2.x) are treated as supported because both streams are listed in the configured Version Streams. This needs verification before closure decisions.

## Step 6 – Already Fixed Check

No resolved siblings were found. Within this issue's own stream, the lock file evidence shows the fix has **already shipped in 2.2.3** (backend v0.4.11, quinn-proto 0.11.14) and remains in 2.2.4.

## Step 7 – Concurrent Triage Detection

Skipped, because the Upstream Affected Component custom field is not configured.

## Step 7.5 – Release Jira Orchestration

- 2.2.x: no new non-preemptive remediation tasks are needed (see below), so no release Epic or Task is required.
- 2.1.x: only preemptive tasks are proposed. Preemptive tasks are not linked to release Jira.
- 7.5.3 dedup: skipped because the Upstream Affected Component field is not configured.

## Step 8 – Remediation Decision

**In-scope stream 2.2.x (Case B evaluation):** 2.2.0, 2.2.1, and 2.2.2 are affected. However, the upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (tags v0.4.11 and v0.4.12), and the fix has already been propagated and released in RHTPA 2.2.3 and 2.2.4. **Recommendation:** do not create new 2.2.x dependency-bump or downstream-propagation tasks, because they would duplicate work that has already shipped. The remediation for 2.2.x is "fixed in RHTPA 2.2.3". Customers on 2.2.0 to 2.2.2 should upgrade to 2.2.3 or later. If the engineer still wants tracking tasks, use the dependency-bump variant, since the fix is available upstream.

**Out-of-scope stream 2.1.x (Case A: cross-stream impact):** 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, so they are affected. No 2.1.x companion CVE Jira was found. Proposed preemptive tasks for the Cargo source dependency, where the fix is not available upstream on `release/0.3.z`:

| # | Summary | Labels | Link |
|---|---------|--------|------|
| 1 | Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.1) | ai-generated-jira, CVE-2026-31812, security-preemptive | Related → TC-8001 |
| 2 | Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1) | ai-generated-jira, CVE-2026-31812, security-preemptive | Related → TC-8001; Task 1 Blocks Task 2 |

Coordination guidance: rhtpa-backend has `upstream` deployment context (the default). Submit the bump PR to `release/0.3.z` upstream first, then update the backend tag in `artifacts.lock.yaml` in `rhtpa-release.0.3.z`.

Pre-creation checklist:
- Task count: 2 for 2.1.x (Cargo, source dependency). 0 new for 2.2.x, because the fix is already shipped.
- Cross-stream coverage: 2.1.x is covered by the preemptive tasks.
- Link types: Related (preemptive → TC-8001), Blocks (upstream → downstream).
- Preemptive labels: present.
- Release Jira linking: N/A, because there are no non-preemptive tasks.
- Dedup: N/A.

Every mutation above (Affects Versions edit, preemptive task creation, links, comments, and the `ai-cve-triaged` label) requires engineer confirmation. In this eval they are written here and not executed.

## Post-Triage Summary

1. Add label `ai-cve-triaged` to TC-8001.
2. Post the summary comment below on TC-8001.

### Summary Comment (to be posted on TC-8001)

**Plain-text rendering:**

> **Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14, fixed in 0.11.14)**
>
> **Version impact** (backend `Cargo.lock` at pinned commits from security-matrix.md):
>
> | Version | quinn-proto | Affected? | Notes |
> |---------|-------------|-----------|-------|
> | 2.1.0 | 0.11.9 | YES | stream 2.1.x (out of scope) |
> | 2.1.1 | 0.11.9 | YES | stream 2.1.x (out of scope) |
> | 2.2.0 | 0.11.9 | YES | |
> | 2.2.1 | 0.11.12 | YES | |
> | 2.2.2 | — | YES | same as 2.2.1 (retag) |
> | 2.2.3 | 0.11.14 | NO | fix shipped |
> | 2.2.4 | 0.11.14 | NO | |
>
> **Affects Versions correction:** [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] (scoped to stream 2.2.x per `[rhtpa-2.2]`).
>
> **Outcome:** Affected. For stream 2.2.x, the fix is already shipped in RHTPA 2.2.3 (backend v0.4.11 bumped quinn-proto to 0.11.14). No new 2.2.x remediation tasks were created. Affected 2.2.0 to 2.2.2 users should upgrade to 2.2.3 or later.
>
> **Cross-stream impact:** quinn-proto < 0.11.14 also affects stream 2.1.x (2.1.0, 2.1.1) based on lock file analysis. No 2.1.x companion issue exists, so preemptive remediation tasks were created:
> - 2.1.x upstream backport: `<preemptive-task-1-key>` (security-preemptive), Related to TC-8001
> - 2.1.x downstream propagation: `<preemptive-task-2-key>` (security-preemptive), blocked by `<preemptive-task-1-key>`
>
> **Release Jira:** none (no non-preemptive remediation tasks).
> **Dedup:** none (Upstream Affected Component field not configured).
>
> @psirt-analyst FYI: triage complete for this issue.
>
> ---
> This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.

**ADF body:**

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Triage summary for CVE-2026-31812 (quinn-proto < 0.11.14, fixed in 0.11.14)", "marks": [ { "type": "strong" } ] }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Version impact (backend Cargo.lock at pinned commits): 2.1.0 0.11.9 YES (2.1.x, out of scope); 2.1.1 0.11.9 YES (2.1.x, out of scope); 2.2.0 0.11.9 YES; 2.2.1 0.11.12 YES; 2.2.2 YES (same as 2.2.1, retag); 2.2.3 0.11.14 NO (fix shipped); 2.2.4 0.11.14 NO." }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Affects Versions correction: [RHTPA 2.0.0] → [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] (scoped to stream 2.2.x)." }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Outcome: Affected. For stream 2.2.x, the fix is already shipped in RHTPA 2.2.3 (quinn-proto 0.11.14). No new 2.2.x remediation tasks were created. Affected 2.2.0 to 2.2.2 users should upgrade to 2.2.3 or later." }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Cross-stream impact: stream 2.1.x (2.1.0, 2.1.1) is also affected. Preemptive remediation tasks: <preemptive-task-1-key> (upstream backport, security-preemptive) and <preemptive-task-2-key> (downstream propagation, security-preemptive), both Related to TC-8001. Release Jira: none. Dedup: none." }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "mention", "attrs": { "id": "557058:psirt-analyst-mock-id", "text": "@psirt-analyst" } },
        { "type": "text", "text": " FYI: triage complete for this issue." }
      ]
    },
    { "type": "rule" },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "This comment was AI-generated by " },
        { "type": "text", "text": "sdlc-workflow/triage-security", "marks": [ { "type": "link", "attrs": { "href": "https://github.com/RHEcosystemAppEng/sdlc-plugins" } } ] },
        { "type": "text", "text": " v0.14.0." }
      ]
    }
  ]
}
```
