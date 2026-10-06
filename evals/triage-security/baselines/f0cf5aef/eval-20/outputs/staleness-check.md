# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Version Streams checked**: 2.1.x, 2.2.x
- **Staleness threshold**: 14 days
- **Matrix file**: security-matrix-mock.md (shared file covering both streams)

## Timestamp Extraction

| Stream | Matrix File | Last-Updated Timestamp | Age | Status |
|--------|-------------|------------------------|-----|--------|
| 2.1.x | security-matrix-mock.md | 2026-06-28T10:00:00Z | Within 14-day threshold | Fresh |
| 2.2.x | security-matrix-mock.md | 2026-06-28T10:00:00Z | Within 14-day threshold | Fresh |

## Result

Both version streams have a `Last-Updated` timestamp within the 14-day staleness
threshold. No staleness warning is required.

**Action**: Proceed silently to Step 1 (Data Extraction) without interruption.

No user interaction needed -- the matrix is current and reflects the latest release
landscape for both the 2.1.x and 2.2.x streams.
