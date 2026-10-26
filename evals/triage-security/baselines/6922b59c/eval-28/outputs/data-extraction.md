# Step 1 -- Data Extraction

## Issue: TC-8060

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | **2.2.x** (scoped -- mapped from `[rhtpa-2.2]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |
| CVE record URL | [CVE-2026-99010](https://www.cve.org/CVERecord?id=CVE-2026-99010) |
| Advisory URL | -- (none provided) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Status | New |
| Existing comments | None |

## Ecosystem Detection

| Property | Value |
|----------|-------|
| Ecosystem | Cargo |
| Category | Source dependency |
| Lock file | `Cargo.lock` |
| Check command | `git show <tag>:Cargo.lock \| grep -A2 'name = "h2"'` |
| Upstream branch | `release/0.4.z` |
| Tasks per stream | 2 (dependency bump + downstream propagation) |

## Vulnerability Summary

A vulnerability was found in h2. The h2 crate before version 0.4.5 allows a
remote attacker to cause memory exhaustion by sending a large number of
CONTINUATION frames. This vulnerability is classified as a denial of service
(DoS). The vulnerability exists because h2 does not properly limit the number
of CONTINUATION frames that can be received for a single HEADERS frame,
allowing an attacker to send an unbounded sequence that consumes server memory.

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** stream in the Version Streams configuration table. Triage is scoped
to this stream only. Cross-stream impact on 2.1.x will be checked in Case A
analysis.
