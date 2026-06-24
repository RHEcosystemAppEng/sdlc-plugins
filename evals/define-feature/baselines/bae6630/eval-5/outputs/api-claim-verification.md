# External API Claim Verification

## Claim Detected

In **Section 4 — Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission — The GitHub API does not support modifying a submitted review."

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API **does** support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a previously submitted pull request review. It is documented in the official GitHub REST API documentation:

- **Endpoint**: `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Documentation**: https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request
- **Purpose**: Update the body text of a pull request review that has already been submitted.

### Suggested Correction

The requirement stating "PR reviews cannot be updated after initial submission so always create a new review" should be revised. Suggested corrected language:

> "Update existing PR reviews when re-running evals on the same PR, rather than creating duplicate reviews. Use the GitHub REST API `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint to update the review body with the latest eval results."

This correction was presented to the user for confirmation before finalizing the Requirements section.
