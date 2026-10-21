# External API Claim Verification

## Detected Claim

In the **Requirements** section (Section 4), the following claim was identified:

> "PR reviews cannot be updated after initial submission so always create a new review"
> Notes: "The GitHub API does not support modifying a submitted review"

This asserts that the GitHub REST API lacks the capability to modify a PR review after it has been submitted.

## Verification Finding

**Result: INCORRECT**

The GitHub REST API **does** support updating a submitted pull request review. The relevant endpoint is:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows updating the body of a previously submitted review. It is documented in the official GitHub REST API reference under the Pull Request Reviews category.

- **Method:** PUT
- **Endpoint:** `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Documentation:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

The claim that "The GitHub API does not support modifying a submitted review" is factually incorrect.

## Suggested Corrected Language

**Original requirement row:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |

**Corrected requirement row:**

| Requirement | Notes | Is MVP? |
|---|---|---|
| Update the existing PR review when re-running evals, or create a new review if none exists | Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review | Yes |

The corrected language reflects the actual API capability: reviews can be updated via the PUT endpoint, so the workflow should update an existing review rather than always creating a new one.
