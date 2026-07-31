# Unsupported Ecosystem Notification

## Ecosystem Detection Result

The ecosystem detection in Step 1 resolved to **Go modules** based on the vulnerable
library and component context. However, Go modules is not present in the Ecosystem
Mappings tables of any configured version stream.

Configured ecosystems in the security matrix:

| Stream | Ecosystems |
|--------|------------|
| 2.1.x  | Cargo, RPM |
| 2.2.x  | Cargo, RPM |

## Notification Presented to User

> **Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required.

This notification follows the skill's template pattern from SKILL.md Step 1 Ecosystem
detection, where the detected ecosystem name (Go modules) is substituted into the
`<ecosystem>` placeholder:

Template: `"**Unsupported ecosystem**: <ecosystem> is not yet supported for automated triage. Manual assessment is required."`

Rendered: `"**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required."`

## Triage Halted

Automated triage **stops** after this notification. The following steps are NOT
performed for the unsupported ecosystem:

- Step 1.5 (External CVE Data Enrichment) — skipped
- Step 1.7 (Embargo Check) — skipped
- Step 2 (Version Impact Analysis) — skipped; no lock file inspection, no version
  impact table is produced
- Step 3 (Affects Versions Correction) — skipped
- Step 4 (Duplicate, Sibling, Overlap, and Reconciliation Check) — skipped
- Step 5 (Version Lifecycle Check) — skipped
- Step 6 (Already Fixed Check) — skipped
- Step 7 (Concurrent Triage Detection) — skipped
- Step 8 (Remediation) — skipped; no remediation tasks are created

No Jira mutations (label additions, status transitions, task creation, comments) are
performed beyond the Step 0.7 early assignment actions that occurred before ecosystem
detection.

The engineer must assess this vulnerability manually, including:

- Determining which lock file or dependency mechanism to inspect for Go modules
- Manually checking dependency versions across supported product versions
- Creating any remediation tasks through standard Jira workflows

To enable automated triage for Go modules in the future, add an entry to each
stream's Ecosystem Mappings table in security-matrix.md with the appropriate
Repository, Lock File (e.g., `go.sum`), Check Command, and Upstream Branch values.
