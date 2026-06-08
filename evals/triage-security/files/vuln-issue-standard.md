<!-- SYNTHETIC TEST DATA — standard Vulnerability issue with wrong Affects Versions for triage-security eval testing -->

# Mock Jira Vulnerability Issue

**Key**: TC-8001
**Summary**: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-31812, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.0.0
**Due Date**: 2026-07-15
**Assignee**: Unassigned

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) — GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) — CVE Record
- [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) — Upstream fix PR

## Comments

_(no comments)_

---

## Description

A vulnerability was found in quinn-proto. The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This vulnerability is classified as a denial of service (DoS).

**Affected package**: quinn-proto
**Affected versions**: versions before 0.11.14
**Fixed version**: 0.11.14
**CVSS**: 7.5 (High)

The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits.

### References

- https://github.com/advisories/GHSA-2026-qp73-x4mq
- https://rustsec.org/advisories/RUSTSEC-2026-0042.html
