# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update or modify a pull request review after it has been submitted.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of a submitted pull request review. It accepts the `owner`, `repo`, `pull_number`, and `review_id` as path parameters, and the updated review `body` in the request payload.

Documentation reference: [GitHub REST API - Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

## Suggested Corrected Language

The requirement row should be revised from:

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

To:

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update existing PR review when re-running evals on the same PR, or create a new review if none exists | Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review | Yes |
