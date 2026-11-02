# Step 2 — Version Impact Analysis

## 2.1 — Load the Supportability Matrix

Loaded security-matrix.md for both configured version streams.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Aggregated all versions from both streams into a single working matrix.

## 2.3 — Extract Dependency Versions

Using pinned commits from the supportability matrix for each version (Important Rule 13 — never branch HEAD for released versions):

### Stream 2.1.x

- **2.1.0** (tag `v0.3.8`): `git show v0.3.8:Cargo.lock | grep -A2 'name = "quinn-proto"'` → quinn-proto **0.11.9**
- **2.1.1** (tag `v0.3.12`): `git show v0.3.12:Cargo.lock | grep -A2 'name = "quinn-proto"'` → quinn-proto **0.11.9**

### Stream 2.2.x

- **2.2.0** (tag `v0.4.5`): `git show v0.4.5:Cargo.lock | grep -A2 'name = "quinn-proto"'` → quinn-proto **0.11.9**
- **2.2.1** (tag `v0.4.8`): `git show v0.4.8:Cargo.lock | grep -A2 'name = "quinn-proto"'` → quinn-proto **0.11.12**
- **2.2.2** (tag `v0.4.9`): retag of 2.2.1 (backend pin `v0.4.8` matches 2.2.1) — carry forward result: quinn-proto **0.11.12** (same as 2.2.1)
- **2.2.3** (tag `v0.4.11`): `git show v0.4.11:Cargo.lock | grep -A2 'name = "quinn-proto"'` → quinn-proto **0.11.14**
- **2.2.4** (tag `v0.4.12`): `git show v0.4.12:Cargo.lock | grep -A2 'name = "quinn-proto"'` → quinn-proto **0.11.14**

## 2.4 — Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

All versions from both the 2.1.x and 2.2.x streams in the supportability matrix are included (Important Rule 4). Retag version 2.2.2 carries forward the affected status from 2.2.1 (Important Rule 5). Pinned commit tags from the supportability matrix are used, not branch HEAD (Important Rule 13).
