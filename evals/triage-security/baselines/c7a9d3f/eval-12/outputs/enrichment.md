# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Extracted data from `containers.cna.affected[].versions[]`:

| Field | Value |
|-------|-------|
| Product | h2 |
| Vendor | hyperium |
| Status | affected |
| Version constraint | lessThan 0.4.8 |
| Version type | semver |

**Fix threshold from MITRE**: versions less than **0.4.8** are affected. Version 0.4.8 is the first fixed version.

### OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Extracted data from `affected[].ranges[].events`:

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 |
| Aliases | CVE-2026-48901 |
| Package ecosystem | crates.io |
| Package name | h2 |
| Introduced | 0 (all versions from the beginning) |
| Fixed | 0.4.8 |

**Fix threshold from OSV.dev**: fixed at version **0.4.8**.

### Cross-Validation Table

| Source | Affected range | Fixed version | Precision |
|--------|---------------|---------------|-----------|
| Jira description | "versions prior to the fix" | "see advisory" | IMPRECISE -- no specific version threshold |
| MITRE CVE API | < 0.4.8 (semver lessThan) | 0.4.8 | PRECISE -- structured semver constraint |
| OSV.dev | introduced at 0, fixed at 0.4.8 | 0.4.8 | PRECISE -- structured range events |

### Cross-Validation Result: AGREEMENT

Both MITRE CVE API and OSV.dev agree on the fix threshold:

- **MITRE**: `lessThan: 0.4.8` (versions below 0.4.8 are affected)
- **OSV.dev**: `fixed: 0.4.8` (version 0.4.8 is the fix)

The Jira description was imprecise ("versions prior to the fix" / "see advisory") and could not provide a usable version threshold on its own. The external sources resolve this ambiguity.

### Enriched Fix Threshold

**Authoritative fix threshold: 0.4.8**

This enriched value (from cross-validated external CVE data) supersedes the imprecise Jira description and will be used as the comparison baseline in Step 2.3 for version impact analysis. All h2 versions < 0.4.8 are considered affected; versions >= 0.4.8 are not affected.
