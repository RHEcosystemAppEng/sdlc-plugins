# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed structured data:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Version type | semver |

The MITRE CVE record provides a machine-readable `lessThan` constraint: all versions below 0.4.8 are affected.

### OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed structured data:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions from initial release) |
| Fixed | 0.4.8 |

The OSV.dev record confirms the fix version as 0.4.8, with all prior versions affected from initial release.

### Cross-Validation Table

| Source | Affected range | Fixed version | Precision |
|--------|----------------|---------------|-----------|
| Jira description | "versions prior to the fix" | "see advisory" | Imprecise -- no specific threshold |
| MITRE CVE API | < 0.4.8 | 0.4.8 | Precise (semver lessThan constraint) |
| OSV.dev | introduced: 0, fixed: 0.4.8 | 0.4.8 | Precise (semver range with introduced/fixed events) |

### Cross-Validation Result

**Agreement**: MITRE CVE API and OSV.dev both specify the fix threshold as **0.4.8**. The Jira description is imprecise ("versions prior to the fix" / "see advisory") but does not contradict the external data -- it simply lacks specificity.

**Enriched fix threshold**: **< 0.4.8** (versions below 0.4.8 are affected; 0.4.8 and above are fixed)

This enriched threshold from external sources takes precedence over the imprecise Jira description data because it provides machine-readable version constraints. The enriched fix threshold will be used in Step 2.3 for version impact comparisons.
