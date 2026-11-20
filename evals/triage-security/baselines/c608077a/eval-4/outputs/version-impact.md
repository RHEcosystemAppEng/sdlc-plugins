# Step 2 – Version Impact Analysis: CVE-2026-33501 (h2 < 0.4.8)

Lock file data comes from the simulated `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
output in `security-matrix-mock.md`. Every released version was checked at its pinned
backend tag from the supportability matrix. Both streams were enumerated from the
Version Streams table (2.1.x → rhtpa-release.0.3.z, 2.2.x → rhtpa-release.0.4.z).

## Version impact table

| Stream | Version | Backend tag | h2 | Affected? | Notes |
|--------|---------|-------------|----|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8`  | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | `v0.4.5`  | 0.4.8 | NO | ships the fixed version (0.4.8) |
| 2.2.x | 2.2.1 | `v0.4.8`  | 0.4.8 | NO | ships the fixed version (0.4.8) |
| 2.2.x | 2.2.2 | `v0.4.8`  | —     | NO | retag of 2.2.1 (same as 2.2.1; backend lock check skipped) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.4.9 | NO | |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.4.9 | NO | |

## Mixed impact across streams

| Stream | Result | Summary |
|--------|--------|---------|
| **2.1.x** | **AFFECTED** | All released versions (2.1.0, 2.1.1) ship h2 0.4.5 |
| **2.2.x** | **NOT AFFECTED** | Every 2.2.x version ships h2 >= 0.4.8 (0.4.8 or 0.4.9) |

PSIRT's claim that RHTPA 2.2.0 is affected is a **false positive**: 2.2.0 already ships
h2 0.4.8, which is the fixed version (the range is exclusive: "before 0.4.8").

## Development stream (Step 2.2)

Dev stream detection needs the unreleased RHTPA versions from
`getJiraIssueTypeMetaWithFields`. No Jira calls were allowed and no unreleased version
data was supplied, so no separate development stream was identified. 2.2.x is the
latest configured stream (no forward pointer). Its newest pinned tag already ships
h2 0.4.9, and dependency versions in a stream do not normally regress, so the dev
head is very unlikely to be affected. **Engineer to confirm** with
`git show HEAD:Cargo.lock` in rhtpa-backend once the dev stream is identified.

## Dependency chain context (Step 2.3.5), affected 2.1.x versions

```
Dependency chain for h2:
  backend (workspace) → [hyper / reqwest / tonic] → h2   (expected)
  Type: likely transitive. h2 is normally pulled in by hyper (HTTP/2 support).
        Cargo.toml / `cargo tree -i h2` was not inspected in this eval; confirm in the task.
  Profile: production (HTTP/2 server stack is a runtime dependency)
  Present in: 2.1.0, 2.1.1 (h2 0.4.5); 2.2.x moved to 0.4.8+ starting with 2.2.0

Remediation: bump the direct dependency (e.g. hyper/reqwest) so that h2 resolves to
>= 0.4.8; fallback `cargo update -p h2 --precise 0.4.8` or `cargo add h2@0.4.8`.
h2 0.4.5 → 0.4.8 is a semver-compatible patch bump within 0.4.x, so a lockfile-only update
should be possible.
```

## Upstream fix status (Step 2.5)

| Stream | Ecosystem | Repository | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|------------|-----------------|------------|--------|
| 2.1.x | Cargo | backend (rhtpa-backend) | `release/0.3.z` | not available (no git access in eval) | **Unconfirmed → treated as NOT fixed** |
| 2.2.x | Cargo | backend (rhtpa-backend) | `release/0.4.z` | n/a, stream not affected | n/a |

Because a fix on `release/0.3.z` could not be confirmed, the 2.1.x remediation uses the
**upstream backport + downstream propagation** pair. If
`git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock` already shows
h2 >= 0.4.8, switch the first task to the dependency-bump variant.

**Next step:** engineer reviews this table (confirmation gate) before Step 3.
