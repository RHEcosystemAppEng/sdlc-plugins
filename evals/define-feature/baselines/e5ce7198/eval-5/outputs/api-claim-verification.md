# External API Claim Verification

## Detected Claims

The following claims in the user input were flagged for verification:

1. **Claim:** "PR reviews cannot be updated after initial submission so always create a new review"
   - **Source:** Section 4 — Requirements, row 4 (Requirement column)

2. **Claim:** "The GitHub API does not support modifying a submitted review"
   - **Source:** Section 4 — Requirements, row 4 (Notes column)

## Verification Finding

**Status: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. It is documented in the GitHub REST API reference under Pull Request Reviews.

Therefore, the requirement to "always create a new review" is based on a false premise. The system can update an existing review instead of creating a new one on each CI run, which would reduce review noise on the PR.

## Suggested Corrected Language

**Original Requirement:**
> PR reviews cannot be updated after initial submission so always create a new review

**Original Notes:**
> The GitHub API does not support modifying a submitted review

**Corrected Requirement:**
> Update the existing eval review when re-running, or create a new review if none exists

**Corrected Notes:**
> Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update a previously submitted review; create a new review only on the first run
