# Triage Outcome -- TC-8002 (CVE-2026-28940)

## Decision: Case C -- No Supported Versions Affected

The version impact analysis shows that **no supported product version ships a vulnerable version of serde_json**. All versions across both streams (2.1.x and 2.2.x) include serde_json >= 1.0.137, which is above the fix threshold of 1.0.135.

This is a **Case C** outcome per the triage-security skill: no remediation is needed.

## Rationale

CVE-2026-28940 affects serde_json versions **before 1.0.135**. The fix (a configurable recursion limit defaulting to 128 levels of nesting) was introduced in serde_json 1.0.135.

However, every version in the supportability matrix -- across both the 2.1.x stream (serde_json 1.0.137) and the 2.2.x stream (serde_json 1.0.138 - 1.0.139) -- already ships a serde_json version that includes the fix. The vulnerability was resolved in the dependency before any of these product versions were built.

The PSIRT-assigned Affects Versions field lists "RHTPA 2.2.0", but lock file evidence shows RHTPA 2.2.0 ships serde_json 1.0.138, which is not vulnerable.

## Proposed Jira Actions

The following Jira mutations would be proposed to the engineer for confirmation (not executed in this eval):

### 1. Affects Versions Correction (Step 3)

- **Current**: RHTPA 2.2.0
- **Proposed**: Remove all Affects Versions (no versions are affected)
- **Rationale**: PSIRT assigned RHTPA 2.2.0 based on scan-time heuristics, but lock file analysis at the pinned source commit (v0.4.5) shows serde_json 1.0.138, which is above the fix threshold.

### 2. Close as Not a Bug (Step 8, Case C)

After engineer confirmation:

1. **Add comment** to TC-8002:
   > No supported versions ship a vulnerable version of serde_json.
   > Version impact analysis:
   >
   > | Version | serde_json | Affected? |
   > |---------|------------|-----------|
   > | 2.1.0 | 1.0.137 | NO |
   > | 2.1.1 | 1.0.137 | NO |
   > | 2.2.0 | 1.0.138 | NO |
   > | 2.2.1 | 1.0.138 | NO |
   > | 2.2.2 | -- | NO (retag of 2.2.1) |
   > | 2.2.3 | 1.0.139 | NO |
   > | 2.2.4 | 1.0.139 | NO |
   >
   > All supported versions ship serde_json >= 1.0.137, which is outside the
   > affected range (< 1.0.135). The fix (configurable recursion limit) was
   > already included before any of these versions were built.

2. **Transition** TC-8002 to Closed with resolution **"Not a Bug"**.

3. **Set VEX Justification** (customfield_12345) to **"Component not Present"** -- the vulnerable version of serde_json (< 1.0.135) is not present in any shipped product version.

4. **Add label** `ai-cve-triaged` to TC-8002.

### 3. Post-Triage Summary Comment

A summary comment would be posted to TC-8002 documenting:
- The version impact table (all versions NOT affected)
- The Affects Versions correction (RHTPA 2.2.0 removed -- no versions affected)
- The triage outcome: Closed as "Not a Bug" with VEX justification "Component not Present"
- An @mention of the issue reporter (the PSIRT analyst) for visibility

### 4. No Remediation Tasks Created

Since no versions are affected, no remediation tasks are created. No upstream backport or downstream propagation is needed.

## Cross-Stream Impact

The issue is scoped to stream 2.2.x (from summary suffix `[rhtpa-2.2]`). The 2.1.x stream was also analyzed and is likewise not affected (serde_json 1.0.137 in both 2.1.0 and 2.1.1). No cross-stream remediation is needed.

## Summary

| Aspect | Detail |
|--------|--------|
| CVE | CVE-2026-28940 |
| Library | serde_json |
| Affected range | < 1.0.135 |
| Fix threshold | 1.0.135 |
| Lowest shipped version | 1.0.137 (stream 2.1.x) |
| Versions affected | 0 of 7 |
| Triage outcome | Case C: Close as Not a Bug |
| VEX Justification | Component not Present |
| Remediation tasks | None |
