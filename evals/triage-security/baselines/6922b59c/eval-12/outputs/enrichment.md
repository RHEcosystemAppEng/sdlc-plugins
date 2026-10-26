# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

The Jira description for TC-8030 provides imprecise version information:
- Affected versions: "versions prior to the fix" (no numeric threshold)
- Fixed version: "see advisory" (no numeric version)

External CVE databases were queried to obtain structured, machine-readable version constraints.

### MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 (semver) |
| Status | affected |

The MITRE record provides a precise `lessThan` constraint: all versions below 0.4.8 are affected. Version 0.4.8 is the first fixed version.

### OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Package | h2 |
| Ecosystem | crates.io |
| Introduced | 0 (all versions from the beginning) |
| Fixed | 0.4.8 |

The OSV record confirms: vulnerability was introduced from the initial version and fixed at 0.4.8.

### Cross-Validation Table

| Source | Affected range | Fixed version | Status |
|--------|---------------|---------------|--------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) | No numeric threshold |
| MITRE CVE API | < 0.4.8 | 0.4.8 | Structured, authoritative |
| OSV.dev | introduced: 0, fixed: 0.4.8 | 0.4.8 | Structured, ecosystem-specific |

### Cross-Validation Result

**Agreement**: Both MITRE and OSV.dev agree on the fix threshold:
- Affected: all versions < 0.4.8
- Fixed: >= 0.4.8

The Jira description is imprecise but consistent (it says "versions prior to the fix" which aligns with the external data -- just without a specific version number).

### Enriched Fix Threshold

Since both external sources agree and the Jira description lacks a precise threshold, the external data takes precedence as the authoritative fix threshold:

| Parameter | Value |
|-----------|-------|
| **Enriched fix threshold** | **< 0.4.8** |
| **First fixed version** | **0.4.8** |
| **Confidence** | **High** (two independent external sources agree) |
| **Precedence** | External structured data (MITRE + OSV.dev) over imprecise Jira prose |

This enriched fix threshold will be used in Step 2 (Version Impact Analysis) for all version comparisons.
