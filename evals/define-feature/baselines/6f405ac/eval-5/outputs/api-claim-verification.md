# External API Claim Verification

## Detected Claims

Two related claims were detected in **Section 4 -- Requirements**:

1. **Claim:** "PR reviews cannot be updated after initial submission"
   - Source: Requirement row 4, requirement text
2. **Claim:** "The GitHub API does not support modifying a submitted review"
   - Source: Requirement row 4, notes column

## Verification Result

**INCORRECT** -- Both claims are factually wrong.

The GitHub REST API supports updating a submitted pull request review via:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. The capability is documented in the official GitHub REST API reference for pull request reviews.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update existing eval review if one was previously posted; create a new review only on first run"
**Corrected notes:** "Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review"
