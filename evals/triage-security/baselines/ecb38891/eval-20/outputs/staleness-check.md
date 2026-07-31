# Step 0.3 -- Matrix Staleness Check

## Configuration

Version Streams from Security Configuration:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Staleness Check Results

The security-matrix.md file covers both streams in a single file. The `Last-Updated` timestamp was read from the HTML comment at the top of the file:

```
<!-- Last-Updated: 2026-06-28T10:00:00Z -->
```

- **Last-Updated**: 2026-06-28T10:00:00Z
- **Current date**: 2026-07-31
- **Staleness threshold**: 14 days (default)
- **Result**: The matrix timestamp is within the 14-day threshold. **No staleness warning displayed.**

## Outcome

The staleness check passed silently. No warning was presented to the user and no user prompt or options were displayed. Triage proceeds directly to Step 0.5 (JIRA Access Initialization) and beyond without any interruption from the staleness check.
