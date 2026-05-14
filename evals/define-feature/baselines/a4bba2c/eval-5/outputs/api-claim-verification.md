# External API Claim Verification

## Detected Claim

In the **Requirements** section (row 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission"
> "The GitHub API does not support modifying a submitted review"

This claim asserts that the GitHub REST API lacks the capability to modify a PR review once it has been submitted, and therefore a new review must always be created.

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a submitted pull request review. It accepts the `review_id` of an existing submitted review and a new `body` parameter to replace the review content.

**Documentation reference:** GitHub REST API — Pull Request Reviews — [Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

### Suggested Corrected Language

The original requirement row:

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

Should be corrected to:

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update the existing PR review when re-running evals on the same PR, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |

This correction reflects the actual capability of the GitHub REST API and avoids unnecessary review duplication.
