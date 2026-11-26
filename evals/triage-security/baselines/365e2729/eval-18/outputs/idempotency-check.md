# Idempotency Check: TC-8001 Re-run

Before proposing each mutation, the skill checks whether the issue (as read in Step 1) already
has the resulting artifact. This table covers every artifact that a full Case B triage of a
scoped Cargo CVE would produce.

| # | Triage artifact | Producing step | Pre-existing evidence on TC-8001 | Decision |
|---|-----------------|----------------|----------------------------------|----------|
| 1 | `ai-cve-triaged` label | Post-Triage Summary §1 | Label already present in `labels` | **SKIP.** Re-adding would be a no-op label write. |
| 2 | Transition to Assigned | Step 0.8 | Status is `In Progress`, which is later than Assigned | **SKIP.** "If the issue is already in Assigned or any later status … skip the transition silently." |
| 3 | Transition to In Progress | Remediation outcome | Already `In Progress` (the prior summary records "Transitioned to In Progress") | **SKIP** |
| 4 | Assignment to current user | Step 0.8 | Assignee is `engineer-a@example.com` | **SKIP if the current user is engineer-a** (no change). If a different engineer runs the re-run, interactive Step 0.8 would propose reassignment, which needs explicit confirmation because someone else owns an In Progress issue. That case is outside the "no mutation" scenario. |
| 5 | Upstream backport remediation Task | Step 8 Case B | TC-8100 "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]", labels `ai-generated-jira, Security, CVE-2026-31812`, In Progress | **SKIP creation.** Remediation already exists for the 2.2.x stream. Creating another would duplicate work in progress. |
| 6 | Downstream propagation remediation Task | Step 8 Case B | TC-8101 "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]", same labels, Open | **SKIP creation** |
| 7 | Depend link TC-8001 → TC-8100 | Step 8 linkage | `issuelinks` contains Depend / TC-8100 | **SKIP.** Matched on `type.name == "Depend"` and linked key, the same check used in Steps 4.2 and 4.3. |
| 8 | Depend link TC-8001 → TC-8101 | Step 8 linkage | `issuelinks` contains Depend / TC-8101 | **SKIP** |
| 9 | Blocks link between TC-8100 and TC-8101 | Step 8 linkage (upstream → downstream) | TC-8101 records `Blocks: TC-8100` | **SKIP.** The link exists. (Its recorded direction reads as TC-8101 blocks TC-8100, which is the reverse of the template's upstream → downstream convention. This is flagged for the engineer to check, and the skill does not change it automatically.) |
| 10 | Description digest comment | Remediation Task Creation (`shared/description-digest-protocol.md`) | `[sdlc-workflow] Description digest: sha256-md:a1b2c3…a1b2` from triage-security, 2026-07-01T10:00:00Z | **SKIP.** Digests are posted only right after a task is created, and this run creates no task, so there is nothing to digest. The existing digest stays as `/implement-task`'s integrity anchor. Re-posting would add a second digest and make "most recent digest" selection ambiguous. |
| 11 | Post-triage summary comment | Post-Triage Summary §2 | Summary from triage-security v0.11.1 with footnote, 2026-07-01T10:01:00Z, covering version impact, AV correction, label, TC-8100/TC-8101, and the transition | **SKIP.** Nothing new to report would just repeat the existing audit trail. |
| 12 | Affects Versions correction + comment | Step 3 | Field = RHTPA 2.2.0, RHTPA 2.2.1. The prior summary says it was corrected. | **Already corrected by the prior run, so no duplicate correction comment.** One discrepancy remains (see below). |
| 13 | Cross-stream impact comment (Case A) | Step 8 Case A | The 2.1.x stream (2.1.0, 2.1.1 → quinn-proto 0.11.9) is also affected. No cross-stream comment or Related link exists in the issue data. | **Not posted automatically.** Step 4 sibling search (a JQL query) cannot run in this eval. If a 2.1.x sibling CVE Jira exists, Case A skips preemptive tasks for it. If none exists, a live run would propose the cross-stream comment plus preemptive 2.1.x tasks, gated on confirmation. Not created here because sibling evidence is unavailable. |
| 14 | Related links to siblings / preemptive reconciliation | Steps 4.2 / 4.4 | No sibling or preemptive evidence supplied | **No action** (no trusted match) |
| 15 | Cross-CVE overlap (4.3), concurrent triage (7) | Steps 4.3 / 7 | Upstream Affected Component field is not configured in Security Configuration | **Skipped** by configuration |
| 16 | Release Jira linking | Step 7.5 | No release Epic or Task evidence. Existing tasks have no release Blocks link. | **No creation.** Step 7.5 needs individual confirmation and a stream-to-version decision. Remediation already exists, so nothing new needs a release container. The engineer can link it manually. |

## Discrepancy found during re-verification (not an idempotency artifact)

The re-run recomputed version impact from the pinned-commit evidence. The result **contradicts the
prior triage for RHTPA 2.2.2**:

- In the security matrix, 2.2.2 (build 0.4.9) is pinned to backend tag `v0.4.8` ("backend retag of 2.2.1"). The lock-file data marks `v0.4.9` as a retag of `v0.4.8`.
- `v0.4.8` ships quinn-proto **0.11.12**, which is < 0.11.14, so **2.2.2 is affected** (Important Rule 5: carry forward the retag result).
- The prior summary says "RHTPA 2.2.2 and later ship quinn-proto 0.11.14 (not affected)", and Affects Versions omits RHTPA 2.2.2.

Step 3 therefore yields a **proposal**, not an automatic write:
`Current: [RHTPA 2.2.0, RHTPA 2.2.1] → Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`.
Per Guardrails and Important Rule 11, this goes to the engineer for explicit confirmation. Nothing
was written in this run. Existing tasks TC-8100 and TC-8101 already target the 2.2.x stream and
release/0.4.z, so no new remediation task is needed either way.

Also noted for the engineer, with no action: v0.4.11 on `release/0.4.z` already ships 0.11.14. That
suggests the upstream fix is already on the branch (Step 2.5 "fix available"). If so, TC-8100's
"upstream backport" may in practice be a dependency bump. The existing in-progress task is left as is.
