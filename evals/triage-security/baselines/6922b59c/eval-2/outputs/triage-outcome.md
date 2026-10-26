# Triage Outcome -- TC-8002

## Decision: Case C -- No Supported Versions Affected

### Summary

CVE-2026-28940 affects serde_json versions **before 1.0.135**. Lock file
analysis across all supported product versions (both the 2.1.x and 2.2.x
streams) shows that every version ships serde_json **1.0.137 or later**,
which is outside the vulnerable range. No supported version is affected.

### Recommendation

**Close TC-8002 as "Not a Bug" (not affected).**

### Proposed Jira Actions

The following actions would be performed (in this eval, they are documented
rather than executed):

#### 1. Assign and Transition (Step 0.8)

- Assign TC-8002 to the current user.
- Transition TC-8002 from "New" to "Assigned" status.

#### 2. Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is `RHTPA 2.2.0`. Since the version impact
analysis shows that RHTPA 2.2.0 is **not affected** (ships serde_json 1.0.138,
which is above the fix threshold of 1.0.135), the Affects Versions field should
be cleared or left as-is for the closure.

Since the issue is being closed as "Not a Bug", no Affects Versions correction
is strictly required -- the closure itself documents that no versions are
affected.

#### 3. Duplicate/Sibling Check (Step 4)

No sibling search was performed (eval mode). In a live triage, the skill would
search for other Vulnerability issues with the `CVE-2026-28940` label.

Steps 4.3 (cross-CVE overlap) and 4.4 (preemptive task reconciliation) are
skipped because the Upstream Affected Component custom field is not configured.

#### 4. Version Lifecycle Check (Step 5)

Not performed in this eval. In a live triage, the product lifecycle page at
https://access.example.com/product-life-cycle/rhtpa would be checked to verify
that affected versions are within support lifecycle. Since no versions are
affected, this step does not change the outcome.

#### 5. Already Fixed Check (Step 6)

Not applicable. The vulnerability was never present in any supported version --
this is not an "already fixed" scenario but rather a "never affected" scenario.

#### 6. Concurrent Triage Detection (Step 7)

Skipped because the Upstream Affected Component custom field is not configured.

#### 7. Release Jira Orchestration (Step 7.5)

Not applicable. No remediation is needed, so no release Jira structure is
required.

#### 8. Close as Not a Bug (Step 8, Case C)

**Proposed actions:**

1. **Add closing comment** to TC-8002:

   > No supported versions ship a vulnerable version of serde_json.
   > Version impact analysis:
   >
   > | Version | serde_json | Affected? |
   > |---------|------------|-----------|
   > | 2.1.0 | 1.0.137 | NO |
   > | 2.1.1 | 1.0.137 | NO |
   > | 2.2.0 | 1.0.138 | NO |
   > | 2.2.1 | 1.0.138 | NO |
   > | 2.2.2 | 1.0.138 | NO (retag of 2.2.1) |
   > | 2.2.3 | 1.0.139 | NO |
   > | 2.2.4 | 1.0.139 | NO |
   >
   > All supported versions ship serde_json >= 1.0.137, which is outside the
   > affected range (versions before 1.0.135). The fix (recursion limit,
   > introduced in 1.0.135) is already present in all shipped versions.

2. **Set VEX Justification** (customfield_12345): **"Component not Present"**

   Rationale: The vulnerable version of serde_json (< 1.0.135) is not present
   in any supported product version. All versions ship serde_json >= 1.0.137.

3. **Transition** TC-8002 to **Closed** with resolution **"Not a Bug"**.

4. **Add label** `ai-cve-triaged` to TC-8002 to mark it as triaged.

### Post-Triage Summary Comment

A summary comment would be posted to TC-8002 documenting:

1. Version impact table (all versions unaffected)
2. No Affects Versions correction needed (closing as not affected)
3. Triage outcome: Closed as Not a Bug -- no supported versions ship a
   vulnerable serde_json version
4. No remediation tasks created
5. VEX Justification: Component not Present

### Key Evidence

- **Fix threshold**: serde_json 1.0.135 (from CVE description)
- **Lowest shipped version**: serde_json 1.0.137 (versions 2.1.0 and 2.1.1)
- **Margin**: All shipped versions are at least 2 patch versions above the fix
  threshold
- **Ecosystem**: Cargo (Rust crate, source dependency)
- **Issue stream scope**: 2.2.x (but all streams checked per triage rules)
- **Cross-stream status**: Neither stream (2.1.x nor 2.2.x) is affected
