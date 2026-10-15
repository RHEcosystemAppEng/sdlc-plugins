# Version Impact Analysis -- TC-8002

## CVE-2026-28940: serde_json (affected versions: before 1.0.135)

### Version Impact Table

| Version | Stream | Backend Tag | serde_json Version | Affected? | Notes                |
|---------|--------|-------------|--------------------|-----------|-----------------------|
| 2.1.0   | 2.1.x  | `v0.3.8`    | 1.0.137            | NO        |                       |
| 2.1.1   | 2.1.x  | `v0.3.12`   | 1.0.137            | NO        |                       |
| 2.2.0   | 2.2.x  | `v0.4.5`    | 1.0.138            | NO        |                       |
| 2.2.1   | 2.2.x  | `v0.4.8`    | 1.0.138            | NO        |                       |
| 2.2.2   | 2.2.x  | `v0.4.8`    | 1.0.138            | NO        | retag of 2.2.1        |
| 2.2.3   | 2.2.x  | `v0.4.11`   | 1.0.139            | NO        |                       |
| 2.2.4   | 2.2.x  | `v0.4.12`   | 1.0.139            | NO        |                       |

### Analysis

Every supported version across both streams ships serde_json **at or above** the fix threshold of 1.0.135:

- **Stream 2.1.x** (2.1.0, 2.1.1): all ship serde_json 1.0.137, which is above the fix version 1.0.135.
- **Stream 2.2.x** (2.2.0 through 2.2.4): all ship serde_json 1.0.138 or 1.0.139, both above the fix version 1.0.135.
- **Version 2.2.2** is a retag of 2.2.1 (identical backend tag `v0.4.8`), so its serde_json version is carried forward as 1.0.138.

**No supported version ships a vulnerable version of serde_json.** The earliest version in the matrix (2.1.0, built 2025-09-15) already included serde_json 1.0.137, which is 2 patch versions above the fix threshold of 1.0.135.

### Dependency Chain Context

serde_json is a Rust crate found in `Cargo.lock`. Based on the ecosystem mappings, it is inspected via `git show <tag>:Cargo.lock`. As all versions are already at or above the fix threshold, detailed dependency chain tracing (direct vs. transitive) is not required for remediation purposes.

### Upstream Fix Status

Not applicable -- no versions are affected, so upstream fix status does not influence remediation decisions.
