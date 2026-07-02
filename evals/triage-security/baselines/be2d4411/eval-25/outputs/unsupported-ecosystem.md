# Unsupported Ecosystem Notification

## TC-8040 -- CVE-2026-31812 (quinn-proto)

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

---

### Context

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Scoped stream**: 2.2.x
- **Configured ecosystems in stream 2.2.x**: Cargo, RPM

The detected ecosystem (Go modules) does not appear in the Ecosystem Mappings table for any configured version stream. Without a mapping entry, the skill has no lock file path or check command to inspect dependency versions, so automated version impact analysis cannot be performed.

### Required Action

Manual assessment is required. An engineer should:

1. Identify the correct lock file or dependency manifest for Go modules in the affected repositories
2. Manually inspect dependency versions at the pinned commits from the supportability matrix
3. Determine which supported product versions ship the vulnerable version of quinn-proto (versions before 0.11.14)
4. Update Affects Versions and create remediation tasks as needed

### Triage Status

Automated triage **stopped** at Step 1 (Ecosystem Detection). No version impact analysis, Affects Versions correction, or remediation tasks were created.
