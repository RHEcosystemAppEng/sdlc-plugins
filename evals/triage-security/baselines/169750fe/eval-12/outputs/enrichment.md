# Step 1.5 -- External CVE Data Enrichment

## MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Extracted structured data:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Fix threshold | 0.4.8 |

The MITRE CVE record specifies a precise `lessThan` constraint: versions below `0.4.8` are affected. The `versionType` is `semver`, confirming standard semantic versioning comparison applies.

## OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Extracted structured data:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Ecosystem | crates.io |
| Package | h2 |
| Introduced | 0 (all versions from the beginning) |
| Fixed | 0.4.8 |

The OSV.dev record uses SEMVER range events: the vulnerability was introduced at version `0` (all versions) and fixed at `0.4.8`.

## Cross-Validation Table

| Source | Affected range | Fixed version | Status |
|--------|---------------|---------------|--------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) | Imprecise -- no actionable threshold |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 | Precise -- structured data |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 | Precise -- structured data |

## Cross-Validation Result

**Agreement**: MITRE CVE API and OSV.dev both report the fix threshold as **0.4.8**. The two external sources are in full agreement.

The Jira description was imprecise ("versions prior to the fix" / "see advisory") and could not provide an actionable version threshold on its own. The external CVE databases supply the precise, machine-readable constraint that the Jira description lacks.

## Enriched Fix Threshold

**Fix threshold for Step 2.3: `0.4.8`**

All h2 versions `< 0.4.8` are affected by CVE-2026-48901. Versions `>= 0.4.8` are not affected.

This enriched fix threshold takes precedence over the imprecise Jira description data and will be used for all version impact comparisons in Step 2.3.
