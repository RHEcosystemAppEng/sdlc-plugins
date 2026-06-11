# Step 2 -- Version Impact Analysis: TC-8002

## CVE-2026-28940: serde_json < 1.0.135

### Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` from `rhtpa-release.0.4.z`

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

### Cross-stream Coverage (informational -- outside issue scope)

The 2.1.x stream is also checked for completeness per the forward pointer chain:

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | |

### Dependency Version Extraction

Lock file data extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`:

**2.2.x stream (in scope):**

| Version | Tag | serde_json version | Affected? (< 1.0.135) | Notes |
|---------|-----|--------------------|-----------------------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | NO | >= 1.0.135 (patched) |
| 2.2.1 | v0.4.8 | 1.0.138 | NO | >= 1.0.135 (patched) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1, same as 2.2.1 (1.0.138) |
| 2.2.3 | v0.4.11 | 1.0.139 | NO | >= 1.0.135 (patched) |
| 2.2.4 | v0.4.12 | 1.0.139 | NO | >= 1.0.135 (patched) |

**2.1.x stream (out of scope, for reference):**

| Version | Tag | serde_json version | Affected? (< 1.0.135) | Notes |
|---------|-----|--------------------|-----------------------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | NO | >= 1.0.135 (patched) |
| 2.1.1 | v0.3.12 | 1.0.137 | NO | >= 1.0.135 (patched) |

### Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 1.0.138 | NO | ships patched version |
| 2.2.1 | 1.0.138 | NO | ships patched version |
| 2.2.2 | -- | NO | retag of 2.2.1 (1.0.138) |
| 2.2.3 | 1.0.139 | NO | ships patched version |
| 2.2.4 | 1.0.139 | NO | ships patched version |

**Result: NO supported versions in the 2.2.x stream are affected.** All versions ship serde_json >= 1.0.135, which is at or above the fix version. The vulnerability (affecting versions < 1.0.135) does not apply to any shipped version.

Additionally, the 2.1.x stream (outside this issue's scope) also ships serde_json 1.0.137, which is patched. No supported versions across any stream are affected.

### Dependency Chain Analysis (Step 2.3.5)

Not applicable -- no versions are affected, so dependency chain tracing for remediation context is not required.

### Upstream Fix Status (Step 2.5)

Not applicable -- since no versions are affected, upstream fix status is moot. For the record, all shipped versions already include the fix (serde_json >= 1.0.135).
