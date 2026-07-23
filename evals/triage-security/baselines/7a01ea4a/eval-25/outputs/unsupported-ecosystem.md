# Unsupported Ecosystem Notification

## TC-8040 -- CVE-2026-31812 (quinn-proto)

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

- **Detected ecosystem**: Go modules
- **Vulnerable library**: quinn-proto
- **CVE**: CVE-2026-31812
- **Fixed version**: 0.11.14
- **Stream in scope**: 2.2.x

### Supported ecosystems for this stream

The Ecosystem Mappings table in the 2.2.x stream's `security-matrix.md` defines the following supported ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

Go modules is not among the configured ecosystems. The skill cannot determine the lock file path, check command, or upstream branch for this ecosystem.

### Why automated triage cannot proceed

The triage-security skill reads available ecosystems from the stream's `security-matrix.md` Ecosystem Mappings table rather than assuming a fixed set. When the detected ecosystem is not listed in that table:

1. No lock file path is configured -- the skill does not know which file to inspect (e.g., `go.sum`, `go.mod`)
2. No check command is configured -- the skill does not know how to extract the dependency version
3. No upstream branch is configured -- the skill cannot check upstream fix status

Without these configuration values, Steps 2.3 (dependency version extraction), 2.4 (version impact table), and 2.5 (upstream fix check) cannot execute.

### Recommended next steps

1. **Manual assessment**: Inspect the relevant lock files manually to determine whether `quinn-proto` (or its Go module equivalent) is present in any supported product version at a vulnerable version.
2. **Add ecosystem support**: If Go modules dependencies are common in this product, consider adding a Go modules row to the Ecosystem Mappings table in each stream's `security-matrix.md` via the `/setup` skill:

   | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
   |-----------|------------|-----------|---------------|-----------------|
   | Go modules | backend | `go.sum` | `git show <tag>:go.sum` | `release/0.4.z` |

3. **Re-run triage**: After adding Go modules to the Ecosystem Mappings table, re-run `/sdlc-workflow:triage-security TC-8040` for automated version impact analysis.

### Triage status

Automated triage is **halted** at Step 1 (Ecosystem Detection). No Jira mutations have been performed. The issue remains in its current state (Status: New, Affects Versions: RHTPA 2.0.0).
