# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claims were identified:

1. "PR reviews cannot be updated after initial submission"
2. "The GitHub API does not support modifying a submitted review"

These claims assert that the GitHub REST API lacks the capability to update a pull request review after it has been submitted.

## Verification Finding

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

- **Endpoint**: `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Capability**: This endpoint allows updating the body (comment text) of a previously submitted pull request review.
- **Documentation**: [GitHub REST API - Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

The API accepts a `body` parameter and updates the top-level review comment of an existing, already-submitted review.

## Suggested Corrected Language

**Original requirement row:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Corrected requirement row:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update the existing PR review when re-running evals on the same PR, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |
