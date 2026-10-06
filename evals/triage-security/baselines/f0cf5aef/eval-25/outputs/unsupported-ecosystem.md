# Unsupported Ecosystem Notification

## TC-8040 -- CVE-2026-31812 (quinn-proto)

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

The detected ecosystem for the vulnerable library `quinn-proto` resolved to **Go modules**. However, the Ecosystem Mappings tables in the configured security matrices for both version streams only include the following ecosystems:

| Stream | Supported Ecosystems |
|--------|---------------------|
| 2.1.x  | Cargo, RPM          |
| 2.2.x  | Cargo, RPM          |

**Go modules** does not appear in either stream's Ecosystem Mappings table. The triage-security skill requires a matching ecosystem entry to determine the correct lock file path, check command, and remediation task structure.

### Action Required

Automated triage has been stopped. To proceed, one of the following manual actions is needed:

1. **Add Go modules to the Ecosystem Mappings table** in the relevant `security-matrix.md` files (defining the lock file path, check command, and upstream branch), then re-run `/sdlc-workflow:triage-security TC-8040`.
2. **Perform manual assessment** of the vulnerability impact across supported versions without automated lock file inspection.
3. **Re-evaluate the ecosystem detection** -- if the library was misidentified as a Go module and is actually from a supported ecosystem (e.g., Cargo), correct the assessment and re-run triage.
