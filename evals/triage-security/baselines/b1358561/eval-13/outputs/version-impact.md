# TC-8001 — Step 2 Version Impact Analysis

The data comes from the "Mock Lock File Data" section of `security-matrix-mock.md`, which stands in for the output of
`git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at each pinned backend tag.
Released versions use their **pinned** tags only. Retags carry forward the result of the original version.

## 2.1 Matrix load / 2.1.1 format validation

| Stream | Konflux repo | Required sections | Ecosystem Mappings columns | Result |
|--------|--------------|-------------------|----------------------------|--------|
| 2.1.x | rhtpa-release.0.3.z | Supportability Matrix, Ecosystem Mappings, Source Pinning Method, Forward Pointer present | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | Pass |
| 2.2.x | rhtpa-release.0.4.z | all present | matches template | Pass |

Ecosystem used: **Cargo**, repository `backend`, lock file `Cargo.lock`. Upstream branches are `release/0.3.z` (2.1.x) and `release/0.4.z` (2.2.x).

## 2.2 Development stream

Not determinable in this eval, because there is no Jira `getJiraIssueTypeMetaWithFields` call and no unreleased-version data. 2.2.x is the latest configured stream ("no forward pointer"), and no unreleased stream or development branch is configured. No development-stream (branch HEAD) row is added. **Flag:** an engineer should confirm whether an unreleased RHTPA version exists.

## 2.3 / 2.4 Version impact table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build | backend tag (pinned) | quinn-proto | Affected? | Notes |
|---------|--------|-------|----------------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.3.8 | `v0.3.8` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | 0.3.12 | `v0.3.12` | 0.11.9 | **YES** | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | 0.4.5 | `v0.4.5` | 0.11.9 | **YES** | in scope |
| 2.2.1 | 2.2.x | 0.4.8 | `v0.4.8` | 0.11.12 | **YES** | in scope |
| 2.2.2 | 2.2.x | 0.4.9 | `v0.4.8` | — (same as 2.2.1) | **YES** | retag of 2.2.1. Lock check skipped, result carried forward |
| 2.2.3 | 2.2.x | 0.4.11 | `v0.4.11` | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | 0.4.12 | `v0.4.12` | 0.11.14 | NO | fixed version shipped |

Summary:
- **In-scope stream 2.2.x:** 2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 and are not affected.
- **Out-of-scope stream 2.1.x:** 2.1.0 and 2.1.1 are affected (0.11.9). This is cross-stream impact (Case A).
- PSIRT Affects Versions `RHTPA 2.0.0` does not match any supported version.

## 2.3.5 Dependency chain context

quinn-proto is the protocol-state crate of the `quinn` QUIC stack. In Rust it is normally pulled in transitively, for example `backend (workspace) -> reqwest (http3) / quinn -> quinn-proto`. The mock data contains only the `Cargo.lock` version lines, not the `[[package]]` dependency arrays or `Cargo.toml` manifests. The exact chain and direct/transitive classification therefore **could not be verified** and are not asserted here.

```
Dependency chain for quinn-proto:
  backend (workspace) -> ? -> quinn-proto   (chain UNVERIFIED: manifest/dependency arrays not available)
  Type: unverified (likely transitive via quinn)
  Profile: assumed production (present in shipped Cargo.lock at every pinned tag; no dev-only evidence)
  First appeared: present in all checked tags (v0.3.8 onward)
  Version history: 0.11.9 (v0.3.8 - v0.4.5) -> 0.11.12 (v0.4.8) -> 0.11.14 (v0.4.11+)
```

Before the tasks are created, the engineer should run `cargo tree -i quinn-proto` on each upstream branch to confirm the chain. The remediation templates include both the direct and transitive approaches.

No dev-only or feature-gated evidence was found, so no `dev-dependency` label is applied and no VEX feature-gate prompt is shown.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not available (latest released tag `v0.3.12` = 0.11.9) | **NO / unverified**. Treated as not fixed, so the plan is upstream backport + downstream propagation |
| 2.2.x | Cargo | release/0.4.z | not available directly. Tags `v0.4.11` and `v0.4.12` cut from this branch ship 0.11.14 | **YES** (inferred from released tags). Dependency bump variant + downstream propagation |

In a real run, confirm with:
`git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock | grep -A2 'quinn-proto'` and the same command for `release/0.4.z`.

Note for 2.2.x: the Konflux repo `rhtpa-release.0.4.z` already pins `v0.4.12` (0.11.14) for the latest release, 2.2.4. The fix has therefore **already shipped** in 2.2.3. The 2.2.x remediation tasks are mainly a verify-and-confirm step on the upstream branch and Konflux reference. The engineer should decide at the confirmation gate whether they are needed (see remediation.md).

**Engineer confirmation required before Step 3.**

## Step 3 (Affects Versions correction, derived from this table)

Scoped to stream 2.2.x per the `[rhtpa-2.2]` suffix:

`Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Version IDs would be resolved dynamically via `getJiraIssueTypeMetaWithFields(TC, 10024)` and filtered by prefix `RHTPA`. No IDs are hardcoded. 2.1.0 and 2.1.1 are deliberately excluded because they belong to the 2.1.x stream.
