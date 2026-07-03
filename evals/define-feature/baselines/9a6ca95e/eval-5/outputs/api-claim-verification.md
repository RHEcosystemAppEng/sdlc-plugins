# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim:** "PR reviews cannot be updated after initial submission so always create a new review"

**Supporting statement:** "The GitHub API does not support modifying a submitted review"

## Verification Finding

**Result:** INCORRECT

The GitHub REST API **does** support updating a submitted pull request review. The endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. It is documented in the official GitHub REST API reference under Pull Request Reviews.

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing eval review when re-running on the same PR, or create a new review if none exists"
**Corrected notes:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"

The corrected language reflects the actual GitHub REST API capability and avoids creating duplicate reviews on repeated eval runs.
