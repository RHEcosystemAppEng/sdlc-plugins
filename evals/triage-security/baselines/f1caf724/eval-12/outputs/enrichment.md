# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed fields from the CNA container:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Version type | semver |

The MITRE CVE record provides a precise machine-readable version constraint: all semver versions less than 0.4.8 are affected. The fix threshold is **0.4.8**.

### OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed fields:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions from the beginning) |
| Fixed | 0.4.8 |

The OSV.dev record confirms the fix at version **0.4.8**, with all prior versions affected.

### Cross-Validation

| Source | Affected range | Fixed version |
|--------|---------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Assessment**: The MITRE CVE API and OSV.dev are in **agreement** -- both report the fix threshold as **0.4.8**. The Jira description is imprecise ("versions prior to the fix" / "see advisory") but consistent with the external data -- it simply lacks a specific version number.

### Enriched Fix Threshold

**Fix threshold: 0.4.8** (from MITRE CVE API and OSV.dev, cross-validated)

- Versions of h2 **< 0.4.8** are **affected**
- Versions of h2 **>= 0.4.8** are **not affected**

This enriched fix threshold supersedes the imprecise Jira description data and will be used in Step 2.3 for version impact comparisons. The external data takes precedence because it provides machine-readable version constraints rather than prose-parsed ranges.
