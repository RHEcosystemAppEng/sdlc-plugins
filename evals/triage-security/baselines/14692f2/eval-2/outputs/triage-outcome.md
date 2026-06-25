# Step 7 -- Triage Outcome: TC-8002 (CVE-2026-28940)

## Decision: Case C -- No Supported Versions Affected

**Recommendation: Close as Not a Bug (not affected).**

### Rationale

The version impact analysis shows that **all** supported product versions (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) ship serde_json >= 1.0.135, which is outside the affected range (< 1.0.135). No supported version includes a vulnerable version of serde_json.

- Lowest serde_json version across all streams: **1.0.137** (in 2.1.0 and 2.1.1)
- Fix threshold: **1.0.135**
- 1.0.137 >= 1.0.135 -- not affected

### Proposed Jira Actions

The following Jira mutations would be performed after engineer confirmation:

1. **Add comment to TC-8002:**

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
   > All supported versions ship serde_json >= 1.0.137 which is outside the affected range (< 1.0.135).

2. **Transition TC-8002 to Closed** with resolution **Not a Bug**.

3. **Set VEX Justification** (customfield_12345) to **Component not Present**.

   Justification: The vulnerable version of serde_json (< 1.0.135) is not present in any supported product version. All versions ship a patched version (>= 1.0.135).

4. **Assign TC-8002** to current user.

5. **Add label** `ai-cve-triaged` to TC-8002.

### Remediation Tasks

**None.** No remediation tasks are created because no supported versions are affected (Case C).

### Affects Versions Correction

The current Affects Versions on TC-8002 is `[RHTPA 2.2.0]`. Since no versions are actually affected, the Affects Versions field should be **cleared** (set to empty) as part of the close action, or left as-is since the issue is being closed as Not a Bug. The close resolution and VEX Justification field convey that the product is not affected.

### VEX Justification

- **Field**: customfield_12345 (configured in Security Configuration)
- **Value**: Component not Present
- **Rationale**: The vulnerable package version (serde_json < 1.0.135) is not shipped in any supported product version. All versions include serde_json >= 1.0.137, which contains the fix for CVE-2026-28940.
