# Unsupported Ecosystem Notification

**Unsupported ecosystem**: Go modules is not yet supported for automated triage.
Manual assessment is required.

---

Automated triage for TC-8040 (CVE-2026-31812, quinn-proto) has stopped at Step 1
(Ecosystem Detection). The detected ecosystem `Go modules` does not appear in the
Ecosystem Mappings table for any configured version stream. No version impact
analysis, Affects Versions correction, or remediation task creation was performed.

To proceed, either:
1. Add a `Go modules` row to the Ecosystem Mappings table in `security-matrix.md`
   for the relevant version stream(s), specifying the lock file path and check
   command, then re-run `/triage-security TC-8040`.
2. Perform a manual assessment of the vulnerability impact across supported versions.
