# Step 2.1.1 — Matrix Format Validation Results

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Execution mode**: Interactive (`FULLSEND_OUTPUT_DIR` absent)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Matrix source**: `evals/triage-security/files/security-matrix-mock.md` (contains the matrices for both configured Version Streams, one per `# Stream N` block)

## Template Extraction

Required section headings, taken from the template's `##`/`###` headings (Step 2.1.1). `## Version Stream` is informational and not enforced:

| # | Required heading | Level |
|---|---|---|
| 1 | `## Supportability Matrix` | `##` |
| 2 | `### Source Pinning Method` | `###` |
| 3 | `## Ecosystem Mappings` | `##` |
| 4 | `## Forward Pointer` | `##` |

Expected Ecosystem Mappings columns, in this order:

`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

Supportability Matrix columns are product-specific. Only parsability is checked, not the column names.

---

## Stream 2.1.x — `rhtpa-release.0.3.z`

Configured Konflux repo: `git.example.com/rhtpa/rhtpa-release.0.3.z` (local path `/home/dev/repos/rhtpa-release.0.3.z`)

### Check 1 — Required sections present

| Required heading | Present? | Notes |
|---|---|---|
| `## Supportability Matrix` | PASS | Found |
| `### Source Pinning Method` | PASS | Found |
| `## Ecosystem Mappings` | PASS | Found |
| `## Forward Pointer` | PASS | Found. Content: "Next stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`" |
| `## Version Stream` (informational) | Present | Not enforced |

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | PASS |
| 2 | Repository | Repository | PASS |
| 3 | Lock File | Lock File | PASS |
| 4 | Check Command | Check Command | PASS |
| 5 | Upstream Branch | Upstream Branch | PASS |

Column count: 5 expected, 5 actual. Header cells have no extra whitespace.

### Check 3 — Table parsability

| Table | Header row | Separator row (`---`) | Data rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | Present | 2 (2.1.0, 2.1.1) | PASS |
| Ecosystem Mappings | Present | Present | 2 (Cargo, RPM) | PASS |

### Auto-repairs

None needed. The Forward Pointer section exists and the headers have no stray whitespace.

### Warnings

None.

### Result: **PASS**. The stream proceeds to aggregation.

---

## Stream 2.2.x — `rhtpa-release.0.4.z`

Configured Konflux repo: `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path `/home/dev/repos/rhtpa-release.0.4.z`)

### Check 1 — Required sections present

| Required heading | Present? | Notes |
|---|---|---|
| `## Supportability Matrix` | PASS | Found |
| `### Source Pinning Method` | PASS | Found |
| `## Ecosystem Mappings` | PASS | Found |
| `## Forward Pointer` | PASS | Found. Content: "This is the latest stream — no forward pointer." |
| `## Version Stream` (informational) | Present | Not enforced |

### Check 2 — Ecosystem Mappings column structure

| Position | Expected | Actual | Match |
|---|---|---|---|
| 1 | Ecosystem | Ecosystem | PASS |
| 2 | Repository | Repository | PASS |
| 3 | Lock File | Lock File | PASS |
| 4 | Check Command | Check Command | PASS |
| 5 | Upstream Branch | Upstream Branch | PASS |

Column count: 5 expected, 5 actual. Header cells have no extra whitespace.

### Check 3 — Table parsability

| Table | Header row | Separator row (`---`) | Data rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | Present | 5 (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) | PASS |
| Ecosystem Mappings | Present | Present | 2 (Cargo, RPM) | PASS |

### Auto-repairs

None needed.

### Warnings

None.

### Result: **PASS**. The stream proceeds to aggregation.

---

## Summary

| Stream | Matrix | Sections | Ecosystem Mappings columns | Parsability | Auto-repairs | Warnings | Outcome |
|---|---|---|---|---|---|---|---|
| 2.1.x | rhtpa-release.0.3.z | 4/4 | Exact match | PASS | None | None | **PASS** |
| 2.2.x | rhtpa-release.0.4.z | 4/4 | Exact match | PASS | None | None | **PASS** |

**Overall outcome: PASS.** Step 2.1.1 says a pass proceeds silently, so there is no user prompt, nothing is written to any `security-matrix.md`, and the `Last-Updated` timestamps are unchanged. Both streams go into the aggregated working matrix: 7 released versions, 2.1.0–2.1.1 and 2.2.0–2.2.4, with 2.2.2 recorded as a backend retag of 2.2.1 (`v0.4.8`).

## Informational observations (outside Step 2.1.1 checks, not blocking)

1. **Supportability Matrix column naming.** The matrices use `Version` where the template uses `Product Version`. Step 2.1.1 treats Supportability Matrix columns as product-specific, so this is not a warning. The `backend` source column matches the template's `{source-repo-name}` expansion pattern. The configured Source Repositories name is `rhtpa-backend`, though, not `backend`, so later steps have to map that name.
2. **`#### Container Images` section missing.** The template declares this at heading level 4, so it is not one of the required `##`/`###` headings and Step 2.1.1 does not check it. Its absence matters to the separate *On-demand matrix population* procedure, which would propose adding the section (interactive and confirmation-gated). It does not affect format validation.
3. **Matrix staleness (Step 0.3 context).** The file header is `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. That is 128 days before today (2026-11-03) and over the 14-day threshold, so Step 0.3 would already have raised the staleness warning (Refresh / Proceed / Stop) before Step 2.1.1. This validation assumes the engineer chose to proceed.
4. **Configuration note.** The Version Streams table in the supplied CLAUDE.md has no `Security Matrix Path` column. For this eval, the matrix content came from the supplied mock file rather than from a configured path.
