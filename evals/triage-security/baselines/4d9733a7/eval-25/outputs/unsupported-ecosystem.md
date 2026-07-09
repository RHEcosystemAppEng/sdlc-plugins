# Unsupported Ecosystem Notification

## Step 5.3 -- Unsupported Ecosystem Handling

The ecosystem detection in Step 1 resolved to **Go modules**, which is not listed in the Ecosystem Mappings table for the 2.2.x stream (or any configured stream). The Ecosystem Mappings table only contains: Cargo, RPM.

### Notification to User

> **Unsupported ecosystem**: Go modules is not yet supported for automated triage.
> Manual assessment is required.

### Triage Halted

Automated triage is stopped at this point. The following steps will NOT be performed for the Go modules ecosystem:

- Step 2 (Version Impact Analysis) -- skipped
- Step 2.3 (Dependency version extraction) -- skipped
- Step 2.3.5 (Dependency chain context) -- skipped
- Step 3 (Affects Versions Correction) -- skipped
- Step 4 (Duplicate/Sibling Check) -- skipped
- Step 5 (Version Lifecycle Check) -- skipped
- Step 6 (Already Fixed Check) -- skipped
- Step 7 (Concurrent Triage Detection) -- skipped
- Step 8 (Remediation) -- skipped

No version impact analysis, remediation task creation, or Affects Versions correction is performed. The engineer must assess the Go modules dependency manually and determine the appropriate remediation approach outside of automated triage.
