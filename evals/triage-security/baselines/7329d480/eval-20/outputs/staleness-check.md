# Step 0.3 -- Matrix Staleness Check

## Configuration

- Current date: 2026-07-02
- Staleness threshold: 14 days

## Streams Checked

### Stream 2.1.x (rhtpa-release.0.3.z)

| Field | Value |
|-------|-------|
| Matrix file | security-matrix.md (shared file covering both streams) |
| Last-Updated timestamp | 2026-06-28T10:00:00Z |
| Age | 4 days |
| Threshold | 14 days |
| Result | **Fresh** -- no action required |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Field | Value |
|-------|-------|
| Matrix file | security-matrix.md (shared file covering both streams) |
| Last-Updated timestamp | 2026-06-28T10:00:00Z |
| Age | 4 days |
| Threshold | 14 days |
| Result | **Fresh** -- no action required |

## Outcome

Both version streams have a `Last-Updated` timestamp of 2026-06-28, which is
4 days ago. This is well within the 14-day staleness threshold.

**Step 0.3 passes silently.** No staleness warning is raised; triage proceeds
with the current matrix data.
