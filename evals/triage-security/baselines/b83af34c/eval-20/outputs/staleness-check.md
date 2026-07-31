# Step 0.3 -- Matrix Staleness Check

## Configuration

- Version Streams checked: 2.1.x, 2.2.x
- Matrix file: security-matrix-mock.md (single file covering both streams)
- Staleness threshold: 14 days (default)

## Timestamp Extraction

The `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` HTML comment was read from line 1
of security-matrix-mock.md. Parsed ISO 8601 timestamp: **2026-06-28T10:00:00Z**.

## Staleness Calculation

- Last-Updated: 2026-06-28
- Current date: 2026-07-31
- Days elapsed: **33 days**
- Threshold: 14 days

**Result: STALE** -- The matrix is 33 days old, which exceeds the 14-day threshold.

## Action Per Skill Specification

Per SKILL.md Step 0.3, when the matrix is older than 14 days, the skill MUST warn the
user and present options:

> "Security matrix for stream **2.1.x** / **2.2.x** was last updated on 2026-06-28
> (33 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate"

The skill would wait for the user's choice before proceeding. This is NOT a silent pass.

## Conclusion

The staleness check detected that the matrix is outdated (33 days > 14-day threshold).
A staleness warning and user prompt would be displayed. The triage would be interrupted
at Step 0.3 pending user input.

If the user chose "Proceed anyway" (option 2), triage would continue to Step 0.5 and
beyond. If the user chose "Stop" (option 3), triage would halt. If the user chose
"Refresh now" (option 1), matrix population would be re-run first.
