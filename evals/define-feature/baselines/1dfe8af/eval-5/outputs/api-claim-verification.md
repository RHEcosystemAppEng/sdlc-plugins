# External API Claim Verification

## Detected Claims

The following claims were detected in **Section 4 — Requirements**:

1. **"PR reviews cannot be updated after initial submission so always create a new review"**
2. **"The GitHub API does not support modifying a submitted review"**

## Verification Finding

**Status: INCORRECT**

The claims are factually wrong. The GitHub REST API **does** support updating a submitted pull request review via the following endpoint:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint allows modifying the body of an already-submitted review. It is documented in the GitHub REST API reference under Pull Request Reviews.

## Evidence

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Purpose:** Update the body text of a pull request review that has already been submitted
- **Documentation:** [GitHub REST API — Update a review for a pull request](https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request)

## Suggested Correction

The Requirement row currently reads:

> PR reviews cannot be updated after initial submission so always create a new review

Suggested corrected language:

> PR reviews can be updated using `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`, so update the existing review instead of creating a new one when re-running evals

The Notes column currently reads:

> The GitHub API does not support modifying a submitted review

Suggested corrected language:

> The GitHub REST API supports updating a submitted review via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
