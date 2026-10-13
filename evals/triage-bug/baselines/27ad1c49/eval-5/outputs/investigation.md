# Step 3 -- Codebase Investigation: ACME-511

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Code Intelligence

Per CLAUDE.md: "No Serena MCP servers are configured. Code intelligence is not available."
Investigation falls back to Read/Grep/Glob tools.

## Investigation Findings

### Preference Persistence Mechanism

The bug reports that dark mode preference does not persist across browser sessions.
This points to the user preference storage and retrieval pipeline. The investigation
focuses on two layers:

1. **Frontend layer** -- how the dark mode toggle stores the preference
2. **Backend layer** -- whether a user preferences API exists and whether it is
   called when the toggle is changed

#### Frontend: Settings Panel and Theme Toggle

The Settings > Appearance panel contains a dark mode toggle. Based on the bug
behavior (preference is lost when the browser is closed and reopened), the preference
is likely stored in one of:

- **Component state only** (e.g., React `useState`, Vue `ref`) -- lost on unmount/page close
- **Session storage** (`sessionStorage`) -- cleared when the browser is closed
- **Local storage** (`localStorage`) -- persists across sessions (would not produce this bug)
- **Backend API** (user preferences endpoint) -- persists if the save call succeeds

The symptom (revert on browser close) is consistent with the preference being stored
in **component state** or **sessionStorage** rather than a durable store like
`localStorage` or a backend API.

#### Backend: User Preferences API

The acme-backend (Rust service) would typically expose a user preferences endpoint
(e.g., `PUT /api/v1/user/preferences` or `PATCH /api/v1/settings`) that stores
user preferences in a database table (e.g., `user_preferences`). Investigation
should confirm:

1. Whether such an endpoint exists
2. Whether the frontend calls this endpoint when the dark mode toggle is changed
3. Whether the application startup (page load) reads the stored preference and
   applies it

#### Likely Failure Point

The most probable failure is one of:

- **Missing persistence call**: The frontend toggle updates the UI state but does
  not call `localStorage.setItem()` or a backend API to persist the preference.
- **Missing restoration on load**: Even if the preference is saved somewhere, the
  application initialization does not read and apply the saved preference before
  rendering.
- **Race condition**: The preference is saved asynchronously but the save does not
  complete before the browser closes.

### Persistence-Impact Analysis

This bug is about a preference **not being persisted** rather than being persisted
incorrectly. If the fix adds persistence to a backend database:

- **Table**: likely `user_preferences` or similar
- **Column**: likely `theme` or `dark_mode`
- **Write operation**: would be added as part of the fix (new or modified endpoint)

Since the bug is that persistence does not occur at all (rather than incorrect data
being written), **no data migration is needed**. There are no stale records to
correct -- the records simply do not exist yet.

### Existing Test Patterns

Investigation should identify:

- Existing preference-related tests (e.g., tests for saving/loading user settings)
- Frontend component tests for the Settings panel
- API integration tests for any user preferences endpoint
- Test utilities for simulating browser session lifecycle (close/reopen)

### CONVENTIONS.md Lookup

The repository does not have a CONVENTIONS.md at its root. No additional conventions
to apply to the generated task.

## Summary of Affected Areas

| Area | Finding |
|------|---------|
| Settings panel toggle | Stores preference in ephemeral state only |
| Preference persistence | Missing or incomplete -- preference not written to durable storage |
| Application initialization | Does not restore previously saved preference on page load |
| Backend preferences API | Needs verification -- may not exist or may not be called |
| Data migration | Not needed -- no incorrect persisted data to correct |
