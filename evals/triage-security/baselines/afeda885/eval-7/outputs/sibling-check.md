# Step 4 -- Sibling and Link Analysis for TC-8006

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

### JQL Search for Siblings

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Result**: 1 sibling found.

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (companion tracker, NOT a duplicate)

TC-8001 is a cross-stream companion, not a same-stream duplicate. PSIRT intentionally creates one Vulnerability issue per stream. No duplicate closure is warranted.

### Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker for the 2.2.x stream). Per the Step 4.2 procedure:

1. **Check for existing link before creating one.**

   The issue's `issuelinks` array (fetched in Step 1) already contains:
   - Link type: `Related`
   - Direction: outward (TC-8006 -> TC-8001)
   - Link ID: 1990401

   This link satisfies all three conditions required by Step 4.2:
   - `type.name` is "Related" -- YES
   - `outwardIssue.key` matches the sibling key (TC-8001) -- YES
   - Link already exists -- YES

   **Result: Related link to TC-8001 already exists -- skipping link creation.**

   No `jira.create_link` call is needed. The existing link is sufficient for cross-stream coordination.

2. **Verify no Affects Versions overlap.**

   - TC-8006 Affects Versions: RHTPA 2.1.0
   - TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1
   - Overlap: **None** -- each issue carries only versions from its own stream.

   No version overlap detected. Each companion issue correctly owns its stream's versions.

3. **Sibling landscape presentation:**

   ```
   CVE-2026-31812 companion issues:

   | Issue      | Stream | Status      | Affects Versions             |
   |------------|--------|-------------|------------------------------|
   | TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1    |
   | TC-8006 <--| 2.1.x  | New         | RHTPA 2.1.0                  |
   ```

   The arrow indicates TC-8006 is the current issue being triaged.

### Step 4.3 -- Cross-CVE Overlap Detection

The Security Configuration in claude-md-security-config.md does NOT include the following optional fields:
- Upstream Affected Component custom field -- not configured
- PS Component custom field -- not configured
- Stream custom field -- not configured

Per the Step 4.3 prerequisite: "If any of these fields are not configured, skip this step entirely."

**Result: Step 4.3 skipped -- required custom fields not configured.**

### Step 4.4 -- Preemptive Task Reconciliation

Simulated JQL query for preemptive tasks:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

**Simulated result**: No matching preemptive tasks found for CVE-2026-31812 in the 2.1.x stream.

**Result: No preemptive task reconciliation needed. Proceeding to Step 5.**
