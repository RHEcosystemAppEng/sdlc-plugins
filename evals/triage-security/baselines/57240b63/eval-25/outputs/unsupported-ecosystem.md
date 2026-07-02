# Unsupported Ecosystem Notification

## CVE-2026-31812 -- quinn-proto

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

---

### Context

- **Issue**: TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
- **Detected ecosystem**: Go modules
- **Stream**: 2.2.x (rhtpa-release.0.4.z)
- **Supported ecosystems in this stream**: Cargo, RPM

### Why triage stopped

The triage-security skill determines the ecosystem from the vulnerable library name and component context. The supported ecosystems are defined in each stream's `security-matrix.md` Ecosystem Mappings table. The skill reads available ecosystems from configuration rather than assuming a fixed set.

The detected ecosystem **Go modules** does not appear in the Ecosystem Mappings table for the 2.2.x stream (or the 2.1.x stream). Without a matching ecosystem entry, the skill cannot determine:

1. Which lock file to inspect (e.g., `go.sum`, `go.mod`)
2. Which check command to use for dependency version extraction
3. Which repository contains the relevant dependency data

Automated version impact analysis (Step 2) requires this ecosystem mapping to function.

### Recommended next steps

1. **Manual assessment**: Inspect the relevant dependency files manually to determine whether the product ships a vulnerable version of quinn-proto.
2. **Add ecosystem support**: If Go modules dependencies are tracked in this product, add a row to the Ecosystem Mappings table in the stream's `security-matrix.md`:

   | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
   |-----------|------------|-----------|---------------|-----------------|
   | Go modules | <repository> | `go.sum` | `git show <tag>:go.sum` | `<branch>` |

3. **Re-run triage**: After adding the ecosystem mapping, re-run `/sdlc-workflow:triage-security TC-8001` to complete automated triage.
