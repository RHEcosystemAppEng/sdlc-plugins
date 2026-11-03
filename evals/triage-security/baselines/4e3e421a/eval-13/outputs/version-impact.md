# TC-8001 — Step 2: Version Impact Analysis

Source: security-matrix-mock.md (Supportability Matrix + simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
output from the "quinn-proto versions by tag" table). No real git commands were executed.

## 2.1 Matrix loaded

| Stream | Konflux repo | Versions |
|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0 (v0.3.8), 2.1.1 (v0.3.12) |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0 (v0.4.5), 2.2.1 (v0.4.8), 2.2.2 (v0.4.8, retag of 2.2.1), 2.2.3 (v0.4.11), 2.2.4 (v0.4.12) |

Format validation: required sections (Supportability Matrix, Ecosystem Mappings, Source Pinning Method,
Forward Pointer) present; Ecosystem Mappings columns match template -> Pass.

## 2.2 Development stream

No Jira version metadata (unreleased versions) was available in the eval inputs, so no development stream
could be identified. No branch-HEAD row is included (not fabricated). In a live run,
`getJiraIssueTypeMetaWithFields` would be used to find the earliest unreleased `RHTPA` version.

## 2.4 Version impact table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Backend pin | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | outside issue scope (cross-stream) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.8 | — | YES | same as 2.2.1 (backend retag of 2.2.1; lock file check skipped) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

Summary:
- In-scope stream 2.2.x: **2.2.0, 2.2.1, 2.2.2 affected**; 2.2.3 and 2.2.4 not affected.
- Other stream 2.1.x: **2.1.0, 2.1.1 affected** -> cross-stream impact (Case A).
- PSIRT Affects Version `RHTPA 2.0.0` is not a supported version in the matrix and is incorrect.

## 2.3.5 Dependency chain context

```
Dependency chain for quinn-proto:
  backend (workspace) → ... → quinn-proto
  Type: not determinable from the supplied mock data (only resolved lock-file versions were provided;
        no Cargo.toml / dependency graph). Engineer should confirm with `cargo tree -i quinn-proto`
        at v0.4.8 and v0.3.12. quinn-proto is commonly pulled in transitively via `quinn`
        (e.g., reqwest http3 feature) — unverified.
  Profile: assumed production (no evidence of dev-only/build-only scope) — no `dev-dependency` label.
  Version progression: 0.11.9 (v0.3.8 .. v0.4.5) → 0.11.12 (v0.4.8) → 0.11.14 (v0.4.11+)
```

Remediation: if direct, bump quinn-proto to >= 0.11.14; if transitive, bump the direct dependency first,
fall back to `cargo add quinn-proto@0.11.14`.

## 2.5 Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | not available in eval data | UNKNOWN |
| 2.2.x | Cargo | release/0.4.z | not available in eval data | UNKNOWN (tags v0.4.11/v0.4.12 cut from this line already ship 0.11.14, suggesting the fix is present — needs `git show release/0.4.z:Cargo.lock` confirmation) |

Because upstream-branch HEAD could not be confirmed, the **upstream backport + downstream propagation**
task pair is used (not the dependency-bump variant). The engineer should switch the 2.2.x upstream task to the
dependency-bump variant if `release/0.4.z` HEAD is confirmed at >= 0.11.14.

Engineer confirmation of this table is required before Step 3 (assumed confirmed for the eval).
