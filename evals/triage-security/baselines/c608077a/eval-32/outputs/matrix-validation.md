# Step 2.1.1 — Matrix Format Validation: TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Stream under validation**: 2.2.x (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
**Matrix file**: `security-matrix-no-forward-pointer-mock.md` (stands in for the 2.2.x stream's `security-matrix.md`)
**Canonical template**: `docs/templates/security-matrix.template.md`
**Mode**: Interactive (not Fullsend). No Jira, git, or other external calls were made for this eval.

## Template extraction

**Required section headings** (the `##` / `###` headings the skill enforces):

1. `## Supportability Matrix`
2. `## Ecosystem Mappings`
3. `### Source Pinning Method`
4. `## Forward Pointer`

`## Version Stream` is informational only and is not enforced. `#### Container Images` is a level-4 heading, so it is outside the `##`/`###` set this check enforces.

**Expected Ecosystem Mappings columns** (exact names, in this order):
`Ecosystem | Repository | Lock File | Check Command | Upstream Branch`

## Check 1 — Required sections present

| Required Section | Present? | Result |
|---|---|---|
| `## Supportability Matrix` | Yes | PASS |
| `## Ecosystem Mappings` | Yes | PASS |
| `### Source Pinning Method` | Yes | PASS |
| `## Forward Pointer` | **No** | **MISSING — can be auto-repaired** |

(`## Version Stream` is present: informational, not enforced.)

## Check 2 — Ecosystem Mappings column structure

- Expected: `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- Actual:   `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`
- Column count: 5 / 5. Names and order match exactly. No extra whitespace in headers.
- **Result: PASS**

## Check 3 — Table parsability

| Table | Header Row | Separator Row (`---`) | Data Rows | Result |
|---|---|---|---|---|
| Supportability Matrix | `Version \| Build \| Build Date \| backend \| Notes` | Yes | 2 (2.2.0, 2.2.1) | PASS |
| Ecosystem Mappings | `Ecosystem \| Repository \| Lock File \| Check Command \| Upstream Branch` | Yes | 1 (Cargo) | PASS |

Supportability Matrix column names depend on the product, so the check only confirms the table parses. It does not compare the names to the template (`Version` rather than `Product Version` is acceptable).

## Auto-repairs

| # | Issue | Repair (proposed in memory) | Log |
|---|---|---|---|
| 1 | Missing `## Forward Pointer` section | Add `## Forward Pointer` with content `None` to the end of the proposed matrix | Auto-repaired: appended missing Forward Pointer section to `security-matrix-no-forward-pointer-mock.md`. |

No column-header whitespace normalization was needed.

The source matrix was not changed in place during validation. Content appended to the proposed matrix:

```markdown

## Forward Pointer

None
```

The full repaired proposal is in `outputs/security-matrix-repaired.md`.

**Local matrix write safety.** In a live interactive run, the skill re-reads the target immediately before the repair write and compares it with the snapshot taken at validation time:

- **File unchanged**: the repair is written and `Last-Updated` is updated after the write succeeds.
- **File changed**: the current file is kept, and the skill asks for a fresh review or aborts.

This eval did not write to the real matrix path. The repaired content is in `outputs/` only, so the source fixture and its `Last-Updated` timestamp (2026-06-28T10:00:00Z) are unchanged.

## Warnings (cannot be auto-repaired)

None:
- Both critical sections (`## Supportability Matrix`, `## Ecosystem Mappings`) are present.
- No Ecosystem Mappings column mismatch.
- No malformed tables.

## Validation outcome

**Result: REPAIRED**. The only issue was auto-fixable: the missing Forward Pointer section. Under Step 2.1.1 the triage reports the repair and **proceeds without prompting the user**. The 2.2.x stream stays in the aggregated working matrix (versions 2.2.0 → backend `v0.4.5`, 2.2.1 → backend `v0.4.8`; Cargo / `Cargo.lock` / upstream branch `release/0.4.z`) and goes on to Step 2.2+ version impact analysis for quinn-proto (< 0.11.14).

### Notes outside Step 2.1.1 (for later steps; they do not affect this result)

- **Staleness (Step 0.3).** `Last-Updated` is 2026-06-28, which is about 145 days before today (2026-11-20). That exceeds the 14-day threshold, so a live run would show the Refresh / Proceed / Stop staleness prompt.
- **No Container Images section.** The matrix has no `#### Container Images` section. This is not a Step 2.1.1 failure, but in a live run on-demand matrix population would research and propose the `(Product Version, Component)` rows.
- **2.1.x stream not validated.** Security Configuration also lists a 2.1.x stream (`rhtpa-release.0.3.z`), but no matrix fixture was provided for it, so it was not validated here.
