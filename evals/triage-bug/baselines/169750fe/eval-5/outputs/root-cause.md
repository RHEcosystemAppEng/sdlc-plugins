# Root Cause Analysis -- Step 4

## Root Cause Determination

### What is broken

The dark mode toggle in Settings > Appearance updates the in-memory theme state but does not persist the user's preference to durable storage (e.g., `localStorage`). When the browser is closed and reopened, the in-memory state is lost and the application defaults to light mode.

### Why it is broken

The toggle handler updates the application's theme state (e.g., context or store) without writing the preference to `localStorage` or any other persistent storage mechanism. Additionally, the application initialization does not attempt to read a stored preference -- it unconditionally defaults to light mode on startup.

Two missing pieces cause this bug:

1. **No persistence write**: The dark mode toggle event handler sets the theme state in memory but never calls `localStorage.setItem('theme', 'dark')` (or equivalent) to save the choice.
2. **No persistence read on startup**: The application initialization/bootstrap logic does not check `localStorage.getItem('theme')` to restore the user's last preference before rendering.

### Where it is broken

- **Toggle handler**: The event handler for the dark mode toggle in the Settings > Appearance component -- missing the `localStorage.setItem()` call after updating state.
- **App initialization**: The application entry point or theme provider -- missing the `localStorage.getItem()` call to restore the persisted preference on load.

### How to verify the fix

A reproducer test should:

1. Simulate enabling dark mode via the settings toggle
2. Verify the preference is written to `localStorage`
3. Simulate an application restart (clear in-memory state, reinitialize)
4. Assert that the application loads in dark mode by reading the preference from `localStorage`
5. Also test the reverse: toggling back to light mode persists correctly

## Root Cause Comment (for Jira)

The following comment would be posted to ACME-511:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        { "type": "text", "text": "Root Cause" }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "The dark mode toggle updates the in-memory theme state but does not persist the preference to localStorage. On application startup, no stored preference is read -- the app unconditionally defaults to light mode. Two fixes are needed: (1) write the preference to localStorage when the toggle changes, and (2) read the stored preference on initialization before rendering."
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        { "type": "text", "text": "Affected Files" }
      ]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Settings > Appearance toggle handler -- missing localStorage.setItem() call" }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "Application initialization / theme provider -- missing localStorage.getItem() on startup" }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        { "type": "text", "text": "Suggested Approach" }
      ]
    },
    {
      "type": "orderedList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "In the dark mode toggle handler, add a localStorage.setItem('theme', mode) call after updating the in-memory state." }
              ]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [
                { "type": "text", "text": "In the application initialization or theme provider, add a localStorage.getItem('theme') call to read the stored preference and apply it before first render." }
              ]
            }
          ]
        }
      ]
    },
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [
        { "type": "text", "text": "Reproducer Strategy" }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Write a test that: (1) toggles dark mode ON, (2) asserts localStorage contains the dark mode preference, (3) re-initializes the application (clearing in-memory state), and (4) asserts the app loads in dark mode from the stored preference."
        }
      ]
    },
    {
      "type": "rule"
    },
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "This comment was AI-generated by "
        },
        {
          "type": "text",
          "text": "sdlc-workflow/triage-bug",
          "marks": [
            {
              "type": "link",
              "attrs": {
                "href": "https://github.com/RHEcosystemAppEng/sdlc-plugins"
              }
            }
          ]
        },
        {
          "type": "text",
          "text": " v0.13.10."
        }
      ]
    }
  ]
}
```
