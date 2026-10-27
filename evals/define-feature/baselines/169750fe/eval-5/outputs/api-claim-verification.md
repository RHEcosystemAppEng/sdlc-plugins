# External API Claim Verification

## Detected Claim

**Section:** Requirements (Section 4)

**Claim text:** "PR reviews cannot be updated after initial submission" / "The GitHub API does not support modifying a submitted review"

**Requirement row:** "PR reviews cannot be updated after initial submission so always create a new review" with note "The GitHub API does not support modifying a submitted review"

## Verification Result: INCORRECT

The claim is **incorrect**. The GitHub REST API does support updating a submitted pull request review.

### Evidence

The GitHub REST API provides the following endpoint for updating a submitted review:

```
PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}
```

This endpoint accepts a `body` parameter to update the review's top-level comment text after it has been submitted. It is documented in the official GitHub REST API reference under Pull Request Reviews.

**Documentation reference:** https://docs.github.com/en/rest/pulls/reviews#update-a-review-for-a-pull-request

### Conclusion

The requirement's premise is factually wrong. PR reviews can be updated after submission using the `PUT` endpoint above. The requirement should be revised to reflect this capability rather than assuming reviews are immutable.

## Suggested Corrected Language

**Original requirement:** "PR reviews cannot be updated after initial submission so always create a new review"

**Original note:** "The GitHub API does not support modifying a submitted review"

**Corrected requirement:** "Update the existing PR review when re-running evals, or create a new review if none exists"

**Corrected note:** "Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review"
