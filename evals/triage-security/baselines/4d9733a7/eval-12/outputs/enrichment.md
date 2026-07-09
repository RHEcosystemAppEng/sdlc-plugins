# Step 1.5 -- External CVE Data Enrichment

The Jira description for TC-8030 (CVE-2026-48901) lacks a precise fix threshold. The affected versions field states "versions prior to the fix" with no specific version number, and the fixed version says "see advisory." Step 1.5 queries external CVE databases to obtain structured version range data.

## 1. MITRE CVE API

**Query:** `https://cveawg.mitre.org/api/cve/CVE-2026-48901`

**Response (mock):**
```json
{
  "cveMetadata": {"cveId": "CVE-2026-48901"},
  "containers": {
    "cna": {
      "affected": [{
        "product": "h2",
        "vendor": "hyperium",
        "versions": [{
          "status": "affected",
          "lessThan": "0.4.8",
          "versionType": "semver"
        }]
      }]
    }
  }
}
```

**Extracted data:**
- Product: h2
- Vendor: hyperium
- Affected range: `lessThan` **0.4.8** (semver)
- Fix threshold: **0.4.8**

## 2. OSV.dev API

**Query:** `https://api.osv.dev/v1/vulns/CVE-2026-48901`

**Response (mock):**
```json
{
  "id": "RUSTSEC-2026-0089",
  "aliases": ["CVE-2026-48901"],
  "affected": [{
    "package": {"ecosystem": "crates.io", "name": "h2"},
    "ranges": [{
      "type": "SEMVER",
      "events": [
        {"introduced": "0"},
        {"fixed": "0.4.8"}
      ]
    }]
  }]
}
```

**Extracted data:**
- Package: h2 (crates.io ecosystem)
- Introduced: 0 (all versions from inception)
- Fixed: **0.4.8**
- Fix threshold: **0.4.8**

## 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | lessThan 0.4.8 | 0.4.8 |
| OSV.dev | introduced: 0, fixed: 0.4.8 | 0.4.8 |

**Result: Agreement.** Both MITRE CVE API and OSV.dev report the same fix threshold: **0.4.8**. The external sources agree and provide a precise, machine-readable version constraint.

**Enriched fix threshold: 0.4.8** (authoritative value for Step 2.3 comparisons)

This enriched threshold replaces the imprecise Jira description data ("versions prior to the fix") for all subsequent version impact analysis.
