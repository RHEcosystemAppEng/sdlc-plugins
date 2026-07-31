# Step 1.5 -- External CVE Data Enrichment

The Jira description for CVE-2026-48901 provides imprecise version data ("versions prior to the fix" / "see advisory"). Querying external CVE databases to obtain a precise fix threshold.

## 1. MITRE CVE API

**Query**: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Response** (parsed):

The MITRE CVE record contains an `affected` entry for product `h2` by vendor `hyperium`. The `versions` array specifies:

- `status`: affected
- `lessThan`: **0.4.8**
- `versionType`: semver

**Extracted fix threshold from MITRE**: `< 0.4.8` (all versions below 0.4.8 are affected; 0.4.8 is the fix version).

## 2. OSV.dev API

**Query**: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Response** (parsed):

The OSV record (RUSTSEC-2026-0089) contains an `affected` entry for package `h2` in the `crates.io` ecosystem. The `ranges` array contains a SEMVER range with events:

- `introduced`: 0 (all versions from the beginning)
- `fixed`: **0.4.8**

**Extracted fix threshold from OSV.dev**: fixed at **0.4.8** (versions from 0 up to but not including 0.4.8 are affected).

## 3. Cross-Validation

| Source | Affected Range | Fixed Version |
|--------|---------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (lessThan field) | 0.4.8 |
| OSV.dev | introduced: 0, fixed: 0.4.8 | 0.4.8 |

**Result: Agreement.** Both MITRE CVE API and OSV.dev agree on the fix threshold: **0.4.8**. The Jira description data is imprecise and does not specify a version number, but the external sources provide a consistent, machine-readable fix threshold.

**Enriched fix threshold**: **0.4.8** (authoritative, from cross-validated external sources)

This enriched fix threshold (0.4.8) will be used as the authoritative value for version impact comparisons in Step 2.3, replacing the imprecise Jira description data. Versions shipping h2 < 0.4.8 are affected; versions shipping h2 >= 0.4.8 are not affected.
