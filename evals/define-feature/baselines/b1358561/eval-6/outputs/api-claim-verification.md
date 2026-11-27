# External API Claim Verification

## Claim Detected

- **Section:** Requirements (Step 3d), row 4
- **API:** GitHub REST API (Pull Request Reviews)
- **Claim (requirement):** "PR reviews cannot be updated after initial submission so always create a new review"
- **Claim (notes):** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated ... after creation" / "The API does not support Y"

## User Notification

> I detected a claim about an external API capability in the Requirements section: GitHub PR reviews cannot be updated after initial submission. I'll attempt to verify it against the official GitHub REST API documentation.

## Verification Attempt

- **WebSearch:** unavailable, not performed
- **WebFetch:** unavailable, not performed
- **Result:** UNVERIFIED (fallback path)

No official documentation was consulted, so the claim was neither confirmed nor refuted. The skill does not mark it confirmed or incorrect from memory. It flags the claim to the user.

## Fallback Message to User

> I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **PR reviews cannot be updated after initial submission so always create a new review (the GitHub API does not support modifying a submitted review)**. Would you like to proceed as-is, or verify it manually before continuing?

## Suggested Manual Check

Before this Feature goes to planning, check the official GitHub REST API docs for Pull Request Reviews (docs.github.com, "REST API endpoints for pull request reviews"). Look for an endpoint that updates an existing review, for example an `update a review` operation on `/repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`. If that endpoint exists, revise requirement row 4. The design would then update the existing eval review instead of always creating a new one.

## Outcome

Pending user decision. The original wording is kept in the preview, and the claim is marked as unverified there. Nothing goes to Jira until the user explicitly picks "proceed as-is" or revises the requirement after checking it manually.
