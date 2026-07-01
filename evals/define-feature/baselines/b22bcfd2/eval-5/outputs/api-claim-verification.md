# External API Claim Verification

## Detected Claim

The following claim was found in **Section 4 — Requirements**:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

## Verification Result: INCORRECT

The claim that the GitHub API does not support modifying a submitted review is **factually incorrect**.

### Evidence

The GitHub REST API provides the following endpoint for updating a submitted pull request review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted review. Documentation reference: [GitHub REST API — Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request).

## Suggested Corrected Language

**Original Requirement:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Corrected Requirement:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update the existing PR review when re-running evals on the same PR, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |
