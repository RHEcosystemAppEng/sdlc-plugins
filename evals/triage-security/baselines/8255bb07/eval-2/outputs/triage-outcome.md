# Triage Outcome -- TC-8002

## Decision: Case C -- No Supported Versions Affected

CVE-2026-28940 (serde_json stack overflow, versions before 1.0.135) does not affect
any supported product version. All versions across both the 2.1.x and 2.2.x streams
ship serde_json >= 1.0.137, which is well above the fix threshold of 1.0.135.

**Recommendation: Close as "Not a Bug" (not affected).**

## Evidence

- The vulnerability affects serde_json versions **before 1.0.135**
- The lowest serde_json version shipped across all supported versions is **1.0.137** (in versions 2.1.0 and 2.1.1)
- Every other version ships 1.0.138 or 1.0.139
- No version has ever shipped a vulnerable serde_json version

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Version is **RHTPA 2.2.0**. Based on lock file evidence,
RHTPA 2.2.0 ships serde_json 1.0.138, which is NOT affected. The Affects Version is
incorrect.

**Proposed action**: Remove RHTPA 2.2.0 from Affects Versions (no versions should
remain, since none are affected). This correction reinforces the Case C close decision.

## Proposed Jira Actions

The following actions are presented as recommendations requiring engineer confirmation
before execution:

### 1. Assign and Transition (Step 0.7)

- **Assign** TC-8002 to the current user
- **Transition** from New to Assigned status

### 2. Affects Versions Correction (Step 3)

- **Remove** RHTPA 2.2.0 from Affects Versions (not actually affected per lock file evidence)

### 3. Close as Not a Bug (Step 8, Case C)

- **Add comment** to TC-8002:

  > No supported versions ship a vulnerable version of serde_json.
  >
  > Version impact analysis:
  >
  > | Version | serde_json | Affected? |
  > |---------|-----------|-----------|
  > | 2.1.0 | 1.0.137 | NO |
  > | 2.1.1 | 1.0.137 | NO |
  > | 2.2.0 | 1.0.138 | NO |
  > | 2.2.1 | 1.0.138 | NO |
  > | 2.2.2 | -- | NO (retag of 2.2.1) |
  > | 2.2.3 | 1.0.139 | NO |
  > | 2.2.4 | 1.0.139 | NO |
  >
  > All supported versions ship serde_json >= 1.0.137, which is outside the
  > affected range (versions before 1.0.135). The fix was included in serde_json
  > 1.0.135, and the earliest version we ship is 1.0.137.

- **Transition** TC-8002 to Closed with resolution "Not a Bug"
- **Set VEX Justification** (customfield_12345) to **"Component not Present"**
  -- while the serde_json package is present, no vulnerable version of it is
  shipped. The more precise VEX value would depend on organizational convention;
  the recommended value here reflects that the vulnerable version range
  (before 1.0.135) is not present in any shipped product version.

  Note: An alternative VEX value of **"Vulnerable Code not Present"** could also
  apply, since the fixed version (1.0.135+) contains the recursion limit patch
  and the vulnerable code path no longer exists. The choice between these two
  depends on organizational VEX policy. The default per the skill procedure is
  "Component not Present" when the vulnerable package version is not included.

### 4. Add Label (Post-Triage)

- **Add label** `ai-cve-triaged` to TC-8002

### 5. Post-Triage Summary Comment

- **Add comment** to TC-8002 with:
  - Version impact table (as above)
  - Affects Versions correction: removed RHTPA 2.2.0 (not affected)
  - Triage outcome: Closed as Not a Bug -- no supported versions ship a vulnerable serde_json version
  - No remediation tasks created (none needed)
  - @mention of the issue reporter (PSIRT analyst)
  - Comment footnote per skill convention

## Duplicate / Sibling Check (Step 4)

No duplicate or sibling issues were identified in this eval scenario. In a live
triage, a JQL search would be run:
```
project = TC AND issuetype = 10024 AND labels = CVE-2026-28940 AND key != TC-8002
```
to find any companion issues for the same CVE across other streams.

## Version Lifecycle Check (Step 5)

Not performed in this eval (no external access). In a live triage, the Product
pages URL (https://access.example.com/product-life-cycle/rhtpa) would be checked
to confirm all versions in the impact table are still within support. Since no
versions are affected, this step has no bearing on the triage outcome.

## Already Fixed Check (Step 6)

This step checks for resolved sibling issues that already addressed the CVE. In
this case, the check is moot -- the vulnerability was never present in any
shipped version, so there is nothing to "fix." The appropriate outcome remains
Case C (close as Not a Bug), not "already fixed via sibling."

## No Remediation Tasks Needed

Since no supported versions are affected (Case C), no remediation tasks are created.
No upstream backport tasks or downstream propagation tasks are necessary.
