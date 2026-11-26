# Step 2 — Version Impact Analysis for TC-8001

Dependency versions come from the simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` output in security-matrix-mock.md. Each lookup uses the backend tag pinned in the supportability matrix.

## Development stream (Step 2.2)

No Jira version metadata (unreleased RHTPA versions) was supplied, so no development stream could be identified. 2.2.x is the latest configured stream (it has no forward pointer). It is fully covered below through its released pinned tags.

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Pinned backend tag | quinn-proto | Affected? | Notes |
|---------|--------|--------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | same as 2.2.1 (backend retag of 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

**Summary**
- In scope (2.2.x): **2.2.0, 2.2.1, 2.2.2** are affected. 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14.
- Out of scope: **2.1.0 and 2.1.1** (2.1.x) are also affected, which triggers Case A (cross-stream impact).
- PSIRT's Affects Versions value `RHTPA 2.0.0` matches no supported version.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Cargo.lock in rhtpa-backend)
  Introduced: present from v0.3.8 (2.1.0) onward
  Fixed in tree: v0.4.11 (2.2.3), quinn-proto 0.11.14
  Direct/transitive: not determinable from mock data (manifest content not supplied).
    quinn-proto is normally pulled in transitively via quinn (QUIC). Remediation
    tasks therefore include the two-tier approach (bump direct dep; pin fallback).
  Scope: runtime (not dev-only/build-only), so the dev-dependency override does not apply.
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not supplied; latest tag v0.3.12 = 0.11.9 | NO (no evidence of fix) |
| 2.2.x | Cargo | release/0.4.z | not supplied; tags v0.4.11/v0.4.12 on this branch = 0.11.14 | YES |

- **2.2.x**: The fix is already on the release/0.4.z line and has shipped in released builds 2.2.3 and 2.2.4. Customers on 2.2.0 through 2.2.2 can resolve the CVE by upgrading to 2.2.3 or later.
- **2.1.x**: There is no evidence of a fix on release/0.3.z. This stream needs an upstream backport followed by downstream propagation.

The engineer reviews and confirms this table before Step 3.
