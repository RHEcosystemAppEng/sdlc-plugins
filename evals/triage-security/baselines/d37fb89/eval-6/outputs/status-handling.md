# Status-Aware Handling Decisions

Each issue from the discovery listing is evaluated according to the status-aware handling rules defined in the triage-security skill. The handling decision depends on the issue's current Jira status.

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]

- **Status**: New
- **Handling**: Proceed with full triage (Steps 1-7). This is the default path for New issues.
- **Stream scope**: Scoped to stream **2.2.x** (suffix `[rhtpa-2.2]` maps to configured Version Stream 2.2.x).
- **Component**: `pscomponent:org/rhtpa-server`
- **Notes**: No special handling required. Standard triage workflow applies.

### TC-9002 -- CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]

- **Status**: New
- **Handling**: Proceed with full triage (Steps 1-7). This is the default path for New issues.
- **Stream scope**: Scoped to stream **2.1.x** (suffix `[rhtpa-2.1]` maps to configured Version Stream 2.1.x).
- **Component**: `pscomponent:org/rhtpa-server`
- **Notes**: No special handling required. Standard triage workflow applies.

### TC-9003 -- CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]

- **Status**: In Progress
- **Handling**: **Warning required.** This issue is already in `In Progress` status. It may be actively worked on. Before proceeding, the engineer must be warned:

  > "This issue is already in `In Progress`. It may be actively worked on."

  The engineer is asked whether to:
  1. **Proceed with triage anyway** -- e.g., to verify version impact or update Affects Versions
  2. **Skip this issue**

  If the engineer chooses to skip, return to the discovery list or end the session. If proceeding, run the full triage workflow (Steps 1-7) but exercise caution around Jira mutations that might conflict with active work.

- **Stream scope**: Scoped to stream **2.2.x** (suffix `[rhtpa-2.2]` maps to configured Version Stream 2.2.x).
- **Component**: `pscomponent:org/rhtpa-server`

### TC-9004 -- CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]

- **Status**: New
- **Handling**: Proceed with full triage (Steps 1-7). This is the default path for New issues.
- **Stream scope**: Scoped to stream **2.2.x** (suffix `[rhtpa-2.2]` maps to configured Version Stream 2.2.x).
- **Component**: `pscomponent:org/rhtpa-server`
- **Notes**: No special handling required. Standard triage workflow applies.

---

## Triaged but still New Issues (Query 2)

### TC-9010 -- CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]

- **Status**: New (with `ai-cve-triaged` label)
- **Handling**: This issue was previously triaged but has not moved beyond New status. It appears in the "Triaged but still New" query specifically to flag stale issues. The engineer should decide whether to:
  1. **Re-triage** -- run the full triage workflow again to verify previous findings, check for new upstream fixes, or update version impact analysis
  2. **Follow up on existing remediation** -- check if remediation tasks were created during the prior triage and investigate why they have not progressed
  3. **Skip** -- the issue may be intentionally deferred

  Since the status is New, if the engineer chooses to re-triage, the full triage workflow (Steps 1-7) applies as the default path. The existing `ai-cve-triaged` label indicates prior triage was completed, so the engineer should review the issue's comment history for the previous triage summary before deciding.

- **Stream scope**: Scoped to stream **2.2.x** (suffix `[rhtpa-2.2]` maps to configured Version Stream 2.2.x).
- **Component**: `pscomponent:org/rhtpa-server`

---

## Summary of Handling Decisions

| Key | Status | Handling Decision | Action Required |
|-----|--------|-------------------|-----------------|
| TC-9001 | New | Full triage | None -- proceed directly |
| TC-9002 | New | Full triage | None -- proceed directly |
| TC-9003 | In Progress | Warning + engineer choice | Warn: "already in In Progress"; ask proceed or skip |
| TC-9004 | New | Full triage | None -- proceed directly |
| TC-9010 | New (triaged) | Re-triage or follow-up | Review prior triage history; decide re-triage vs. follow-up |

## Configuration Context

The following Security Configuration fields were used for this analysis:

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Component label pattern**: `pscomponent:`
- **VEX Justification custom field**: customfield_12345 (configured -- available for close operations)
- **Upstream Affected Component custom field**: Not configured (Step 4.3 cross-CVE overlap detection would be skipped)
- **PS Component custom field**: Not configured
- **Stream custom field**: Not configured
- **Version Streams**: 2.1.x, 2.2.x
