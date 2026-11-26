# Step 1.5 – External CVE Data Enrichment: CVE-2026-48901 (h2)

External sources are always queried to cross-check the Jira prose. In this eval the
embedded mock responses from the fixture stand in for live WebFetch calls.

## 1. MITRE CVE API

Source: `https://cveawg.mitre.org/api/cve/CVE-2026-48901` (mock response)

| Field | Value |
|---|---|
| Vendor / product | hyperium / h2 |
| Status | affected |
| `lessThan` | **0.4.8** |
| `versionType` | semver |
| Derived affected range | `< 0.4.8` |
| Derived fixed version | **0.4.8** |

## 2. OSV.dev API

Source: `https://api.osv.dev/v1/vulns/CVE-2026-48901` (mock response)

| Field | Value |
|---|---|
| OSV ID | RUSTSEC-2026-0089 (alias CVE-2026-48901) |
| Ecosystem / package | crates.io / h2 |
| Range type | SEMVER |
| `introduced` | 0 |
| `fixed` | **0.4.8** |
| Derived affected range | `>= 0, < 0.4.8` |
| Derived fixed version | **0.4.8** |

## 3. Cross-validation table

Fix threshold comparison for CVE-2026-48901 (h2):

| Source | Affected range | Fixed version | Precision |
|---|---|---|---|
| Jira description | "versions prior to the fix" | "see advisory" | Imprecise. No numeric threshold. |
| MITRE CVE API | < 0.4.8 | 0.4.8 | Structured (`lessThan`) |
| OSV.dev | >= 0, < 0.4.8 | 0.4.8 | Structured (`introduced`/`fixed` events) |

### Result: Agreement (external sources consistent, Jira has no threshold to contradict them)

- MITRE and OSV.dev agree exactly: affected `< 0.4.8`, fixed in `0.4.8`.
- The Jira description gives no numeric threshold, so it neither conflicts with nor confirms the external data. "Versions prior to the fix" fits `< 0.4.8`. No disagreement prompt is needed.
- Both external APIs answered successfully, so confidence is not degraded.

### Enriched (authoritative) fix threshold passed to Step 2.3

> **h2 affected: `< 0.4.8`; fixed: `>= 0.4.8`**
>
> Boundary semantics: `lessThan` is exclusive. **h2 0.4.8 itself is NOT affected.**
> Any version >= 0.4.8 (e.g., 0.4.8, 0.4.9) is fixed.

Without this enrichment, version impact analysis could not have been performed. The
Jira prose alone does not support any version comparison, and the skill would have had
to stop and ask the engineer for the affected range.

## Step 1.7 – Embargo Check

CVSS is 7.5 (High), which is above the 7.0 trigger. However, **no Embargo policy URL is
configured** in Security Configuration, so the step is skipped silently.
