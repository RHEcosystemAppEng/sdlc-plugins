# Affects Version Resolution -- ACME-500

## Step 4.5: Affects Version/s Resolution

### Step 4.5.1: Check Existing Value

The bug issue ACME-500 already has the Affects Version/s field populated.

**Current value**: `0.9.0`

Since the field is already populated, the skill does NOT silently overwrite or skip the existing value. Instead, it presents the user with three options:

```
Affects Version/s is already set: [0.9.0]

Options:
1. Keep — leave the current value and skip to Step 5
2. Replace — clear and set a new value
3. Augment — add additional versions alongside the current ones

Choose (1/2/3):
```

### Resolution

The skill WAITS for user input before proceeding. No automatic action is taken on the Affects Version/s field.

- If the user chooses **1 (Keep)**: The value remains `0.9.0` and the skill proceeds to Step 5 (Generate Task).
- If the user chooses **2 (Replace)**: The skill clears `0.9.0` and prompts the user for a new version value to set.
- If the user chooses **3 (Augment)**: The skill keeps `0.9.0` and prompts the user for additional version values to add alongside it.

### Key Behavior

The existing value is respected. The skill never silently overwrites a pre-populated Affects Version/s field. User confirmation is required before any modification.
