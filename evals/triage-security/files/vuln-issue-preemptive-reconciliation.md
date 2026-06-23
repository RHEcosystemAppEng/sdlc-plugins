<!-- SYNTHETIC TEST DATA — CVE Jira arrives for a stream that already has a preemptive remediation task -->

# Mock Jira Vulnerability Issue

**Key**: TC-8021
**Summary**: CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-55123, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.1.0, RHTPA 2.1.1
**Due Date**: 2026-08-15
**Assignee**: Unassigned

## Custom Fields

- **customfield_10632** (Upstream Affected Component): tokio
- **customfield_10669** (PS Component): pscomponent:org/rhtpa-server
- **customfield_10832** (Stream): rhtpa-2.1

## Issue Links

_(no existing links)_

## Remote Links

- [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) — GitHub Advisory
- [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) — CVE Record
- [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) — Upstream fix PR

## Comments

_(no comments)_

---

## Description

A vulnerability was found in the tokio crate. Versions of tokio before 1.42.0 are vulnerable to a use-after-free when a spawned task is aborted while holding a borrowed reference. This can lead to memory corruption and potential code execution.

**Affected package**: tokio
**Affected versions**: versions before 1.42.0
**Fixed version**: 1.42.0
**CVSS**: 8.1 (High)

This issue is scoped to stream [rhtpa-2.1]. A proactive remediation task (TC-8022) already exists for this stream, created by a prior cross-stream triage of TC-8020 (stream [rhtpa-2.2]).

### Existing preemptive task (provided by Step 4.4 JQL search)

A JQL search for `labels = 'security-preemptive' AND labels = 'CVE-2026-55123'` returns:

- **TC-8022** — Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
  - **Status**: Open
  - **Labels**: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
  - **Issue Links**:
    - **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

### References

- https://github.com/advisories/GHSA-2026-tk91-v5pp
- https://rustsec.org/advisories/RUSTSEC-2026-0088.html
