# Triage Outcome: TC-8021 -- CVE-2026-55123 tokio Use-after-free

## Summary

TC-8021 is a PSIRT-created Vulnerability issue for **CVE-2026-55123** (tokio use-after-free, versions before 1.42.0), scoped to stream **2.1.x** via the `[rhtpa-2.1]` suffix. Triage determined that a preemptive remediation task (**TC-8022**) already exists for this CVE and stream, created during the prior cross-stream triage of TC-8020 (stream 2.2.x). The preemptive task was reconciled to become a standard remediation task linked to TC-8021.

## Step-by-Step Triage Walkthrough

### Step 0 -- Configuration Validation

Project configuration validated from CLAUDE.md:
- Project key: **TC**
- Cloud ID: **2b9e35e3-6bd3-4cec-b838-f4249ee02432**
- Jira version prefix: **RHTPA**
- Vulnerability issue type ID: **10024**
- Product pages URL: **https://access.example.com/product-life-cycle/rhtpa**
- Component label pattern: **pscomponent:**
- VEX Justification custom field: **customfield_12345**
- Upstream Affected Component field: **customfield_10632**
- PS Component field: **customfield_10669**
- Stream field: **customfield_10832**
- Version Streams: 2.1.x, 2.2.x configured with Konflux release repos
- Source Repositories: rhtpa-backend configured

All required sections present. Proceeding.

### Step 1 -- Data Extraction

Extracted from TC-8021:
- **CVE**: CVE-2026-55123
- **Library**: tokio (Cargo/Rust ecosystem)
- **Affected range**: versions before 1.42.0
- **Fixed version**: 1.42.0
- **Stream scope**: 2.1.x (from suffix `[rhtpa-2.1]`)
- **PSIRT Affects Versions**: RHTPA 2.1.0, RHTPA 2.1.1
- **Upstream fix**: tokio-rs/tokio#7001

### Step 2 -- Version Impact Analysis

Stream 2.1.x supportability matrix covers versions 2.1.0 (tag `v0.3.8`) and 2.1.1 (tag `v0.3.12`). Both versions ship tokio at a version below 1.42.0 (confirmed by the prior cross-stream analysis from TC-8020 triage that led to TC-8022 creation).

| Version | tokio | Affected? | Notes |
|---------|-------|-----------|-------|
| 2.1.0 | < 1.42.0 | YES | Confirmed by prior cross-stream analysis |
| 2.1.1 | < 1.42.0 | YES | Confirmed by prior cross-stream analysis |

### Step 3 -- Affects Versions Correction

PSIRT-assigned Affects Versions: **RHTPA 2.1.0, RHTPA 2.1.1**

This issue is scoped to stream 2.1.x. The version impact table confirms both 2.1.0 and 2.1.1 are affected. The PSIRT assignment is **correct and complete** for this stream. No correction needed.

### Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

#### Step 4.1/4.2 -- Sibling Detection

A JQL search for other Vulnerability issues with label `CVE-2026-55123`:
- **TC-8020** (stream `[rhtpa-2.2]`) -- different-stream sibling (companion tracker). This is the originating CVE Jira from which TC-8022 was proactively created.

PROPOSED: Link TC-8021 to TC-8020 as "Related" (cross-stream companions, not duplicates).

#### Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component, PS Component, and Stream custom fields are all configured. A search for other CVE Jiras with `customfield_10632 ~ 'tokio'` in stream `rhtpa-2.1` would identify any other CVEs whose remediation already covers tokio >= 1.42.0. No additional overlap data was provided in the fixture, so this step proceeds without findings.

#### Step 4.4 -- Preemptive Task Reconciliation (KEY FINDING)

JQL search: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'`

**Result**: TC-8022 found -- "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

**Stream match**: TC-8022 summary contains `(rhtpa-2.1)`, which matches TC-8021's stream scope of 2.1.x.

**Reconciliation actions (PROPOSED)**:

1. **Link TC-8021 to TC-8022 with "Depend"** -- establishes the standard CVE-to-remediation dependency
2. **Remove `security-preemptive` label from TC-8022** -- updated labels become `[ai-generated-jira, Security, CVE-2026-55123]`
3. **Record that remediation exists** for stream 2.1.x -- Step 7 will skip task creation

The "Related" link between TC-8022 and TC-8020 is preserved for audit trail purposes.

### Step 5 -- Version Lifecycle Check

PROPOSED: Fetch the product lifecycle page at https://access.example.com/product-life-cycle/rhtpa to verify that versions 2.1.0 and 2.1.1 are still within support. (No lifecycle data provided in fixture; in a real triage, this would be checked before proceeding.)

### Step 6 -- Already Fixed Check

Sibling TC-8020 (stream 2.2.x) -- check its status. No fixture data indicates it is resolved, so no already-fixed scenario applies for TC-8021's stream (2.1.x). Proceed to Step 7.

### Step 7 -- Remediation

**Outcome**: No new remediation tasks need to be created.

Step 4.4 reconciliation determined that TC-8022 already covers remediation for CVE-2026-55123 in the 2.1.x stream. The task targets the correct library (tokio), correct fixed version (1.42.0), and correct stream (rhtpa-2.1). It has been promoted from preemptive to standard remediation by:
- Linking it to TC-8021 with "Depend"
- Removing the `security-preemptive` label

This falls under a reconciliation-modified version of **Case A (Affected)**: the stream is affected, but the remediation task already exists from a prior proactive creation. No duplicate task is created.

## Post-Triage Summary

### PROPOSED: Add `ai-cve-triaged` label to TC-8021

```
PROPOSED: jira.edit_issue("TC-8021", fields={
  "labels": ["CVE-2026-55123", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### PROPOSED: Post summary comment to TC-8021

```
PROPOSED: jira.add_comment("TC-8021", comment-md:

## CVE Triage Summary -- TC-8021

**CVE**: CVE-2026-55123 (tokio use-after-free, versions before 1.42.0)
**Stream**: 2.1.x (scoped via [rhtpa-2.1] suffix)
**Ecosystem**: Cargo (Rust)

### Version Impact

| Version | tokio | Affected? | Notes |
|---------|-------|-----------|-------|
| 2.1.0 | < 1.42.0 | YES | |
| 2.1.1 | < 1.42.0 | YES | |

### Affects Versions

No correction needed. PSIRT-assigned versions (RHTPA 2.1.0, RHTPA 2.1.1) are correct.

### Preemptive Task Reconciliation

Existing preemptive remediation task TC-8022 was found for this CVE and stream.
Originally created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2]).

Actions:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022
- TC-8022 is now a standard remediation task for this CVE Jira
- No new remediation tasks created

### Companion Issues

| Issue | Stream | Role |
|-------|--------|------|
| TC-8020 | 2.2.x | Cross-stream companion (CVE Jira) |
| TC-8022 | 2.1.x | Remediation task (reconciled from preemptive) |

---
_Triaged by triage-security skill_
)
```

### PROPOSED: Assign TC-8021

```
PROPOSED: Assign TC-8021 to current user
```

### PROPOSED: Transition TC-8021 to In Progress

```
PROPOSED: Transition TC-8021 to "In Progress" (pending confirmation of remediation task status)
```

## Final State

| Item | Before Triage | After Triage (Proposed) |
|------|---------------|-------------------------|
| **TC-8021 status** | New | In Progress |
| **TC-8021 labels** | CVE-2026-55123, pscomponent:org/rhtpa-server | CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged |
| **TC-8021 Affects Versions** | RHTPA 2.1.0, RHTPA 2.1.1 | RHTPA 2.1.0, RHTPA 2.1.1 (no change) |
| **TC-8021 links** | (none) | Depend: TC-8022; Related: TC-8020 |
| **TC-8022 labels** | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | ai-generated-jira, Security, CVE-2026-55123 |
| **TC-8022 links** | Related: TC-8020 | Related: TC-8020; Depend from: TC-8021 |
| **New tasks created** | -- | None (TC-8022 reconciled) |
