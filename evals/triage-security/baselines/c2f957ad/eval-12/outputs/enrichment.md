# Step 1.5 – External CVE Data Enrichment: CVE-2026-48901 (h2)

External sources are always queried. In this eval the mock responses embedded in
`vuln-issue-enrichment.md` stand in for live WebFetch calls.

## 1. MITRE CVE API

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901` (mock response)

| Field | Value |
|-------|-------|
| Vendor / product | hyperium / h2 |
| Status | affected |
| `lessThan` | **0.4.8** |
| `versionType` | semver |
| Derived affected range | `< 0.4.8` |
| Derived fixed version | **0.4.8** |

## 2. OSV.dev API

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901` (mock response)

| Field | Value |
|-------|-------|
| OSV ID | RUSTSEC-2026-0089 (alias CVE-2026-48901) |
| Ecosystem / package | crates.io / h2 |
| Range type | SEMVER |
| `introduced` | 0 |
| `fixed` | **0.4.8** |
| Derived affected range | `>= 0, < 0.4.8` |
| Derived fixed version | **0.4.8** |

## 3. Cross-validation

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version | Notes |
|--------|----------------|---------------|-------|
| Jira description | "versions prior to the fix" (imprecise) | "see advisory" (not stated) | Prose only, no numeric threshold |
| MITRE CVE API | < 0.4.8 | 0.4.8 | `lessThan: 0.4.8`, semver |
| OSV.dev | >= 0, < 0.4.8 | 0.4.8 | `introduced: 0`, `fixed: 0.4.8` |

**Result: Agreement.** MITRE and OSV.dev give the same threshold (fixed in 0.4.8).
The Jira description does not contradict them: "versions prior to the fix" fits
`< 0.4.8`. It just has no numeric value. With no conflicting threshold, the
engineer does not need to pick between sources.

**Authoritative (enriched) fix threshold for Step 2.3: `h2 < 0.4.8` is affected; `h2 >= 0.4.8` is fixed.**

The external structured data takes precedence because it gives machine-readable
semver constraints. Here it also fills a gap: without enrichment, the Jira
description alone could not support any version comparison (a critical field
would be missing and triage would have to stop).

- External API availability: both available. Confidence is not degraded.
- Severity: CVSS 7.5 (High / Important). Step 1.7 Embargo Check would trigger at
  >= 7.0, but no Embargo policy URL is configured, so Step 1.7 is skipped.
