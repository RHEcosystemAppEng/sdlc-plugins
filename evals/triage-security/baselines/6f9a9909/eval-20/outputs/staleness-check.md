# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Version Streams** (from Security Configuration):
  - Stream 2.1.x -- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`
  - Stream 2.2.x -- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`

## Staleness Analysis

Both streams share a single security matrix file for this eval scenario.

### Matrix Timestamp

- **Last-Updated**: `2026-06-28T10:00:00Z`
- **Current date**: `2026-10-06`
- **Age**: 100 days
- **Threshold**: 14 days

### Result: STALE

The security matrix was last updated on 2026-06-28 (100 days ago), which exceeds the 14-day staleness threshold.

Per the skill protocol, the following warning would be presented to the engineer:

> Security matrix for stream **2.1.x** was last updated on 2026-06-28
> (100 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

> Security matrix for stream **2.2.x** was last updated on 2026-06-28
> (100 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

### Notes

- The `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` HTML comment was found at the top of the matrix file and successfully parsed as ISO 8601.
- Both streams (2.1.x and 2.2.x) reference this same matrix file in the eval scenario, so the staleness status applies to both.
- Engineer confirmation is required before proceeding. If the engineer selects "Proceed anyway," triage continues with the current matrix data. If "Refresh now," the matrix population logic from setup Step 10.6 would be invoked for the selected stream(s).
