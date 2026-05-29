# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

- **Requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
- **Notes:** "The GitHub API does not support modifying a submitted review"

This claim asserts that the GitHub REST API lacks the ability to update a pull request review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a pull request review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted review. It accepts a `body` parameter with the updated review text and returns the updated review object.

**Documentation reference:** GitHub REST API documentation for Pull Reviews -- the `PUT` method on `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` is a documented, supported endpoint.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"
**Original notes:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update existing PR review when re-running evals on the same PR, or create a new review if none exists"
**Corrected notes:** "Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review, or `POST` to create a new one"
