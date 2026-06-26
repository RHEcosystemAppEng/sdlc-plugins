# Step 2 -- Version Impact Analysis

## CVE-2026-31812: quinn-proto (fixed in 0.11.14)

### Version Impact Table

| Stream | Version | Build Tag | quinn-proto version | Affected? | Notes |
|--------|---------|-----------|---------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.x | 2.2.2 | v0.4.9 | 0.11.12 | YES | same as 2.2.1 (retag of v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Analysis

**Issue-scoped stream (2.2.x):**
- Versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 and are **affected**.
- Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fix version) and are **not affected**.
- Version 2.2.2 is a retag of 2.2.1 (backend tag v0.4.9 is a retag of v0.4.8), so it ships the same quinn-proto 0.11.12.

**Cross-stream impact (2.1.x):**
- All 2.1.x versions (2.1.0 and 2.1.1) ship quinn-proto 0.11.9 and are **affected**.
- This stream is outside the issue's scope (`[rhtpa-2.2]`) and will be reported as cross-stream impact in Step 7.

### Upstream Fix Status

The upstream fix is available in [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048). The fix was incorporated starting with backend tag v0.4.11 (quinn-proto 0.11.14), which first appeared in product version RHTPA 2.2.3. The 2.1.x stream upstream branch (`release/0.3.z`) has not yet received the fix -- all 2.1.x versions still ship the vulnerable 0.11.9.
