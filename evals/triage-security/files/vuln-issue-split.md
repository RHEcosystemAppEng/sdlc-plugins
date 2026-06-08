<!-- SYNTHETIC TEST DATA — unscoped Vulnerability issue requiring stream-targeted remediation for triage-security eval testing -->

# Mock Jira Vulnerability Issue

**Key**: TC-8004
**Summary**: CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-33501, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.1.0, RHTPA 2.2.0
**Due Date**: 2026-08-01
**Assignee**: Unassigned

## Remote Links

- [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) — GitHub Advisory
- [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) — CVE Record
- [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) — Upstream fix PR

## Comments

_(no comments)_

---

## Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server.

**Affected package**: h2
**Affected versions**: versions before 0.4.8
**Fixed version**: 0.4.8
**CVSS**: 7.5 (High)

This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood) — this CVE specifically affects the Rust h2 library's header accumulation logic. The fix adds a configurable maximum header list size that defaults to 16 KiB.

Note: This issue has NO stream suffix in the summary — it is unscoped and covers all streams. The version impact analysis should check all streams and create remediation only for actually affected streams.

### References

- https://github.com/advisories/GHSA-2026-kv8p-r3n7
- https://rustsec.org/advisories/RUSTSEC-2026-0055.html
