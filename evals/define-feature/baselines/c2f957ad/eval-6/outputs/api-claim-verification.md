# External API Claim Verification

## Detection

- **Section:** Requirements (Step 3d), row 4
- **API:** GitHub REST API (Pull Request Reviews)
- **Claim detected (requirement):** "PR reviews cannot be updated after initial submission so always create a new review"
- **Claim detected (notes):** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated / modified after creation" and "The API does not support Y"

Notification to user:

> I identified a claim about an external API in the Requirements section: GitHub PR reviews cannot be updated after initial submission, and the GitHub API does not support modifying a submitted review. I will attempt to verify this against the official GitHub REST API documentation.

## Verification Attempt

- **WebSearch:** unavailable — no search performed
- **WebFetch:** unavailable — no documentation page fetched
- **Official documentation consulted:** none (web tools unavailable)

## Result

**Status: UNVERIFIED (fallback path)**

The claim could not be confirmed or refuted against official documentation. No verdict (confirmed / incorrect / inconclusive) is asserted, because none of the evidence-based outcomes apply without access to the documentation.

## Fallback Message Presented to User

> "I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **PR reviews cannot be updated after initial submission so always create a new review (the GitHub API does not support modifying a submitted review)**. Would you like to proceed
> as-is, or verify it manually before continuing?"

## Recommended Manual Check

Before relying on this requirement, review the official GitHub REST API documentation for Pull Request Reviews (docs.github.com, "REST API endpoints for pull request reviews") and check whether an endpoint exists to update a review (e.g., a `PUT`/`PATCH` method on `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`). If such an endpoint exists, requirement row 4 should be revised (e.g., "Update the existing eval review on subsequent runs instead of creating a new one").

## User Decision (simulated)

No revision was provided by the user in the input, so the requirement is kept with its original wording. Because the claim is unverified, the preview and the Jira comment explicitly flag it as an **unverified external API claim** requiring manual verification before planning/implementation.
