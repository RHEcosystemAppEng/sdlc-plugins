# Step 0.3 -- Matrix Staleness Check

This step runs **before** Step 0.5 (JIRA Access Initialization). No Jira operations
have been attempted at this point -- the staleness check is a prerequisite gate that
must pass before any triage work proceeds.

## Configuration Extracted (Step 0)

From the Security Configuration in CLAUDE.md, the Version Streams table defines
two streams:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Staleness Check Procedure

For each row in the Version Streams table, read the corresponding `security-matrix.md`
file and extract the `<!-- Last-Updated: <ISO-8601> -->` HTML comment at the top of the file.

### Stream: 2.1.x

**Matrix file**: security-matrix.md (for stream rhtpa-release.0.3.z)

1. **Read the matrix file** at the configured Security Matrix Path.
2. **Extract the timestamp** from the HTML comment:
   ```
   <!-- Last-Updated: 2026-05-01T10:00:00Z -->
   ```
   Parsed ISO 8601 value: **2026-05-01T10:00:00Z** (May 1, 2026)

3. **Staleness comparison**:
   - Last updated: 2026-05-01
   - Current date: 2026-07-31
   - Days since last update: **91 days**
   - Threshold: 14 days (default)
   - Result: **STALE** (91 days > 14 days)

4. **Staleness warning**:

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (91 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

---

### Stream: 2.2.x

**Matrix file**: security-matrix.md (for stream rhtpa-release.0.4.z)

1. **Read the matrix file** at the configured Security Matrix Path.
2. **Extract the timestamp** from the HTML comment:
   ```
   <!-- Last-Updated: 2026-05-01T10:00:00Z -->
   ```
   Parsed ISO 8601 value: **2026-05-01T10:00:00Z** (May 1, 2026)

3. **Staleness comparison**:
   - Last updated: 2026-05-01
   - Current date: 2026-07-31
   - Days since last update: **91 days**
   - Threshold: 14 days (default)
   - Result: **STALE** (91 days > 14 days)

4. **Staleness warning**:

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (91 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

---

## Step Ordering Confirmation

Step 0.3 (Matrix Staleness Check) has been executed. The following steps have **not**
been attempted and will not proceed until the user responds to the staleness warnings above:

- Step 0.5 -- JIRA Access Initialization (not yet executed)
- Step 0.7 -- Assign and Transition to Assigned (not yet executed)
- Step 1 -- Data Extraction (not yet executed)
- All subsequent steps (Steps 2-8)

No Jira MCP calls, REST API calls, or `git show` commands have been issued.
The staleness gate blocks all downstream triage operations until the user chooses
how to handle the stale matrix for each stream.
