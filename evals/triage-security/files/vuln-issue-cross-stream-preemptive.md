<!-- SYNTHETIC TEST DATA — scoped Vulnerability issue where cross-stream analysis reveals another stream is affected but has no CVE Jira -->

# Mock Jira Vulnerability Issue

**Key**: TC-8020
**Summary**: CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-55123, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1
**Due Date**: 2026-08-15
**Assignee**: Unassigned

## Custom Fields

- **customfield_10632** (Upstream Affected Component): tokio
- **customfield_10669** (PS Component): pscomponent:org/rhtpa-server
- **customfield_10832** (Stream): rhtpa-2.2

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

The issue is scoped to stream [rhtpa-2.2]. However, cross-stream version impact analysis reveals that stream rhtpa-2.1 also ships tokio < 1.42.0. No sibling CVE Jira exists for the rhtpa-2.1 stream.

### Cross-stream version impact (provided by Step 2 analysis)

| Version     | Stream    | tokio version | Affected? |
|-------------|-----------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |

### Sibling CVE Jiras (provided by Step 4 JQL search)

No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

### References

- https://github.com/advisories/GHSA-2026-tk91-v5pp
- https://rustsec.org/advisories/RUSTSEC-2026-0088.html
