# Step 3 -- Codebase Investigation: ACME-500

## Target Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

Identified from: the Component field (`sdlc-workflow`) and the code paths referenced
in the bug description (plan-feature skill, CONVENTIONS.md parsing).

## Code Intelligence Status

Per CLAUDE.md: "No Serena MCP servers are configured. Code intelligence is not available."
Using Read/Grep/Glob fallback for investigation.

## Affected Code Paths

### 1. Convention Heading Extraction

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention conformance analysis

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

**Finding**: The heading extraction at `line[3:]` does **not** strip trailing whitespace.
When the heading line is `## Migration Patterns  \n`, the extracted section name becomes
`"Migration Patterns  "` (with two trailing spaces). This creates a key mismatch in the
conventions dictionary.

### 2. Convention-Aware Task Enrichment

**File**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`
**Section**: Convention-aware task enrichment

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md  {convention_name}: {action}")
```

**Finding**: The lookup uses exact string matching (`convention_name in discovered_conventions`).
When the dictionary key is `"Migration Patterns  "` (with trailing spaces) but the lookup
key is `"Migration Patterns"` (clean), the match fails silently. No warning or fallback is
triggered.

## Existing Test Coverage

**File**: `evals/plan-feature/files/conventions-mock.md`

The existing eval fixture for plan-feature conventions does **not** include trailing
whitespace on headings. This edge case is entirely uncovered by current tests.

## CONVENTIONS.md Lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to
incorporate into the fix task's Implementation Notes from the repo itself.

## Persistence-Impact Analysis

### Trace: convention extraction output to persistence boundary

1. `section_name = line[3:]` -- returns heading text (with potential trailing whitespace)
2. `conventions[section_name] = current_section_content` -- stores in in-memory dict
3. `if convention_name in discovered_conventions:` -- lookup against dict
4. `notes.append(...)` -- appends to Implementation Notes list
5. Implementation Notes are written into the Jira Task description via `jira.create_issue`

**Persistence boundary**: The incorrect output (missing convention reference) is persisted
to the Jira Task description at creation time. However, this is a **content omission**
(the convention is silently dropped), not an incorrect computed value stored in a database.

**Assessment**: No data migration is needed. The bug causes a missing reference in generated
task descriptions, which is corrected by fixing the code. Already-created tasks with missing
conventions would need manual review, but this is a Jira content issue, not a database
column requiring migration.

## Summary of Affected Files and Symbols

| File | Symbol/Section | Issue |
|------|---------------|-------|
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention heading extraction (`line[3:]`) | Does not strip trailing whitespace from headings |
| `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` | Convention-aware task enrichment (`convention_name in discovered_conventions`) | Exact match fails against whitespace-padded keys |
| `evals/plan-feature/files/conventions-mock.md` | Test fixture | Missing trailing whitespace edge case coverage |
