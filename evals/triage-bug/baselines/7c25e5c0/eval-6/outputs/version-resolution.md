# Step 4.5 -- Affects Version Resolution

## 4.5.1 -- Check Existing Field

The bug issue ACME-500 already has the Affects Version/s field populated.

**Current value**: `0.9.0`

This field was set at issue creation time and is already present in the Jira issue metadata.

## 4.5.2 -- Present Options to User

Since the Affects Version/s field is already populated, the skill does NOT silently overwrite or skip the existing value. Instead, it presents the user with three options and waits for input:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep — leave the current value and skip to Step 5
2. Replace — clear and set a new value
3. Augment — add additional versions alongside the current ones

Choose (1/2/3):
```

**IMPORTANT**: The skill pauses here and waits for the user to choose one of the three options before proceeding. No automatic action is taken on the existing value.

## Rationale

- **Keep** is appropriate when the reporter has already confirmed the correct version and no further investigation is needed.
- **Replace** is appropriate when the triage investigation reveals the bug was introduced in a different version than the reporter indicated.
- **Augment** is appropriate when the triage investigation reveals additional affected versions beyond what the reporter indicated.

## Resolution

Awaiting user input. The workflow is paused at this step pending the user's choice of option 1, 2, or 3.
