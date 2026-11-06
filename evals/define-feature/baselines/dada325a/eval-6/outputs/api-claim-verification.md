# External API Claim Verification

## Claim Detected

- **Section:** Requirements (Step 3d), row 4
- **API:** GitHub REST API (Pull Request Reviews)
- **Claim (requirement):** "PR reviews cannot be updated after initial submission so always create a new review"
- **Claim (notes):** "The GitHub API does not support modifying a submitted review"
- **Pattern matched:** "X cannot be updated / modified after creation" / "The API does not support Y"

## User Notification

> I detected a claim about an external API capability in the Requirements section:
> "PR reviews cannot be updated after initial submission" (the GitHub API does not
> support modifying a submitted review). I will try to verify it against the official
> GitHub REST API documentation before finalizing this section.

## Verification Attempt

- **WebSearch:** unavailable (not performed)
- **WebFetch:** unavailable (not performed)
- **Official documentation consulted:** none. The web tools needed to look it up were unavailable.

## Result: UNVERIFIED (fallback path)

The claim could not be checked against official documentation. It is neither confirmed
nor refuted. No verdict is given, and the claim is flagged for the user.

## Fallback Prompt Shown to User

> "I detected a claim about an external API but cannot verify it right now
> (web tools unavailable). The claim is: **PR reviews cannot be updated after initial
> submission so always create a new review (The GitHub API does not support modifying a
> submitted review)**. Would you like to proceed as-is, or verify it manually before
> continuing?"

## Recommended Manual Check

Before planning or implementing, check the GitHub REST API "Pull request reviews"
documentation (docs.github.com, REST API > Pulls > Reviews). Look for an endpoint that
updates an existing review, such as a `PUT` on a specific review ID. If one exists,
change requirement row 4 so it updates the existing review instead of always creating
a new one.

## Outcome Recorded for This Run

- The user input for this eval gives no answer to the prompt, so no correction was confirmed.
- Per the "Do NOT fabricate content" guardrail, requirement row 4 keeps the user's original wording.
- The claim is marked as **unverified** in the preview and in the post-creation Jira comment, so planning picks it up.
