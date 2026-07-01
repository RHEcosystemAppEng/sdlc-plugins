# External API Claim Verification

## Detected Claim

**Source section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission so always create a new review — The GitHub API does not support modifying a submitted review"

## Verification Result

**Status:** INCORRECT

The claim that the GitHub API does not support modifying a submitted review is factually wrong. The GitHub REST API provides an endpoint to update a pull request review after it has been submitted:

- **Endpoint:** `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
- **Documentation:** [Update a pull request review](https://docs.github.com/en/rest/pulls/reviews#update-a-pull-request-review)
- **Capability:** This endpoint allows updating the body of a submitted review. A submitted review can be modified after initial submission.

## Suggested Correction

Replace the incorrect requirement:

> PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review

With corrected language:

> PR reviews can be updated after submission using the GitHub REST API (PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}); prefer updating an existing review over creating a new one to reduce notification noise | Update the existing review when re-running evals on the same PR
