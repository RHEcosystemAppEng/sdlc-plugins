# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

The Jira description for TC-8030 provides imprecise version data ("versions prior to the fix" / "see advisory"). External CVE databases were queried to obtain structured, machine-readable version constraints.

### MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed fields:
- **Product**: h2
- **Vendor**: hyperium
- **Affected range**: versions less than 0.4.8 (semver)
- **Fix threshold**: `lessThan: 0.4.8`

Interpretation: all h2 versions below 0.4.8 are affected. Version 0.4.8 and above are fixed.

### OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed fields:
- **OSV ID**: RUSTSEC-2026-0089
- **Aliases**: CVE-2026-48901
- **Package**: h2 (ecosystem: crates.io)
- **Range type**: SEMVER
- **Introduced**: 0 (all versions from the beginning)
- **Fixed**: 0.4.8

Interpretation: all h2 versions from 0 up to (but not including) 0.4.8 are affected. Version 0.4.8 is the fix.

### Cross-Validation Table

| Source | Affected range | Fixed version | Status |
|--------|---------------|---------------|--------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) | Imprecise -- no actionable threshold |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 | Precise |
| OSV.dev | introduced: 0, fixed: 0.4.8 | 0.4.8 | Precise |

### Cross-Validation Result: AGREEMENT

All external sources agree on the fix threshold:

- **MITRE**: `lessThan: 0.4.8` (affected versions are those below 0.4.8)
- **OSV.dev**: `fixed: 0.4.8` (fix introduced at version 0.4.8)

Both sources confirm the same boundary: **h2 < 0.4.8 is affected; h2 >= 0.4.8 is fixed.**

### Enriched Fix Threshold

The Jira description's imprecise data ("versions prior to the fix") has been resolved via external enrichment:

- **Authoritative fix threshold**: `< 0.4.8`
- **Fixed version**: `>= 0.4.8`
- **Confidence**: High (two independent external sources agree; Jira description is consistent but imprecise)

This enriched fix threshold will be used in Step 2.3 for version impact comparisons instead of the imprecise Jira description values.
