# TC-8001 — Data Extraction

> Eval simulation: no Jira MCP, REST API, `git show`, or WebFetch calls were made.
> Every Jira operation in this file is a **proposed** action that needs engineer
> confirmation. None of them has been performed.

## Pre-flight (Steps 0 – 0.6)

| Step | Result |
|------|--------|
| 0 – Validate configuration | PASS. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present in `claude-md-security-config.md`. |
| Extracted config | Jira version prefix `RHTPA`, Vulnerability issue type ID `10024`, Component label pattern `pscomponent:`, Product pages URL `https://access.example.com/product-life-cycle/rhtpa`, VEX Justification field `customfield_12345` |
| Optional config **not** set | Upstream Affected Component field, PS Component field, Stream field (so Steps 4.3, 7 and 7.5.3 dedup are skipped). ProdSec contact email and ProdSec Jira account ID are also unset (no @mentions). Embargo policy URL is unset (Step 1.7 skipped). The Source Repositories table has no Deployment Context column. |
| 0.3 – Matrix staleness | **WARNING.** `security-matrix-mock.md` has `Last-Updated: 2026-06-28T10:00:00Z`, which is **128 days** before today (2026-11-03) and over the 14-day threshold. The engineer must pick one: 1. Refresh now, 2. Proceed anyway, or 3. Stop. *For this eval the analysis continues as if "Proceed anyway" were chosen, so releases after 2026-06-28 may be missing from the impact table.* |
| 0.5 – Jira access | Not initialized (eval: no external calls). |
| 0.6 – Fullsend mode detection | `FULLSEND_OUTPUT_DIR` is absent, so this is **interactive mode**. |
| 0.7 – Load trusted Fullsend input | Skipped (interactive mode only uses this in Fullsend). |

## Step 0.7 early assignment: assign TC-8001 and transition to Assigned (PROPOSED, not performed)

The task calls this "Step 0.7 early assignment". In the current SKILL.md it is numbered **Step 0.8 – Assign and Transition to Assigned**, because 0.7 is the Fullsend trusted-input load, which is skipped here. It runs before data extraction so that Step 7 (Concurrent Triage Detection) can see who is actively triaging the issue.

Proposed sequence, which needs engineer confirmation before any of it runs:

1. **Get the current user's Jira account ID:** `jira.user_info()` returns `<current-user-account-id>`.
2. **Assign TC-8001 to the current user:**
   `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)`. The current assignee is *Unassigned*.
3. **Find the transition dynamically:** `jira.get_transitions("TC-8001")`, then pick the transition whose **target status name is "Assigned"**. No transition ID or name is hardcoded, because Vulnerability issues use a different workflow from Tasks.
4. **Transition to Assigned:** current status is **New**, so the transition applies:
   `jira.transition_issue("TC-8001", <assigned-transition-id>)`.
   If the issue were already Assigned or in a later status, this step would be skipped silently and the assignment would still go ahead.

Status-aware handling: the issue is in **New**, so full triage follows the default path with no warning.

## Step 1 — Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| Issue key | TC-8001 | Issue |
| Issue type / status | Vulnerability / New | Issue |
| CVE ID | **CVE-2026-31812** | Label `CVE-2026-31812` and summary text |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | Issue summary |
| Affected component | `pscomponent:org/rhtpa-server` gives `org/rhtpa-server` | Label matching `pscomponent:` |
| Product version (PSIRT-claimed) | `rhtpa-2.2` | Summary bracket suffix |
| Affects Versions (Jira field) | **RHTPA 2.0.0** | Jira `versions` field |
| Vulnerable library | **quinn-proto** | Description |
| Affected version range | **< 0.11.14** ("versions before 0.11.14") | Description |
| Fixed version | **0.11.14** | Description |
| CVSS / severity | 7.5 (High), DoS | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq (also RUSTSEC-2026-0042: https://rustsec.org/advisories/RUSTSEC-2026-0042.html) | Remote links and description references |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 (already past as of 2026-11-03) | Issue `duedate` |
| Assignee (before Step 0.8) | Unassigned | Issue |
| Existing comments | None | Comment history |
| Reporter | Not present in the mock issue. Step 1 must capture it from `jira.get_issue` for the mandatory @mention in the post-triage summary. | — |

All critical fields (CVE ID, library, affected range) parsed successfully, so there is no need to stop for engineer input.

### Stream scope resolution

- Suffix `[rhtpa-2.2]` maps to the configured Version Stream **2.2.x** (`git.example.com/rhtpa/rhtpa-release.0.4.z`).
- **Issue stream scope: 2.2.x (scoped).** Steps 3 and 8 limit standard corrections and remediation to 2.2.x. Other affected streams are handled through Case A, the cross-stream path.

### Ecosystem detection

- `quinn-proto` is a Rust crate, and the backend repository (`rhtpa-backend`, rust-analyzer) uses `Cargo.lock`.
- **Ecosystem: Cargo.** Both streams list it in their Ecosystem Mappings table, with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.
- Classification: **source dependency**, so each affected stream gets **2 remediation tasks** (upstream backport or dependency bump, plus downstream propagation).

### Deployment context lookup

- The affected repository is `rhtpa-backend` (the matrix `backend` column, the Rust backend service).
- The Source Repositories table has **no Deployment Context column**. Step 1 defaults the context to `upstream` for recordkeeping. Under the backward-compatibility rule in `remediation-templates.md`, the Coordination Guidance subsection is **omitted** from the task descriptions.

## Step 1.5 — External CVE Data Enrichment

The MITRE (`https://cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev (`https://api.osv.dev/v1/vulns/CVE-2026-31812`) lookups were **not queried**, because the eval forbids external calls. Following the "Unavailable" rule:

> External CVE databases unavailable — using Jira description data only.
> Fix threshold confidence is reduced.

**Fix threshold used for Step 2: quinn-proto < 0.11.14 (fixed in 0.11.14)**, from the Jira description.

## Step 1.7 — Embargo Check

No Embargo policy URL is configured, so this step is **skipped silently**, even though CVSS 7.5 meets the >= 7.0 trigger.
