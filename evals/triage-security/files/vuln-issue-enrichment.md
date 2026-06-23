<!-- SYNTHETIC TEST DATA — Vulnerability issue with imprecise Jira description for external CVE enrichment eval testing -->

# Mock Jira Vulnerability Issue

**Key**: TC-8030
**Summary**: CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-48901, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.2.0
**Due Date**: 2026-08-01
**Assignee**: Unassigned

## Remote Links

- [GHSA-2026-r7f2-kk9p](https://github.com/advisories/GHSA-2026-r7f2-kk9p) — GitHub Advisory
- [CVE-2026-48901](https://www.cve.org/CVERecord?id=CVE-2026-48901) — CVE Record
- [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) — Upstream fix PR

## Comments

_(no comments)_

---

## Description

A vulnerability was found in h2. The h2 crate is affected by an HTTP/2 CONTINUATION flood vulnerability. An attacker can send a large number of CONTINUATION frames that causes excessive memory allocation and CPU usage.

**Affected package**: h2
**Affected versions**: versions prior to the fix
**Fixed version**: see advisory
**CVSS**: 7.5 (High)

The vulnerability exists because h2 does not limit the number of CONTINUATION frames that can follow a HEADERS frame. An attacker can exploit this to cause a denial of service.

### References

- https://github.com/advisories/GHSA-2026-r7f2-kk9p
- https://rustsec.org/advisories/RUSTSEC-2026-0089.html

## External CVE Data (mock responses for eval)

### MITRE CVE API Response (https://cveawg.mitre.org/api/cve/CVE-2026-48901)

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

### OSV.dev API Response (https://api.osv.dev/v1/vulns/CVE-2026-48901)

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
