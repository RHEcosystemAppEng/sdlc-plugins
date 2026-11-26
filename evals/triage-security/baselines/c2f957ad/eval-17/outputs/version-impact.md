# Step 2 – Version Impact Analysis: CVE-2026-31812 (TC-8001)

## 2.1 Supportability matrix (aggregated)

Loaded from `security-matrix-mock.md` (both streams). Format validation: Pass. Required sections are present
(Supportability Matrix, Ecosystem Mappings, Source Pinning Method, Forward Pointer). The Ecosystem Mappings
columns match `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`.

| Stream | Version | Build | backend tag | Notes |
|---|---|---|---|---|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | |

## 2.2 Development stream

Not determined. Step 2.2 finds the dev stream from unreleased Jira versions (`getJiraIssueTypeMetaWithFields`),
and Jira cannot be called in this eval. No dev-stream branch HEAD lock data was provided. **Dev stream: not assessed.**
Engineer action: confirm whether an unreleased RHTPA version (e.g. 2.3/3.0) exists and check its branch HEAD `Cargo.lock`.

## 2.3 Dependency versions (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`)

Fix threshold: quinn-proto **< 0.11.14** is affected; **0.11.14** is fixed (Jira description; external enrichment unavailable).

## 2.4 Version impact table

```
Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0   | 2.1.x  | 0.11.9      | YES       | v0.3.8; outside issue scope (cross-stream) |
| 2.1.1   | 2.1.x  | 0.11.9      | YES       | v0.3.12; outside issue scope (cross-stream) |
| 2.2.0   | 2.2.x  | 0.11.9      | YES       | v0.4.5 |
| 2.2.1   | 2.2.x  | 0.11.12     | YES       | v0.4.8 |
| 2.2.2   | 2.2.x  | —           | YES       | same as 2.2.1 (backend retag of v0.4.8) |
| 2.2.3   | 2.2.x  | 0.11.14     | NO        | v0.4.11; fixed version |
| 2.2.4   | 2.2.x  | 0.11.14     | NO        | v0.4.12; fixed version |
| dev     | —      | —           | UNKNOWN   | not assessed (needs Jira unreleased versions + branch HEAD) |
```

Summary:
- **In scope (2.2.x):** 2.2.0, 2.2.1, 2.2.2 affected. 2.2.3 and 2.2.4 are not affected (the fix first shipped in 2.2.3 / backend v0.4.11).
- **Cross-stream (2.1.x):** 2.1.0 and 2.1.1 affected. No released 2.1.x version ships the fix.
- **PSIRT Affects Versions mismatch:** the Jira field says `RHTPA 2.0.0`. That version is not in any supported stream and has no lock-file evidence. The proposed correction (Step 3, scoped to 2.2.x) is **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**, with RHTPA 2.0.0 removed. Version IDs would be found at runtime and are not hardcoded.

## 2.3.5 Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) → ... → quinn-proto
  Type: undetermined. Cargo.toml / full Cargo.lock dependency graph not available in eval data.
        quinn-proto is usually pulled in transitively (e.g. via quinn ← reqwest/h3 HTTP/3 support);
        must be confirmed from manifests before implementation.
  Profile: assumed production (no evidence of [dev-dependencies]/[build-dependencies] gating)
  Present in: all released 2.1.x and 2.2.x versions (0.11.9 → 0.11.12 → 0.11.14)
  Fixed at: backend v0.4.11 (2.2.3) and later

Remediation: if transitive, bump the direct dependency that pulls in quinn-proto first;
otherwise pin quinn-proto >= 0.11.14 directly (cargo add / cargo update -p quinn-proto).
```

## 2.5 Upstream fix status

Branch HEADs could not be inspected (`git show` is disallowed in this eval). The status below is inferred from the newest **tag** evidence on each upstream branch and must be confirmed at branch HEAD.

```
Upstream fix status:

| Stream | Ecosystem | Upstream Branch | Version at latest known tag     | Fixed? |
|--------|-----------|-----------------|---------------------------------|--------|
| 2.1.x  | Cargo     | release/0.3.z   | 0.11.9 (v0.3.12)                | NO (HEAD unverified) |
| 2.2.x  | Cargo     | release/0.4.z   | 0.11.14 (v0.4.11, v0.4.12)      | YES (HEAD unverified) |
```

Remediation paths:
- **2.2.x:** fix available upstream, and already shipped in 2.2.3/2.2.4. Use the dependency bump / reference variant.
- **2.1.x:** not fixed upstream. Needs an upstream backport PR on `release/0.3.z`, then a Konflux release repo update.

**Engineer confirmation required** for this table before Step 3 (simulated: confirmed).
