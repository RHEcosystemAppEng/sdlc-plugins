# External API Claim Verification

## Detected Claim

In **Section 4 -- Requirements**, the following claim was identified:

> "PR reviews cannot be updated after initial submission"
> "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to update or modify a pull request review once it has been submitted.

## Verification Finding

**Result: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted review. It accepts a `body` parameter containing the updated review text and returns the updated review object.

**Documentation reference:** GitHub REST API documentation for Pull Request Reviews -- the `PUT` method on the review resource endpoint confirms that submitted reviews can be modified after creation.

## Suggested Corrected Language

The original requirement row:

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

Should be corrected to:

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update the existing PR review when re-running evals on the same PR, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |
