# Unsupported Ecosystem Notification

After Step 1 Ecosystem Detection resolved to **Go modules**, the skill checked the 2.2.x stream's Ecosystem Mappings table and found that Go modules is not a supported ecosystem.

The following notification is presented to the user:

---

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

---

## Triage Halted

Automated triage stops at this point. The following steps are **not performed** for the unsupported ecosystem:

- Step 1.5 (External CVE Data Enrichment) -- skipped
- Step 1.7 (Embargo Check) -- skipped
- Step 2 (Version Impact Analysis) -- skipped
- Step 3 (Affects Versions Correction) -- skipped
- Step 4 (Duplicate, Sibling, Overlap, and Reconciliation Check) -- skipped
- Step 5 (Version Lifecycle Check) -- skipped
- Step 6 (Already Fixed Check) -- skipped
- Step 7 (Concurrent Triage Detection) -- skipped
- Step 8 (Remediation) -- skipped

No version impact analysis, remediation task creation, Affects Versions correction, or Jira mutations are performed. The engineer must assess the Go modules ecosystem vulnerability manually and determine the appropriate remediation path outside of automated triage.

## Recommendation

To enable automated triage for Go modules in the future, add a row to the Ecosystem Mappings table in the stream's security-matrix.md with the appropriate lock file path (e.g., `go.sum`), check command, and upstream branch configuration. Then update the ecosystem classification table to define whether Go modules is a source dependency or system package ecosystem.
