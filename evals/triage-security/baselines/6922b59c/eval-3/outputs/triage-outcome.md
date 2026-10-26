# Triage Outcome — TC-8003

## Decision: Close as Duplicate

TC-8003 should be **closed as a duplicate** of TC-7999.

## Rationale

TC-7999 is an existing Vulnerability issue for the same CVE (CVE-2026-31812) scoped to the same stream ([rhtpa-2.2] / 2.2.x). It is already in **In Progress** status, meaning triage and remediation work is actively underway. Creating a second parallel triage for the same CVE in the same stream would produce duplicate remediation tasks and conflicting Affects Versions ownership.

### Key Evidence

| Factor | Detail |
|--------|--------|
| Same CVE | Both TC-8003 and TC-7999 carry the label `CVE-2026-31812` |
| Same stream | Both have the summary suffix `[rhtpa-2.2]`, mapping to stream 2.2.x |
| Same component | Both carry `pscomponent:org/rhtpa-server` |
| Sibling status | TC-7999 is In Progress; TC-8003 is New |
| Affects Versions overlap | TC-7999: [RHTPA 2.2.0, RHTPA 2.2.1]; TC-8003: [RHTPA 2.2.0] |

### Version Impact Context

The version impact analysis (performed for completeness before discovering the duplicate) confirms:

- **Affected**: RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (0.11.12), RHTPA 2.2.2 (0.11.12, retag of 2.2.1)
- **Not affected**: RHTPA 2.2.3 (0.11.14), RHTPA 2.2.4 (0.11.14)
- **Fix threshold**: quinn-proto >= 0.11.14

This confirms TC-7999's Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1] are substantively correct (RHTPA 2.2.2 is a retag and may need to be added to TC-7999 separately).

### Cross-Stream Note

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9), but this is outside TC-8003's scope. Cross-stream impact would be handled through TC-7999's triage (Case A) or through a separate PSIRT-created issue for the 2.1.x stream.

## Proposed Jira Actions

The following actions would be executed in interactive mode after engineer confirmation:

1. **Comment on TC-8003**: Document the duplicate finding with version impact evidence
2. **Close TC-8003**: Transition to Closed with resolution "Duplicate"
3. **Add `ai-cve-triaged` label**: Mark TC-8003 as triaged to prevent re-processing

No remediation tasks are created for TC-8003 — TC-7999 owns remediation for this CVE in the 2.2.x stream.

## Items NOT Done (deferred to TC-7999's triage)

- Affects Versions correction (RHTPA 2.2.2 may need to be added to TC-7999)
- Remediation task creation (upstream dependency bump + downstream propagation)
- Cross-stream impact analysis (Case A for 2.1.x stream)
- Release Jira orchestration (Step 7.5)
- Post-triage summary comment with full version impact table
