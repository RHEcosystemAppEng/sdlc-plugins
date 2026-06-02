# Description Digest Protocol

Skills that create Jira tasks (plan-feature, verify-pr) record a content digest of
the task description at creation time. Skills that consume tasks (implement-task)
use this digest to detect whether the description was modified after creation,
guarding against silent tampering between planning and implementation phases.

## Marker String

The digest comment uses this exact marker prefix so consumers can locate it among
all issue comments:

```
[sdlc-workflow] Description digest:
```

The full comment body is a single line with a format-tagged digest:

```
[sdlc-workflow] Description digest: sha256-adf:<hex-digest>
```

or

```
[sdlc-workflow] Description digest: sha256-md:<hex-digest>
```

The tag (`adf` or `md`) identifies which description format was hashed, so the
consumer can verify using the same format. See **Hashing** below.

## Tool-Based Computation

Use the `scripts/sha256-digest.py` script to compute the digest. The script
auto-detects the input format and outputs a format-tagged digest:

- **ADF JSON input** → `sha256-adf:<64-char-hex>` (parses JSON, re-serializes
  with compact separators, hashes)
- **Plain text input** (markdown) → `sha256-md:<64-char-hex>` (strips
  leading/trailing whitespace, hashes)

**Usage:**

```bash
# From a file
python3 scripts/sha256-digest.py /tmp/desc.txt

# From stdin
cat /tmp/desc.txt | python3 scripts/sha256-digest.py
```

The script exits non-zero with an error message on stderr if the input is empty.
Always check the exit code before using the output.

The format tag in the output tells the consumer which representation was hashed,
so it can fetch the description in the same format for verification. This
eliminates cross-format mismatches when the producer and consumer use different
Jira access methods (MCP returns markdown, REST API returns ADF JSON).

## Hashing

- **Algorithm:** SHA-256
- **Format awareness:** The Jira API returns the description in different formats
  depending on the access method — MCP returns markdown text, REST API v3 returns
  ADF JSON. These are different representations of the same content and produce
  different hashes. The digest is tagged with the format used (`sha256-adf` or
  `sha256-md`) so the consumer knows which format to verify against.
- **Normalization per format:**
  - **ADF JSON** (REST API path): parse as JSON and re-serialize with compact
    separators (`json.dumps(parsed, separators=(',', ':'))`)
  - **Markdown text** (MCP path): strip leading and trailing whitespace
- **Output:** Format-tagged digest — `sha256-adf:<64-char-hex>` or
  `sha256-md:<64-char-hex>`
- **Computation:** Always use `scripts/sha256-digest.py` — see **Tool-Based
  Computation** above. Do not compute SHA-256 manually. Do not hash the
  description string passed to `create_issue` — always re-fetch from the API
  after creation, since Jira normalizes content during storage.

The producer computes the hash by re-fetching the description from the Jira API
immediately after creating the issue. The script auto-detects the format and
produces the appropriate tagged digest.

## Jira Comment Format

Post a comment on the created issue using ADF `contentFormat`. The comment body is
a single paragraph containing the marker and digest:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "[sdlc-workflow] Description digest: <tagged-digest>"
        }
      ]
    }
  ]
}
```

Replace `<tagged-digest>` with the full output from `scripts/sha256-digest.py`
(e.g., `sha256-md:a1b2...` or `sha256-adf:a1b2...`). The tag is part of the
digest value — do not strip it.

This comment is separate from the skill's standard footnote comment. Post it as an
independent comment — do not append it to the plan summary comment or any other
comment.

## Consumer Verification

The consumer (implement-task) retrieves issue comments and searches for those whose
body starts with the marker string `[sdlc-workflow] Description digest:`.

### Multiple Digest Comments

If multiple comments match the marker string (e.g., from plan-feature re-runs or
manual postings), the consumer must select the most recent one by `created`
timestamp. This ensures deterministic behavior without rejecting valid re-planning
scenarios.

If found:

1. Extract the tagged digest value (e.g., `sha256-md:a1b2...` or
   `sha256-adf:a1b2...`). Parse the format tag (`md` or `adf`) and the hex digest.
2. Fetch the current description from `jira.get_issue`, write it to a temp file,
   and compute the digest using `scripts/sha256-digest.py`. The script auto-detects
   the format and outputs a tagged digest.
3. **Compare format tags first:**
   - **Tags match** (e.g., both `sha256-md`) — compare the hex digests directly.
   - **Tags differ** (e.g., stored is `sha256-adf`, computed is `sha256-md`) —
     the producer and consumer used different Jira access methods. Log a warning:
     "Digest format mismatch (stored: `<tag>`, current: `<tag>`) — producer and
     consumer used different API access methods. Skipping integrity check."
     Proceed normally without blocking.
4. **Compare hex digests** (when tags match):
   - **Match:** proceed normally — description is unmodified since planning.
   - **Mismatch:** warn the user that the task description was modified after
     planning. Display the expected vs actual digest and ask whether to proceed
     or abort. Do not silently continue.

### Legacy Digest Format

Digest comments created before the format-tag enhancement use the untagged format
`sha256:<hex-digest>`. When the consumer encounters an untagged digest, treat it
as a legacy digest — log a warning ("Legacy digest format detected — skipping
integrity check") and proceed normally. Do not attempt to match an untagged digest
against a tagged one.

### Comment Edit Detection

After locating the digest comment, check whether it was edited after posting by
comparing the comment's `created` and `updated` timestamps (both are returned by
the Jira REST API on every comment object):

1. If `updated` equals `created` — the comment is unmodified; proceed with digest
   comparison as above
2. If `updated` is later than `created` — the comment was edited after initial
   posting. Warn: "Digest comment was edited after initial posting — integrity
   cannot be fully guaranteed." Proceed with digest comparison but surface the
   warning to the user alongside any match/mismatch result
3. If the API response does not include `created`/`updated` fields (e.g., the MCP
   tool omits them) — skip this check silently and proceed with digest comparison
   only

This is a defense-in-depth measure. It detects the case where an attacker modifies
both the task description and the digest comment to match. Timestamp manipulation
by a Jira admin would bypass this check, but it raises the bar for casual tampering.

## Backward Compatibility

Tasks created before this protocol was introduced will not have a digest comment.
When the consumer finds no comment matching the marker string:

- Log a warning: "No description digest found — skipping integrity check. This task
  may have been created before digest tracking was introduced."
- Proceed with implementation normally — do not block execution.

## Rules

- Producers must post the digest comment immediately after creating the task issue,
  before creating issue links or other comments
- The digest comment must be a standalone comment, not embedded in other comments
- Consumers must treat a missing digest as a non-blocking warning, not an error
- Consumers should check digest comment `created` vs `updated` timestamps when
  available, and warn if the comment was edited — but proceed regardless
- The marker string is fixed — do not vary it per skill or per invocation

## Common Mistakes — Do NOT

The following mistakes have been observed in practice and must be avoided:

- **Do NOT use placeholder text.** The `<hex-digest>` in the marker template is a
  placeholder — replace it with the actual computed hash. Never post a comment
  containing the literal string `<hex-digest>`, `<hex>`, `sha256:placeholder`, or
  any other stand-in text.
- **Do NOT use abbreviated hashes.** A SHA-256 digest is exactly 64 lowercase
  hexadecimal characters. Values like `sha256:a1b2c3d4e5f6` (12 chars) or
  `sha256:abc123` (6 chars) are wrong. Always output the full 64-character digest.
- **Do NOT use example or hardcoded hashes.** Every digest must be freshly computed
  from the actual description content. Never copy a hash from documentation,
  examples, or a previous task.
- **Do NOT add extra text to the marker line.** The comment body must be exactly
  one line: `[sdlc-workflow] Description digest: sha256-md:<64-char-hex>` (or
  `sha256-adf:<64-char-hex>`). Do not append explanations, timestamps, or metadata
  after the hash.
- **Do NOT strip the format tag.** The output from `scripts/sha256-digest.py`
  includes the tag (`sha256-md:` or `sha256-adf:`). Post the full tagged value —
  the consumer needs the tag to know which format to verify against.
