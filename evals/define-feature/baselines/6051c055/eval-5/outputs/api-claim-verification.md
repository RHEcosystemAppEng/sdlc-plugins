# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission"
> "The GitHub API does not support modifying a submitted review"

This claim asserts that the GitHub REST API lacks the capability to update or modify a pull request review once it has been submitted, and therefore a new review must always be created.

## Verification Finding

**Status: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted pull request review. It accepts:
- `owner` (path) -- the repository owner
- `repo` (path) -- the repository name
- `pull_number` (path) -- the pull request number
- `review_id` (path) -- the review ID
- `body` (request body) -- the updated review body text

Documentation reference: [GitHub REST API -- Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)

## Suggested Corrected Language

**Original requirement:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Corrected requirement:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update the existing PR review when re-running evals, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |

The corrected language reflects the actual API capability: reviews can be updated after submission using the PUT endpoint, so the workflow should update existing reviews rather than always creating new ones.
