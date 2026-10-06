# Step 1.5 -- External CVE Data Enrichment

## CVE-2026-48901 (h2)

### 1. MITRE CVE API Response

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

Parsed fields:
- **Product**: h2
- **Vendor**: hyperium
- **Affected version range**: lessThan 0.4.8 (semver)
- **Fix threshold**: 0.4.8

The MITRE CVE record provides a structured `affected[].versions[]` entry with `"lessThan": "0.4.8"` and `"versionType": "semver"`, confirming that all versions below 0.4.8 are affected.

### 2. OSV.dev API Response

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901`

Parsed fields:
- **Package**: h2 (ecosystem: crates.io)
- **Alias**: RUSTSEC-2026-0089
- **Range type**: SEMVER
- **Introduced**: 0 (all versions from the beginning)
- **Fixed**: 0.4.8

The OSV record provides explicit `introduced` and `fixed` version markers confirming the affected range spans from the initial release through 0.4.7 (inclusive), with 0.4.8 as the first fixed version.

### 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|---------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (semver) | 0.4.8 |
| OSV.dev | introduced 0, fixed 0.4.8 | 0.4.8 |

**Result: Agreement.** Both external sources (MITRE and OSV.dev) agree on the fix threshold:

- **Affected range**: all h2 versions < 0.4.8
- **Fixed version**: 0.4.8

The Jira description was imprecise ("versions prior to the fix" / "see advisory") and did not provide a usable numeric threshold. The external CVE databases resolve this ambiguity with structured, machine-readable version constraints.

**Enriched fix threshold for Step 2**: **h2 < 0.4.8** (versions below 0.4.8 are affected; 0.4.8 and above are fixed).

This enriched threshold takes precedence over the Jira description data because it provides precise, cross-validated version constraints from authoritative sources.
