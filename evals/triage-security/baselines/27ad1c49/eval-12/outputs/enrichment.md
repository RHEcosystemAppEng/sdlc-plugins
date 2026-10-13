# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

The Jira description for TC-8030 provides imprecise version information:
- **Affected versions**: "versions prior to the fix" (no specific version threshold)
- **Fixed version**: "see advisory" (no specific version number)

External CVE databases are queried to obtain structured, machine-readable version constraints.

## MITRE CVE API

**Source**: https://cveawg.mitre.org/api/cve/CVE-2026-48901

Extracted data:
- **Product**: h2
- **Vendor**: hyperium
- **Affected range**: lessThan 0.4.8 (semver)
- **Fix threshold**: 0.4.8

The MITRE record provides a precise `lessThan` constraint: versions below 0.4.8 are affected.

## OSV.dev API

**Source**: https://api.osv.dev/v1/vulns/CVE-2026-48901

Extracted data:
- **Package**: h2
- **Ecosystem**: crates.io
- **Introduced**: 0 (all versions from the beginning)
- **Fixed**: 0.4.8
- **Aliases**: RUSTSEC-2026-0089

The OSV record confirms the fix was introduced in version 0.4.8. All versions from 0 up to (but not including) 0.4.8 are affected.

## Cross-Validation Table

| Source | Affected range | Fixed version | Status |
|--------|----------------|---------------|--------|
| Jira description | "versions prior to the fix" | "see advisory" | Imprecise -- no usable threshold |
| MITRE CVE API | < 0.4.8 (lessThan, semver) | 0.4.8 | Precise |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 | Precise |

## Cross-Validation Result

**Agreement**: MITRE and OSV.dev both report the same fix threshold of **0.4.8**. The Jira description is imprecise but does not contradict the external data -- it simply lacks a specific version number.

**Enriched fix threshold**: **0.4.8**

The external structured data takes precedence over the imprecise Jira description prose. Versions of h2 below 0.4.8 are affected; versions >= 0.4.8 are not affected.

This enriched threshold will be used in Step 2 (Version Impact Analysis) for comparing dependency versions extracted from lock files against the fix boundary.

## Confidence

**High** -- Both external authoritative sources (MITRE CVE API and OSV.dev) agree on the fix threshold. The Jira description's imprecision is fully resolved by the external data.
