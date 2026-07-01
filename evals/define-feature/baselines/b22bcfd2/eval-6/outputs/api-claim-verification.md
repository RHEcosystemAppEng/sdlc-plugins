# API Claim Verification

## Detected Claim

In the Requirements section, the following external API claim was detected:

> "PR reviews cannot be updated after initial submission so always create a new review — The GitHub API does not support modifying a submitted review"

This claim asserts that the GitHub REST API does not support updating or modifying a PR review after it has been submitted.

## Verification Status

**Status: Unverified**

Web tools are unavailable in this session, so the claim cannot be verified against the GitHub REST API documentation. The claim remains unverified.

## User Decision Required

Would you like to:

1. **Proceed as-is** — retain the original claim wording in the Feature description without verification
2. **Verify manually** — check the GitHub REST API documentation yourself before proceeding (reference: `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`)
3. **Remove the claim** — drop the requirement row and revisit it later

Please indicate how you would like to proceed.
