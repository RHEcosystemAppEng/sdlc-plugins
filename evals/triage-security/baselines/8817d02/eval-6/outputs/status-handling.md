# Status-Aware Handling Decisions

Per SKILL.md "Status-aware handling" rules, each discovered issue requires a handling decision based on its current Jira status before triage can proceed. Below is the status-aware analysis for every issue found in the discovery queries.

---

## Query 1: Untriaged Issues

### TC-9001 -- CVE-2026-40112 h2 (HTTP/2 rapid reset vulnerability)

- **Status**: New
- **Stream**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Labels**: CVE-2026-40112, pscomponent:org/rhtpa-server
- **Handling Decision**: **Proceed with full triage (default path)**
- **Rationale**: Status is "New" -- this is the standard entry point for untriaged issues. No warnings or confirmations needed. Full 7-step triage applies: data extraction, version impact analysis across streams 2.1.x and 2.2.x (scoped to 2.2.x for Affects Versions correction), duplicate/sibling check, lifecycle check, already-fixed check, and remediation.

### TC-9002 -- CVE-2026-40297 serde_json (Stack overflow on deeply nested input)

- **Status**: New
- **Stream**: 2.1.x (from summary suffix `[rhtpa-2.1]`)
- **Labels**: CVE-2026-40297, pscomponent:org/rhtpa-server
- **Handling Decision**: **Proceed with full triage (default path)**
- **Rationale**: Status is "New" -- standard untriaged issue. Full 7-step triage applies. Note this is scoped to stream 2.1.x, so Affects Versions correction in Step 3 will only propose versions belonging to stream 2.1.x. Cross-stream impact on 2.2.x will be evaluated in Step 7 Case B.

### TC-9003 -- CVE-2026-40455 tokio (Race condition in task cancellation)

- **Status**: In Progress
- **Stream**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Labels**: CVE-2026-40455, pscomponent:org/rhtpa-server
- **Handling Decision**: **Warn the user before proceeding**
- **Warning message**: "This issue is already in `In Progress`. It may be actively worked on."
- **Options to present to the engineer**:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Rationale**: Per the skill's status-aware handling rules, issues in "In Progress" status require a warning because someone may already be working on remediation. The engineer must explicitly choose whether to proceed or skip. If they proceed, the full triage runs but should be careful not to duplicate existing remediation work -- Step 4 (duplicate/sibling check) and Step 6 (already-fixed check) are especially important for this issue.

### TC-9004 -- CVE-2026-40518 ring (Timing side-channel in RSA verification)

- **Status**: New
- **Stream**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Labels**: CVE-2026-40518, pscomponent:org/rhtpa-server
- **Handling Decision**: **Proceed with full triage (default path)**
- **Rationale**: Status is "New" -- standard untriaged issue. Full 7-step triage applies. Scoped to stream 2.2.x. Cross-stream impact on 2.1.x will be evaluated in Step 7 Case B.

---

## Query 2: Triaged but still New (stale issues)

### TC-9010 -- CVE-2026-39874 quinn-proto (Panic on malformed QUIC frame)

- **Status**: New
- **Stream**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Labels**: CVE-2026-39874, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Handling Decision**: **Flag as stale -- recommend re-triage or follow-up**
- **Rationale**: This issue has the `ai-cve-triaged` label (indicating it was previously triaged by this skill) but remains in "New" status. It was created on 2026-05-28, which is 26 days ago. The fact that it has not moved to "In Progress" or "Closed" after triage suggests one of:
  1. The remediation tasks created during triage have not been picked up
  2. The triage concluded with a close recommendation that was not executed
  3. The triage was interrupted before completion
- **Recommended follow-up actions**:
  - Check the issue's comments for the post-triage summary to understand the previous triage outcome
  - Check if remediation tasks were created and their current status
  - If remediation tasks exist but are stalled, escalate to the team
  - If no remediation tasks exist, consider re-triaging (the engineer can select this issue for a fresh triage run)
- **Status-aware handling**: Since the status is "New", the standard triage path would apply if the engineer selects this issue. However, because it already has the `ai-cve-triaged` label, the skill should note this and ask the engineer whether to re-triage or skip.

---

## Handling Decision Summary

| Issue Key | Status | Stream | Handling Decision | Action Required |
|-----------|--------|--------|-------------------|-----------------|
| TC-9001 | New | 2.2.x | Proceed with full triage | None -- ready for triage |
| TC-9002 | New | 2.1.x | Proceed with full triage | None -- ready for triage |
| TC-9003 | In Progress | 2.2.x | Warn user, ask to proceed or skip | Engineer confirmation required |
| TC-9004 | New | 2.2.x | Proceed with full triage | None -- ready for triage |
| TC-9010 | New (stale) | 2.2.x | Flag as stale, recommend re-triage | Engineer decision on re-triage |

### Priority Recommendation

Based on status, stream distribution, and CVE severity context, a suggested triage order would be:

1. **TC-9001** (CVE-2026-40112, h2 rapid reset) -- New, 2.2.x. HTTP/2 rapid reset vulnerabilities are typically high severity and affect network-facing services.
2. **TC-9004** (CVE-2026-40518, ring timing side-channel) -- New, 2.2.x. Cryptographic timing side-channels in RSA verification can compromise authentication.
3. **TC-9002** (CVE-2026-40297, serde_json stack overflow) -- New, 2.1.x. Stack overflow on nested input is a denial-of-service vector.
4. **TC-9003** (CVE-2026-40455, tokio race condition) -- In Progress, 2.2.x. Already being worked on; triage may only be needed for verification.
5. **TC-9010** (CVE-2026-39874, quinn-proto panic) -- Stale, 2.2.x. Previously triaged; needs follow-up rather than fresh triage.

The engineer should select an issue from the discovery list to begin triage, or provide an issue key directly.
