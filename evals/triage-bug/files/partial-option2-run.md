<!-- SYNTHETIC TEST DATA — State left behind by a triage-bug run that selected Step 4.6 option 2 and stopped part-way, for eval testing -->

# Mock Jira: Prior Triage Run State for ACME-530

**Bug**: ACME-530
**Status**: New

---

## Existing linked issues

### ACME-540 — Task

**Summary**: Add an explicit ORDER BY to the advisories() query in acme-data-client
**Labels**: ai-generated-jira
**Repository**: acme-data-client
**Link**: Blocks ACME-530 (added by the prior run right after this Task's digest)

**Description digest** (posted as an ACME-540 comment by the prior run):

> Description digest — sha256:9f2c1e… (ACME-540). Repository acme-data-client.
> Fix location: root cause. Acceptance criteria unchanged since posting.

## What the prior run completed

1. Root Cause Layer Check classified the owning layer as `acme-data-client`
   (`advisories()` has no `ORDER BY`), not the Step 3 target repository
   `acme-backend`.
2. The engineer chose option 2 (two linked Tasks).
3. ACME-540 was created in `acme-data-client` and its description digest was
   posted.
4. ACME-540 was linked to ACME-530 with `Blocks`.

## What the prior run did not complete

- No symptom-repository Task exists for `acme-backend`.
- No `Related` link exists between ACME-540 and any symptom-repository Task.
