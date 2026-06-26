# Codebase Investigation — ACME-500

## Step 2 — Reproduce/Trace

### Code-path tracing

This bug involves a skill behavior (plan-feature convention conformance analysis) and cannot be directly reproduced via CLI commands. Tracing through the relevant code paths instead.

**Entry point**: The `/plan-feature` skill invocation reads `CONVENTIONS.md` and parses its headings to discover convention sections. The Steps to Reproduce describe creating a `CONVENTIONS.md` with trailing whitespace on a heading line (`## Migration Patterns  `), then running `/plan-feature`.

**Trace findings**:

1. The plan-feature skill reads `CONVENTIONS.md` and splits its content by newlines.
2. For each line starting with `## `, the heading text is extracted using `line[3:]`.
3. The extracted heading `"Migration Patterns  "` (with trailing spaces) is stored as a dictionary key in `conventions`.
4. During task enrichment, the skill looks up convention names using exact string match: `if convention_name in discovered_conventions`.
5. The lookup uses the clean name `"Migration Patterns"` (without trailing spaces), which does not match the key `"Migration Patterns  "`.
6. The convention is silently skipped -- no warning or error is logged for a failed match.

**Reproduction outcome**: Confirmed via code-path tracing. The divergence from expected behavior occurs at the heading extraction step where `line[3:]` does not strip trailing whitespace.

## Step 3 — Codebase Investigation

### Target repository

- **Repository**: acme-backend (based on Component: sdlc-workflow)
- **Serena Instance**: serena_backend (from Repository Registry)
- **Path**: /home/dev/repos/acme-backend

### Code Intelligence note

Per CLAUDE.md: "No Serena MCP servers are configured. Code intelligence is not available." Falling back to Read/Grep/Glob for investigation.

### Affected files and symbols

#### File: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`

**Convention heading extraction** (convention lookup section):

```python
for line in conventions_content.split('\n'):
    if line.startswith('## '):
        section_name = line[3:]  # Extracts heading text after "## "
        conventions[section_name] = current_section_content
```

The defect is at `line[3:]` — this extracts the heading text by slicing from position 3 onward but does NOT call `.strip()` to remove trailing whitespace. When the heading line is `## Migration Patterns  \n`, the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).

**Convention-aware task enrichment** (task enrichment section):

```python
if convention_name in discovered_conventions:
    notes.append(f"Per CONVENTIONS.md Section {convention_name}: {action}")
```

This match fails when `convention_name` is `"Migration Patterns"` (clean) but the dictionary key is `"Migration Patterns  "` (with trailing whitespace from extraction).

### Existing test coverage

- **File**: `evals/plan-feature/files/conventions-mock.md`
- **Finding**: The existing eval fixture for plan-feature conventions does NOT include trailing whitespace on headings. This edge case is not covered by current evals.

### CONVENTIONS.md lookup

The repository does not have a `CONVENTIONS.md` at its root. No conventions to apply to the generated task.

### Investigation summary

| Aspect | Finding |
|--------|---------|
| Defect location | `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` — heading extraction logic |
| Defect type | Missing whitespace normalization in string extraction |
| Root symbol | `line[3:]` in convention heading parser |
| Impact | Conventions with trailing whitespace on headings are silently dropped |
| Silent failure | No warning or error logged when a convention match fails |
| Test gap | Existing eval fixtures do not include trailing whitespace on headings |
| Reuse candidates | None identified — the fix is localized to the heading extraction line |
