# Unsupported Ecosystem Notification

## CVE-2026-31812 -- quinn-proto

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

---

### Context

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Stream in scope**: 2.2.x (from issue suffix `[rhtpa-2.2]`)
- **Supported ecosystems for this stream**: Cargo, RPM

### Why triage stopped

The triage-security skill reads available ecosystems from each stream's `security-matrix.md` Ecosystem Mappings table. The 2.2.x stream (`rhtpa-release.0.4.z`) only defines mappings for **Cargo** and **RPM**. Since **Go modules** is not listed, the skill cannot determine the correct lock file, check command, or upstream branch to use for automated version impact analysis.

### Recommended next steps

1. **Manual assessment**: An engineer should manually determine whether the vulnerable version of quinn-proto is shipped in any supported product version by inspecting the appropriate Go dependency files (e.g., `go.sum`, `go.mod`).
2. **Add ecosystem support**: If Go modules dependencies are part of the product build pipeline, consider adding a Go modules row to the Ecosystem Mappings table in `security-matrix.md` for each version stream, specifying the repository, lock file path (`go.sum`), check command, and upstream branch. Then re-run `/sdlc-workflow:triage-security TC-8040`.
