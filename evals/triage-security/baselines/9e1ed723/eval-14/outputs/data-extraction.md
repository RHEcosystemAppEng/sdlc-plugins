# TC-8005 — Step 1: Data Extraction

Mode: **interactive** (Step 0.6 — `FULLSEND_OUTPUT_DIR` not set). Eval run: no Jira MCP,
git, cosign, or WebFetch calls were made. All data comes from the provided mock files.

## Step 0 — Configuration validation

| Item | Value |
|------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | not configured (Steps 4.3 and 7 skipped) |
| Embargo policy URL | not configured (Step 1.7 skipped) |
| ProdSec contact / account ID | not configured |
| Version Streams | 2.1.x → rhtpa-release.0.3.z; 2.2.x → rhtpa-release.0.4.z |
| Source Repositories | rhtpa-backend (no Deployment Context column → defaults to `upstream`) |

All required sections are present (Repository Registry, Jira Configuration, Code
Intelligence, Security Configuration with Product Lifecycle, Version Streams, Source
Repositories). Validation passed.

## Step 0.3 — Matrix staleness check

| Stream | Last-Updated | Age (as of 2026-11-23) | Status |
|--------|--------------|------------------------|--------|
| 2.1.x | 2026-06-28T10:00:00Z | 148 days | STALE (> 14 days) |
| 2.2.x | 2026-06-28T10:00:00Z | 148 days | STALE (> 14 days) |

> Security matrix for stream **2.2.x** was last updated on 2026-06-28 (148 days ago).
> The matrix may not reflect recent releases. Options: 1. Refresh now, 2. Proceed anyway, 3. Stop.

Eval assumption: **Proceed anyway** with the current matrix (no refresh possible offline).
Any 2.2.x release after 2.2.4 would not be covered by this analysis.

## Step 0.8 — Assign and transition (not executed)

Would assign TC-8005 to the current user and transition New → Assigned after
confirmation. Skipped in this eval (no Jira calls).

## Step 1 — Extracted CVE data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8005 | Issue |
| Issue status | New → full triage path | Issue status |
| CVE ID | CVE-2026-40215 | Label `CVE-2026-40215` and summary |
| Affected component | `pscomponent:org/rhtpa-server` → `org/rhtpa-server` | Labels |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` → stream **2.2.x** | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | `versions` field |
| Vulnerable library | openssl-libs | Description |
| Affected version range | versions before 3.0.7-28.el9_4 (`< 3.0.7-28.el9_4`) | Description |
| Fixed version | 3.0.7-28.el9_4 | Description |
| CVSS | 7.1 (High) | Description |
| Vulnerable code path | `X509_verify_cert()` — SAN extension length not validated | Description |
| Upstream fix PR | none (no GitHub PR remote link) | Remote links |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (RHSA-2026:4021) | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 | Remote links |
| Due date | 2026-08-15 (already past as of 2026-11-23) | `duedate` |
| Assignee | Unassigned | Issue |
| Existing comments | none | Comment history |

All critical fields (CVE ID, library, affected range) were parsed. No engineer input needed.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` → stream `2.2.x`, which matches the configured Version Stream
  `2.2.x` (git.example.com/rhtpa/rhtpa-release.0.4.z).
- **Issue stream scope: 2.2.x (scoped).** Steps 3–8 apply to 2.2.x only. Other streams
  (2.1.x) are reported as cross-stream impact (Case A).

### Ecosystem detection

- Library `openssl-libs` is a system package in the container image → ecosystem **RPM**.
- RPM is listed in the 2.2.x Ecosystem Mappings with lock file `rpms.lock.yaml`
  (check command `git show <tag>:rpms.lock.yaml`).
- Category: **System package** → **1 remediation task per stream** (Konflux release repo fix).
- Investigation method: rpms.lock.yaml + SBOM verification (cosign available).

### Deployment context

- Component `org/rhtpa-server` is not in the Source Repositories table (only
  `rhtpa-backend` is listed). Defaulting to deployment context **`upstream`**.

## Step 1.5 — External CVE data enrichment

MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-40215`) and OSV.dev
(`https://api.osv.dev/v1/vulns/CVE-2026-40215`) were not queried (eval forbids
external calls), so both count as unavailable.

> ⚠ External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 3.0.7-28.el9_4 | 3.0.7-28.el9_4 |
| MITRE CVE API | unavailable | unavailable |
| OSV.dev | unavailable | unavailable |

**Fix threshold used for Step 2:** `3.0.7-28.el9_4` (RPM EVR comparison).

## Step 1.7 — Embargo check

No Embargo policy URL is configured → skipped silently (CVSS 7.1 would otherwise
trigger the gate).
