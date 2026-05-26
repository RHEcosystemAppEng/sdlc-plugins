# External API Claim Verification

## Detected Claim

In **Section 4 -- Requirements**, the following claims were detected:

> "PR reviews cannot be updated after initial submission so always create a new review"

> "The GitHub API does not support modifying a submitted review"

These statements assert that the GitHub REST API lacks the capability to update a pull request review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

**Evidence:**

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a submitted pull request review. It accepts a `body` parameter (the updated text of the review) and returns the updated review object.

**Documentation reference:** GitHub REST API -- Pull Request Reviews -- Update a pull request review.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Corrected requirement:** "PR reviews can be updated after submission using the GitHub REST API's update review endpoint (`PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`); prefer updating an existing review over creating a new one to reduce notification noise"

**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected notes:** "Use the GitHub REST API update review endpoint to modify existing reviews when re-running evals on the same PR"
