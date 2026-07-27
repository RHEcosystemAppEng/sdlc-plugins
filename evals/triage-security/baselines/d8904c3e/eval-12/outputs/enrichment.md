# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed data:
- Product: h2
- Vendor: hyperium
- Affected versions: lessThan **0.4.8** (semver)
- Status: affected

The MITRE CVE record provides a structured `lessThan` constraint indicating all versions below 0.4.8 are affected.

### OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed data:
- ID: RUSTSEC-2026-0089
- Aliases: CVE-2026-48901
- Package: h2 (ecosystem: crates.io)
- Affected range: introduced at **0**, fixed at **0.4.8** (SEMVER)

The OSV.dev record provides explicit `introduced` and `fixed` event markers confirming the affected range.

### Cross-Validation Table

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 | 0.4.8 |
| OSV.dev | >= 0, < 0.4.8 | 0.4.8 |

### Analysis

- **MITRE and OSV.dev agree**: both external sources report the fix threshold as **0.4.8**. Versions < 0.4.8 are affected; versions >= 0.4.8 are not affected.
- **Jira description is imprecise**: the description says "versions prior to the fix" and "see advisory" without specifying concrete version numbers. This is insufficient for version impact analysis.
- **Resolution**: the external sources provide machine-readable version constraints that agree with each other. The enriched fix threshold of **0.4.8** is used as the authoritative value for Step 2 version impact comparisons.

### Enriched Fix Threshold

**Fix threshold: 0.4.8** (from cross-validated MITRE CVE API and OSV.dev data)

- Affected: h2 < 0.4.8
- Not affected: h2 >= 0.4.8
