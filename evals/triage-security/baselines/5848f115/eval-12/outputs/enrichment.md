# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### 1. MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed structured data:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Product | h2 |
| Vendor | hyperium |
| Affected range | lessThan 0.4.8 |
| Version type | semver |

The MITRE CVE record provides a precise affected version range: all semver
versions **less than 0.4.8** are affected. This means version 0.4.8 is the
fix boundary.

### 2. OSV.dev API Response

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

The OSV.dev record confirms the fix version is **0.4.8**, with all prior
versions affected from the initial release.

### 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Result: Agreement.** MITRE and OSV.dev both report the fix threshold as
**0.4.8**. The Jira description is imprecise ("versions prior to the fix" /
"see advisory") but does not contradict the external sources -- it simply
lacks a concrete version number.

The external data provides machine-readable version constraints and takes
precedence over the prose-parsed Jira description.

### Enriched Fix Threshold

**Fix threshold: < 0.4.8** -- any h2 version below 0.4.8 is vulnerable.
Version 0.4.8 and above are not affected.

This enriched fix threshold is used in Step 2.3 for version impact comparisons.
