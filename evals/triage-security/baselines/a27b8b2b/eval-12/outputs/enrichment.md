# Step 1.5 -- External CVE Data Enrichment

The Jira description for TC-8030 lacks a precise fix threshold ("versions prior to the fix", "see advisory"). External CVE databases are queried to obtain structured version range data.

## 1. MITRE CVE API

**Query**: `WebFetch(url: "https://cveawg.mitre.org/api/cve/CVE-2026-48901")`

**Response** (from mock data embedded in fixture):

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

**Extracted data**:
- Product: h2 (vendor: hyperium)
- Affected range: versions < **0.4.8** (lessThan, semver)
- Fix threshold: **0.4.8**

## 2. OSV.dev API

**Query**: `WebFetch(url: "https://api.osv.dev/v1/vulns/CVE-2026-48901")`

**Response** (from mock data embedded in fixture):

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

**Extracted data**:
- Package: h2 (ecosystem: crates.io)
- Introduced: 0 (all versions from the beginning)
- Fixed: **0.4.8**
- Fix threshold: **0.4.8**

## 3. Cross-Validation

| Source | Affected range | Fixed version |
|--------|---------------|---------------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (imprecise) |
| MITRE CVE API | < 0.4.8 (lessThan, semver) | 0.4.8 |
| OSV.dev | introduced: 0, fixed: 0.4.8 | 0.4.8 |

**Result: AGREEMENT**

Both MITRE CVE API and OSV.dev agree on the fix threshold: **0.4.8**. The Jira description provided no precise version data, but both external sources independently confirm the same threshold.

### Enriched Fix Threshold

**Authoritative fix threshold: 0.4.8**

This value is used as the authoritative fix threshold for Step 2.3 version impact comparisons. The external data takes precedence because it provides machine-readable version constraints (lessThan 0.4.8 / fixed 0.4.8) rather than the imprecise prose in the Jira description ("versions prior to the fix").

Versions of h2 **less than 0.4.8** are affected. Versions **>= 0.4.8** are NOT affected.
