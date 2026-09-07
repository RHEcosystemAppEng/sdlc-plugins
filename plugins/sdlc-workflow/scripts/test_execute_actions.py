#!/usr/bin/env python3
"""Tests for execute-actions.py ref resolution and native Jira comment posting."""

import sys
import os
import json
import tempfile
import importlib.util

from jsonschema import validate, ValidationError

script_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "execute_actions",
    os.path.join(script_dir, "execute-actions.py"),
)
execute_actions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(execute_actions)

resolve_refs = execute_actions.resolve_refs

# The result schema the fullsend validation_loop enforces before the post_script
# runs. Loaded once so the schema-validation tests below assert against the real
# shipped constraints rather than a reimplementation.
_RESULT_SCHEMA_PATH = os.path.join(
    script_dir, "..", "schemas", "verify-pr-result.schema.json"
)
with open(_RESULT_SCHEMA_PATH) as _schema_f:
    _RESULT_SCHEMA = json.load(_schema_f)

# Validate a single action instance against the schema's action definition. The
# action def carries no external $refs, so wrapping it with the document's $defs
# and dialect lets `validate` exercise the post_comment if/then branch directly.
_ACTION_SCHEMA = {
    "$schema": _RESULT_SCHEMA["$schema"],
    "$defs": _RESULT_SCHEMA["$defs"],
    "$ref": "#/$defs/action",
}


def test_resolve_refs_replaces_key():
    """A single {{ref.key}}/{{ref.url}} pair resolves to registered values."""
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "Sub-task [{{subtask-1.key}}]({{subtask-1.url}}) created."
    result = resolve_refs(text, registry)
    assert result == "Sub-task [TC-100](https://jira.example.com/browse/TC-100) created.", f"Got: {result}"


def test_resolve_refs_no_placeholders():
    """Text without placeholders is returned unchanged."""
    registry = {}
    text = "No placeholders here."
    result = resolve_refs(text, registry)
    assert result == "No placeholders here."


def test_resolve_refs_unknown_ref_raises():
    """An unregistered ref raises KeyError."""
    registry = {}
    text = "{{unknown-ref.key}}"
    try:
        resolve_refs(text, registry)
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_resolve_refs_in_adf():
    """resolve_refs_in_obj resolves placeholders nested inside an ADF doc."""
    registry = {"rc-1": {"key": "TC-200", "url": "https://jira.example.com/browse/TC-200"}}
    adf = {
        "type": "doc",
        "content": [
            {"type": "text", "text": "Task {{rc-1.key}} created"}
        ]
    }
    result = execute_actions.resolve_refs_in_obj(adf, registry)
    assert result["content"][0]["text"] == "Task TC-200 created"


def test_resolve_refs_multiple_different_refs():
    """Multiple distinct refs in one string each resolve independently."""
    registry = {
        "subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"},
        "rc-1": {"key": "TC-200", "url": "https://jira.example.com/browse/TC-200"},
    }
    text = "Sub-task {{subtask-1.key}} and root-cause {{rc-1.key}} ({{rc-1.url}})."
    result = resolve_refs(text, registry)
    assert result == "Sub-task TC-100 and root-cause TC-200 (https://jira.example.com/browse/TC-200).", f"Got: {result}"


def test_resolve_refs_repeated_placeholder():
    """A placeholder repeated in one string resolves at every occurrence."""
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "{{subtask-1.key}} depends on {{subtask-1.key}}."
    result = resolve_refs(text, registry)
    assert result == "TC-100 depends on TC-100.", f"Got: {result}"


def test_resolve_refs_mixed_key_url_same_ref():
    """The .key and .url fields of one ref resolve to their respective values."""
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "See {{subtask-1.key}} at {{subtask-1.url}}; {{subtask-1.key}} must be done first."
    result = resolve_refs(text, registry)
    assert result == "See TC-100 at https://jira.example.com/browse/TC-100; TC-100 must be done first.", f"Got: {result}"


class _FakeCompleted:
    """Stand-in for subprocess.CompletedProcess."""

    def __init__(self, returncode=0, stderr="", stdout=""):
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout


class _RunRecorder:
    """Captures the argv/input/env of a single subprocess.run call."""

    def __init__(self, returncode=0, stderr=""):
        self.returncode = returncode
        self.stderr = stderr
        self.cmd = None
        self.input = None
        self.env = None

    def __call__(self, cmd, input=None, text=None, capture_output=None, env=None):
        self.cmd = cmd
        self.input = input
        self.env = env
        return _FakeCompleted(self.returncode, self.stderr)


_JIRA_ENV = {
    "JIRA_SERVER_URL": "https://jira.example.com",
    "JIRA_EMAIL": "bot@example.com",
    "JIRA_API_TOKEN": "s3cr3t",
}


def _with_jira_env_and_recorder(recorder):
    """Install a fake subprocess.run + Jira env; return a restore callback."""
    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = recorder
    os.environ.update(_JIRA_ENV)

    def restore():
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    return restore


def test_post_jira_comment_native_builds_argv():
    """post_jira_comment_native calls the native CLI with marker, project, and number."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC-321", "hello **world**")
    finally:
        restore()

    assert recorder.cmd[:4] == ["fullsend", "issues", "post-comment", "--tracker"], f"Got: {recorder.cmd}"
    assert "jira" in recorder.cmd
    assert "--project" in recorder.cmd and recorder.cmd[recorder.cmd.index("--project") + 1] == "TC"
    assert "--number" in recorder.cmd and recorder.cmd[recorder.cmd.index("--number") + 1] == "321"
    assert "--marker" in recorder.cmd
    assert recorder.cmd[recorder.cmd.index("--marker") + 1] == execute_actions.STICKY_COMMENT_MARKER
    assert "--result" in recorder.cmd and recorder.cmd[recorder.cmd.index("--result") + 1] == "-"
    assert recorder.input == "hello **world**"


def test_post_jira_comment_native_maps_env():
    """The native CLI receives JIRA_BASE_URL/JIRA_USER_EMAIL/JIRA_TOKEN mapped from this script's vars."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC-1", "body")
    finally:
        restore()

    assert recorder.env["JIRA_BASE_URL"] == "https://jira.example.com"
    assert recorder.env["JIRA_USER_EMAIL"] == "bot@example.com"
    assert recorder.env["JIRA_TOKEN"] == "s3cr3t"


def test_post_jira_comment_native_nonzero_exits():
    """A non-zero CLI exit aborts with sys.exit(1)."""
    recorder = _RunRecorder(returncode=1, stderr="boom")
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC-1", "body")
        assert False, "Should have exited"
    except SystemExit as e:
        assert e.code == 1
    finally:
        restore()


def test_post_jira_comment_native_invalid_key_exits():
    """A malformed issue key (no hyphen) aborts before invoking the CLI."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC123", "body")
        assert False, "Should have exited"
    except SystemExit as e:
        assert e.code == 1
    finally:
        restore()
    assert recorder.cmd is None, "CLI should not run for an invalid key"


def test_schema_post_comment_accepts_valid_jira_key():
    """The post_comment schema accepts a well-formed hyphenated Jira key so a
    legitimate action still validates and routes to the native CLI."""
    # Given a post_comment action whose issue is a valid Jira key
    action = {"type": "post_comment", "issue": "TC-5811", "body_adf": {}}
    # When validating it against the result schema's action definition
    # Then validation passes (validate raises ValidationError on failure)
    validate(instance=action, schema=_ACTION_SCHEMA)


def test_schema_post_comment_accepts_ref_key_placeholder():
    """The post_comment schema accepts a {{<ref>.key}} placeholder so a comment
    targeting an issue created by an earlier action (which execute_post_comment
    resolves via resolve_refs) survives fullsend's validation_loop instead of
    being rejected before the reference can be resolved."""
    # Given a post_comment action whose issue is a {{<ref>.key}} placeholder
    action = {"type": "post_comment", "issue": "{{sub-1.key}}", "body_adf": {}}
    # When validating it against the result schema's action definition
    # Then validation passes (validate raises ValidationError on failure)
    validate(instance=action, schema=_ACTION_SCHEMA)


def test_schema_post_comment_rejects_non_key_issue():
    """A schema-valid-string-but-non-key issue (numeric ID, URL, lowercase,
    missing hyphen, or a non-.key placeholder) is rejected at validation, so it
    can never pass the producer boundary only to hit the executor's rpartition
    guard and sys.exit(1)."""
    # Given post_comment actions whose issue is neither a hyphenated Jira key
    # nor a {{<ref>.key}} placeholder
    non_keys = [
        "12345",                                        # numeric Jira ID
        "https://jira.example.com/browse/TC-5811",      # URL
        "tc-5811",                                      # lowercase project
        "TC5811",                                       # missing hyphen
        "TC-",                                          # missing number
        "-5811",                                        # missing project
        "{{sub-1.url}}",                                # .url placeholder (not a key)
        "{{SUB.key}}",                                  # uppercase ref name
        "{{sub-1.status}}",                             # unsupported placeholder attr
        "sub-1.key",                                    # missing braces
        "prefix {{sub-1.key}}",                         # placeholder not anchored
    ]
    for issue in non_keys:
        action = {"type": "post_comment", "issue": issue, "body_adf": {}}
        # When validating each against the schema
        # Then validation fails before the action can reach the executor
        try:
            validate(instance=action, schema=_ACTION_SCHEMA)
            assert False, f"non-key issue should be rejected: {issue!r}"
        except ValidationError:
            pass


def test_adf_to_markdown_renders_blocks_and_marks():
    """adf_to_markdown renders headings, lists, code blocks, rules, and inline marks."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "heading", "attrs": {"level": 2},
             "content": [{"type": "text", "text": "Title"}]},
            {"type": "paragraph", "content": [
                {"type": "text", "text": "See "},
                {"type": "text", "text": "TC-1", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " and "},
                {"type": "text", "text": "run", "marks": [{"type": "code"}]},
                {"type": "text", "text": " at "},
                {"type": "text", "text": "here",
                 "marks": [{"type": "link", "attrs": {"href": "https://x.example/y"}}]},
            ]},
            {"type": "bulletList", "content": [
                {"type": "listItem", "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": "first"}]}]},
                {"type": "listItem", "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": "second"}]}]},
            ]},
            {"type": "rule"},
            {"type": "codeBlock", "attrs": {"language": "python"},
             "content": [{"type": "text", "text": "x = 1"}]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    expected = (
        "## Title\n\n"
        "See **TC-1** and `run` at [here](https://x.example/y)\n\n"
        "- first\n- second\n\n"
        "---\n\n"
        "```python\nx = 1\n```"
    )
    assert result == expected, f"Got: {result!r}"


def test_adf_to_markdown_renders_task_list():
    """adf_to_markdown renders taskList DONE/TODO items as - [x] / - [ ] markers, for both paragraph-wrapped and inline taskItem content."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "taskList", "content": [
                {"type": "taskItem", "attrs": {"state": "DONE"}, "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": "done item"}]}]},
                {"type": "taskItem", "attrs": {"state": "TODO"}, "content": [
                    {"type": "text", "text": "todo item"}]},
            ]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == "- [x] done item\n- [ ] todo item", f"Got: {result!r}"


def test_adf_to_markdown_escapes_markdown_active_chars_in_literal_text():
    """Literal markdown-active characters in a plain text node are backslash-escaped
    so the native CLI renders them verbatim instead of reinterpreting them as
    formatting."""
    # Given a paragraph whose literal text contains * _ [ ] and a backtick
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "text", "text": "a*b_c[d]e`f"},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then each active character is escaped with a leading backslash
    assert result == "a\\*b\\_c\\[d\\]e\\`f", f"Got: {result!r}"


def test_adf_to_markdown_does_not_double_escape_marks_or_code():
    """Intentional marks (strong/link) and inline code render correctly: the mark
    syntax the renderer adds is not escaped, inline-code content stays literal, and
    link hrefs are not escaped."""
    # Given marked text, an inline-code span containing an asterisk, and a link
    # whose href contains an underscore
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "text", "text": "bold", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " and "},
                {"type": "text", "text": "a*b", "marks": [{"type": "code"}]},
                {"type": "text", "text": " see "},
                {"type": "text", "text": "here",
                 "marks": [{"type": "link", "attrs": {"href": "https://x.example/a_b"}}]},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then the ** stays, the code asterisk stays literal, and the href underscore
    # is preserved (none are escaped)
    assert result == "**bold** and `a*b` see [here](https://x.example/a_b)", f"Got: {result!r}"


def test_adf_to_markdown_escapes_line_leading_block_markers():
    """A paragraph whose literal text begins with a Markdown block marker
    (heading/bullet/blockquote/ordered-list) has that marker backslash-escaped so
    the native CLI renders it verbatim instead of re-parsing it as a block."""
    # Given paragraphs each starting with a different line-leading block marker
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": "# not a heading"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "### also not"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "- not a bullet"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "+ not a bullet"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "> not a quote"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "1. not ordered"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "2) not ordered"}]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then the leading marker of each line is escaped (heading/bullet/quote escape
    # the first char; ordered lists escape the . / ) separator)
    assert result == (
        "\\# not a heading\n\n"
        "\\### also not\n\n"
        "\\- not a bullet\n\n"
        "\\+ not a bullet\n\n"
        "\\> not a quote\n\n"
        "1\\. not ordered\n\n"
        "2\\) not ordered"
    ), f"Got: {result!r}"


def test_adf_to_markdown_escapes_line_leading_marker_after_hardbreak():
    """A block marker that starts a line *after* a hardBreak inside a paragraph is
    escaped too, since it is at a real line start once rendered."""
    # Given a paragraph with a hardBreak followed by text starting with "# "
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "text", "text": "see:"},
                {"type": "hardBreak"},
                {"type": "text", "text": "# heading"},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then only the post-hardBreak line-leading marker is escaped
    assert result == "see:\n\\# heading", f"Got: {result!r}"


def test_adf_to_markdown_does_not_escape_midline_or_non_marker_text():
    """Escaping is line-position-sensitive: a marker char mid-line, or a
    marker-like prefix that does not actually form a block (no trailing space, a
    heading start intentionally emitted by the heading renderer), is left alone."""
    # Given a heading node, a paragraph with a mid-line '#', and paragraphs whose
    # leading chars do not form a block construct ("-5", "1.5" have no space)
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "heading", "attrs": {"level": 2},
             "content": [{"type": "text", "text": "Real Heading"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "not # a heading"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "-5 degrees"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "1.5 times"}]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then the real heading keeps its intentional prefix and nothing else is escaped
    assert result == (
        "## Real Heading\n\n"
        "not # a heading\n\n"
        "-5 degrees\n\n"
        "1.5 times"
    ), f"Got: {result!r}"


def test_adf_to_markdown_renders_non_text_inline_nodes():
    """Each non-text inline leaf node (mention/emoji/inlineCard/date/status)
    renders its attrs-sourced displayable value instead of being dropped to an
    empty string."""
    # Given a paragraph containing one of each non-text inline leaf type, with
    # an underscore in the inlineCard URL (URLs must not be escaped) and an
    # epoch-millisecond date timestamp for 2021-01-01 UTC
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "mention", "attrs": {"id": "abc", "text": "@Marco Rizzi"}},
                {"type": "text", "text": " "},
                {"type": "emoji", "attrs": {"shortName": ":smile:", "text": "😄"}},
                {"type": "text", "text": " "},
                {"type": "inlineCard", "attrs": {"url": "https://example.com/a_b"}},
                {"type": "text", "text": " "},
                {"type": "date", "attrs": {"timestamp": "1609459200000"}},
                {"type": "text", "text": " "},
                {"type": "status", "attrs": {"text": "In Progress", "color": "yellow"}},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then every node contributes its attrs value (URL underscore preserved, date
    # formatted as YYYY-MM-DD) and nothing is silently dropped
    assert result == "@Marco Rizzi 😄 https://example.com/a_b 2021-01-01 In Progress", \
        f"Got: {result!r}"


def test_adf_to_markdown_renders_inline_nodes_in_task_item():
    """A taskItem whose inline content mixes text with a mention and an
    inlineCard renders all of them — the inline nodes are not dropped in the
    taskItem context."""
    # Given a TODO taskItem with inline mention and inlineCard nodes
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "taskList", "content": [
                {"type": "taskItem", "attrs": {"state": "TODO"}, "content": [
                    {"type": "text", "text": "ping "},
                    {"type": "mention", "attrs": {"text": "@dev"}},
                    {"type": "text", "text": " re "},
                    {"type": "inlineCard", "attrs": {"url": "https://example.com/pr/1"}},
                ]},
            ]},
        ],
    }
    # When rendering the ADF to markdown
    result = execute_actions.adf_to_markdown(doc)
    # Then the checklist item retains the mention and inlineCard values
    assert result == "- [ ] ping @dev re https://example.com/pr/1", f"Got: {result!r}"


def test_adf_to_markdown_renders_table():
    """A table renders as a GFM table: first tableRow is the header (with a ---
    separator), tableCell/tableHeader content is rendered, and literal pipes in a
    cell are escaped so they do not break the column grid."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "table", "content": [
                {"type": "tableRow", "content": [
                    {"type": "tableHeader", "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "Name"}]}]},
                    {"type": "tableHeader", "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "Note"}]}]},
                ]},
                {"type": "tableRow", "content": [
                    {"type": "tableCell", "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "a"}]}]},
                    {"type": "tableCell", "content": [
                        {"type": "paragraph", "content": [{"type": "text", "text": "b|c"}]}]},
                ]},
            ]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == (
        "| Name | Note |\n"
        "| --- | --- |\n"
        "| a | b\\|c |"
    ), f"Got: {result!r}"


def test_adf_to_markdown_renders_blockquote_and_panel():
    """blockquote renders as > -prefixed lines; a panel renders as a quote with a
    bold panelType label so its kind is preserved."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "blockquote", "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "quoted"}]}]},
            {"type": "panel", "attrs": {"panelType": "info"}, "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "heads up"}]}]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == (
        "> quoted\n"
        "\n"
        "> **info**\n"
        ">\n"
        "> heads up"
    ), f"Got: {result!r}"


def test_adf_to_markdown_renders_media_instead_of_dropping():
    """media/mediaSingle render a non-empty image link (or [alt] placeholder when
    no URL is present) rather than being silently dropped — media nodes have no
    text content, so the pre-fix flattening fallback emitted nothing."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "mediaSingle", "content": [
                {"type": "media", "attrs": {"url": "https://ex.com/i.png", "alt": "chart"}}]},
            {"type": "mediaSingle", "content": [
                {"type": "media", "attrs": {"type": "file", "id": "abc-123"}}]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == "![chart](https://ex.com/i.png)\n\n[abc-123]", f"Got: {result!r}"


def test_adf_to_markdown_unknown_block_still_flattens():
    """A genuinely unknown container block still degrades gracefully by recursing
    into its nested content (the preserved fallback), so the fix does not regress
    forward-compat handling of block nodes it does not explicitly cover."""
    doc = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "someFutureBlock", "content": [
                {"type": "paragraph", "content": [{"type": "text", "text": "still here"}]}]},
        ],
    }
    result = execute_actions.adf_to_markdown(doc)
    assert result == "still here", f"Got: {result!r}"


def test_render_adf_date_falls_back_on_out_of_range_timestamp():
    """An integer-parseable but out-of-range epoch-ms timestamp renders as its
    literal string instead of raising, so a single malformed date node cannot
    abort the whole post_script. datetime.fromtimestamp raises OverflowError/OSError
    (or ValueError) for out-of-range values, and that call now sits inside the
    guarded try; before the fix it was outside and any such exception propagated."""
    # Given an integer-parseable epoch-millisecond value far outside the
    # representable datetime range
    out_of_range = "99999999999999999"
    # When rendering it as an ADF date node
    result = execute_actions._render_adf_date(out_of_range)
    # Then the literal value is returned and no exception propagates
    assert result == out_of_range, f"Got: {result!r}"


# A report's tracker-native body. execute_post_report renders this (not the
# GitHub-only report_md) to markdown for Jira via adf_to_markdown, so the fixtures
# below give it text that renders to a string distinct from report_md — proving
# Jira receives the ADF-derived body while GitHub keeps report_md + its marker.
_REPORT_ADF = {
    "type": "doc",
    "version": 1,
    "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": "Jira native body."}]}
    ],
}
_REPORT_ADF_MD = "Jira native body."


def test_execute_post_comment_routes_to_native():
    """execute_post_comment resolves refs in body_adf, renders to markdown, and posts it."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    registry = {"sub-1": {"key": "TC-500", "url": "https://jira.example.com/browse/TC-500"}}
    body_adf = {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [
                {"type": "text", "text": "See "},
                {"type": "text", "text": "{{sub-1.key}}", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " at "},
                {"type": "text", "text": "link",
                 "marks": [{"type": "link", "attrs": {"href": "{{sub-1.url}}"}}]},
            ]},
        ],
    }
    try:
        execute_actions.execute_post_comment(
            {"type": "post_comment", "issue": "{{sub-1.key}}", "body_adf": body_adf},
            registry,
        )
    finally:
        restore()

    assert recorder.cmd[recorder.cmd.index("--number") + 1] == "500"
    assert recorder.input == "See **TC-500** at [link](https://jira.example.com/browse/TC-500)", \
        f"Got: {recorder.input!r}"


def test_post_comment_and_report_use_distinct_sticky_markers():
    """A post_comment and a post_report pass DIFFERENT --marker values to the
    native CLI, so two sticky comments on the same Jira issue never share one
    marker identity and clobber each other."""
    # Given the comment path
    comment_recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(comment_recorder)
    try:
        execute_actions.execute_post_comment(
            {"type": "post_comment", "issue": "TC-777",
             "body_adf": {"type": "doc", "version": 1, "content": []}},
            {},
        )
    finally:
        restore()
    comment_marker = comment_recorder.cmd[comment_recorder.cmd.index("--marker") + 1]

    # And the report path (native GitHub comment + native Jira comment)
    report_calls = []

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        report_calls.append(cmd)
        return _FakeCompleted(0, "")

    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    os.environ.update(_JIRA_ENV)
    try:
        report = {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": "946556e",
            "report_md": "## Verify report",
            "report_adf": _REPORT_ADF,
        }
        execute_actions.execute_post_report({"type": "post_report"}, {}, report)
    finally:
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    jira_cmd = next(c for c in report_calls
                    if c[:3] == ["fullsend", "issues", "post-comment"]
                    and c[c.index("--tracker") + 1] == "jira")
    report_marker = jira_cmd[jira_cmd.index("--marker") + 1]

    # Then the two markers differ, and each matches its dedicated constant
    assert comment_marker == execute_actions.POST_COMMENT_STICKY_MARKER
    assert report_marker == execute_actions.STICKY_COMMENT_MARKER
    assert comment_marker != report_marker, "post_comment and post_report must use distinct markers"


def test_execute_post_report_posts_github_then_jira():
    """execute_post_report posts the report to the GitHub PR then to Jira, both via
    the native `fullsend issues post-comment` sticky CLI (GitHub first)."""
    calls = []

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        calls.append({"cmd": cmd, "input": input, "env": env})
        return _FakeCompleted(0, "")

    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    os.environ.update(_JIRA_ENV)
    try:
        report = {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": "946556e",
            "report_md": "## Verify report\nAll good.",
            "report_adf": _REPORT_ADF,
        }
        execute_actions.execute_post_report({"type": "post_report"}, {}, report)
    finally:
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    # SHA canonicalization (git rev-parse) + native GitHub + native Jira.
    assert len(calls) == 3, f"Expected rev-parse + github + jira calls, got {len(calls)}"
    native = [c for c in calls if c["cmd"][:3] == ["fullsend", "issues", "post-comment"]]
    gh_call = next(c for c in native if c["cmd"][c["cmd"].index("--tracker") + 1] == "github")
    jira_call = next(c for c in native if c["cmd"][c["cmd"].index("--tracker") + 1] == "jira")
    # GitHub side: native sticky CLI targets the PR by number, the marker carries
    # the commit SHA, and the body (stdin) is report_md with NO embedded marker
    # (the CLI prepends it).
    assert gh_call["cmd"][gh_call["cmd"].index("--project") + 1] == "acme/widget"
    assert gh_call["cmd"][gh_call["cmd"].index("--number") + 1] == "42"
    assert gh_call["cmd"][gh_call["cmd"].index("--marker") + 1] == \
        "<!-- sdlc-workflow:verify-pr report commit:946556e -->"
    assert gh_call["input"] == "## Verify report\nAll good."
    assert "sdlc-workflow:verify-pr report commit:" not in gh_call["input"], \
        "marker must not be embedded in the GitHub body; the CLI prepends it"
    # GitHub is posted before Jira.
    assert native[0] is gh_call, "GitHub report must be posted before Jira"
    # Jira side: sticky CLI, and the body is rendered from report_adf (the
    # tracker-native content) via adf_to_markdown, NOT the GitHub-only report_md,
    # which carries the commit marker Jira must never receive.
    assert jira_call["cmd"][jira_call["cmd"].index("--number") + 1] == "777"
    assert jira_call["input"] == _REPORT_ADF_MD
    assert jira_call["input"] != report["report_md"], "Jira must not receive report_md"
    assert "sdlc-workflow:verify-pr report commit:" not in jira_call["input"]


def test_execute_post_report_strips_embedded_leading_marker_from_github_body():
    """When the agent's report_md already begins with the commit-scoped marker
    line, execute_post_report strips it before calling the native CLI (which
    prepends the marker), so the GitHub comment never opens with two duplicate
    marker lines."""
    calls = []

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        calls.append({"cmd": cmd, "input": input})
        return _FakeCompleted(0, "")

    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    os.environ.update(_JIRA_ENV)
    try:
        marker_line = "<!-- sdlc-workflow:verify-pr report commit:946556e -->"
        report = {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": "946556e",
            "report_md": f"{marker_line}\n## Verify report\nAll good.",
            "report_adf": _REPORT_ADF,
        }
        execute_actions.execute_post_report({"type": "post_report"}, {}, report)
    finally:
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    gh_call = next(c for c in calls
                   if c["cmd"][:3] == ["fullsend", "issues", "post-comment"]
                   and c["cmd"][c["cmd"].index("--tracker") + 1] == "github")
    # The leading marker line is stripped; the body starts with the report heading
    # and carries no embedded marker (the CLI prepends the single marker copy).
    assert gh_call["input"] == "## Verify report\nAll good.", f"Got: {gh_call['input']!r}"
    assert "sdlc-workflow:verify-pr report commit:" not in gh_call["input"]


def _run_post_report_with_sha_resolution(commit_sha, resolve):
    """Run execute_post_report with a fake ``git rev-parse`` that maps each input
    ref to a canonical full SHA via ``resolve``. Returns the recorded calls."""
    calls = []

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        calls.append({"cmd": cmd, "input": input})
        if cmd[:2] == ["git", "rev-parse"]:
            # cmd[-1] is "<ref>^{commit}"; strip the peel suffix to look up.
            ref = cmd[-1].split("^", 1)[0]
            return _FakeCompleted(0, "", resolve.get(ref, ""))
        return _FakeCompleted(0, "")

    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    os.environ.update(_JIRA_ENV)
    try:
        report = {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": commit_sha,
            "report_md": "## Verify report",
            "report_adf": _REPORT_ADF,
        }
        execute_actions.execute_post_report({"type": "post_report"}, {}, report)
    finally:
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return calls


def _github_marker_from_calls(calls):
    """Return the --marker passed to the native GitHub post-comment call."""
    gh = next(c for c in calls
              if c["cmd"][:3] == ["fullsend", "issues", "post-comment"]
              and c["cmd"][c["cmd"].index("--tracker") + 1] == "github")
    return gh["cmd"][gh["cmd"].index("--marker") + 1]


def test_execute_post_report_dedup_marker_invariant_to_sha_length():
    """A full-length SHA and an abbreviated SHA for the SAME commit produce the
    SAME --marker on the native GitHub call, because git rev-parse canonicalizes
    both forms to the same full SHA. The native CLI then deduplicates on that
    shared marker, so a retry edits one comment instead of duplicating it."""
    full_sha = "946556e" + "a" * 33   # 40 hex chars
    short_sha = "946556e"             # 7-char abbreviation of the same commit
    # git rev-parse resolves either form of this one commit to its full SHA.
    resolve = {full_sha: full_sha, short_sha: full_sha}

    full_marker = _github_marker_from_calls(
        _run_post_report_with_sha_resolution(full_sha, resolve))
    short_marker = _github_marker_from_calls(
        _run_post_report_with_sha_resolution(short_sha, resolve))

    assert full_marker == f"{execute_actions.GITHUB_REPORT_MARKER_PREFIX}{full_sha} -->", \
        f"marker should carry the canonical full SHA: {full_marker!r}"
    assert full_marker == short_marker, \
        "full and abbreviated SHA of one commit must yield the same sticky marker"


def test_execute_post_report_distinct_commits_same_prefix_do_not_collide():
    """Two distinct commits sharing a 7-hex prefix get DISTINCT --marker values
    (each resolved up to its full 40-char SHA), so the native CLI keeps them as
    separate sticky comments instead of one overwriting the other."""
    full_a = "946556e" + "a" * 33   # commit A
    full_b = "946556e" + "b" * 33   # commit B, same first 7 hex chars, distinct object
    resolve = {full_a: full_a, full_b: full_b}

    marker_a = _github_marker_from_calls(
        _run_post_report_with_sha_resolution(full_a, resolve))
    marker_b = _github_marker_from_calls(
        _run_post_report_with_sha_resolution(full_b, resolve))

    assert marker_a == f"{execute_actions.GITHUB_REPORT_MARKER_PREFIX}{full_a} -->"
    assert marker_b == f"{execute_actions.GITHUB_REPORT_MARKER_PREFIX}{full_b} -->"
    assert marker_a != marker_b, "distinct commits must get distinct sticky markers"


def test_normalize_commit_sha_falls_back_to_prefix_when_unresolvable():
    """When git cannot resolve the SHA (git missing or object absent),
    _normalize_commit_sha falls back to the fixed-length prefix so dedup keeps
    working instead of being disabled."""
    long_sha = "946556e" + "f" * 33

    # git rev-parse reports failure (non-zero, empty stdout) → fallback to prefix.
    def failing_run(cmd, input=None, text=None, capture_output=None, env=None):
        return _FakeCompleted(1, "fatal: Needed a single revision", "")

    saved_run = execute_actions.subprocess.run
    execute_actions.subprocess.run = failing_run
    try:
        result = execute_actions._normalize_commit_sha(long_sha)
    finally:
        execute_actions.subprocess.run = saved_run
    assert result == long_sha[:execute_actions.COMMIT_SHA_MARKER_LENGTH], \
        f"Got: {result!r}"

    # git binary missing (OSError) → same fallback.
    def raising_run(cmd, input=None, text=None, capture_output=None, env=None):
        raise FileNotFoundError("git")

    execute_actions.subprocess.run = raising_run
    try:
        result = execute_actions._normalize_commit_sha(long_sha)
    finally:
        execute_actions.subprocess.run = saved_run
    assert result == long_sha[:execute_actions.COMMIT_SHA_MARKER_LENGTH], \
        f"Got: {result!r}"


def test_post_report_resolves_ref_created_by_later_action():
    """report_md refs resolve regardless of action ordering: a post_report ordered
    BEFORE the create_subtask it references still resolves, because main() defers
    every post_report until after the actions loop populates the registry."""
    calls = []

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        calls.append({"cmd": cmd, "input": input})
        return _FakeCompleted(0, "")

    def fake_create_issue(**kwargs):
        return {"key": "TC-999"}

    # Actions deliberately order post_report FIRST, then the create_subtask whose
    # ref its report_md interpolates — the pre-fix inline order would KeyError.
    data = {
        "report": {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "commit_sha": "946556e",
            "report_md": "Filed sub-task {{sub-1.key}}.",
            "report_adf": {
                "type": "doc",
                "version": 1,
                "content": [
                    {"type": "paragraph",
                     "content": [{"type": "text", "text": "Filed sub-task {{sub-1.key}}."}]}
                ],
            },
        },
        "actions": [
            {"type": "post_report"},
            {
                "type": "create_subtask",
                "ref": "sub-1",
                "parent": "TC-100",
                "summary": "A sub-task",
                "labels": ["review-feedback"],
                "description_adf": {"type": "doc", "version": 1, "content": []},
            },
        ],
    }

    saved_run = execute_actions.subprocess.run
    saved_create = execute_actions._jira_mod.create_issue
    saved_argv = sys.argv
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    execute_actions._jira_mod.create_issue = fake_create_issue
    os.environ.update(_JIRA_ENV)
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        sys.argv = ["execute-actions.py", path]
        execute_actions.main()
    finally:
        execute_actions.subprocess.run = saved_run
        execute_actions._jira_mod.create_issue = saved_create
        sys.argv = saved_argv
        os.remove(path)
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    # The GitHub report body (native call stdin) carries the resolved key, not the
    # raw placeholder.
    native = [c for c in calls if c["cmd"][:3] == ["fullsend", "issues", "post-comment"]]
    gh_call = next(c for c in native if c["cmd"][c["cmd"].index("--tracker") + 1] == "github")
    assert "Filed sub-task TC-999." in gh_call["input"], f"ref not resolved: {gh_call['input']}"
    assert "{{sub-1.key}}" not in gh_call["input"], "placeholder leaked into report body"
    # The Jira body is rendered from report_adf, and its refs resolve too.
    jira_call = next(c for c in native if c["cmd"][c["cmd"].index("--tracker") + 1] == "jira")
    assert jira_call["input"] == "Filed sub-task TC-999.", f"ref not resolved in ADF: {jira_call['input']}"
    assert "{{sub-1.key}}" not in jira_call["input"], "placeholder leaked into Jira body"


if __name__ == "__main__":
    test_resolve_refs_replaces_key()
    test_resolve_refs_no_placeholders()
    test_resolve_refs_unknown_ref_raises()
    test_resolve_refs_in_adf()
    test_resolve_refs_multiple_different_refs()
    test_resolve_refs_repeated_placeholder()
    test_resolve_refs_mixed_key_url_same_ref()
    test_post_jira_comment_native_builds_argv()
    test_post_jira_comment_native_maps_env()
    test_post_jira_comment_native_nonzero_exits()
    test_post_jira_comment_native_invalid_key_exits()
    test_schema_post_comment_accepts_valid_jira_key()
    test_schema_post_comment_accepts_ref_key_placeholder()
    test_schema_post_comment_rejects_non_key_issue()
    test_adf_to_markdown_renders_blocks_and_marks()
    test_adf_to_markdown_renders_task_list()
    test_adf_to_markdown_escapes_markdown_active_chars_in_literal_text()
    test_adf_to_markdown_does_not_double_escape_marks_or_code()
    test_adf_to_markdown_escapes_line_leading_block_markers()
    test_adf_to_markdown_escapes_line_leading_marker_after_hardbreak()
    test_adf_to_markdown_does_not_escape_midline_or_non_marker_text()
    test_adf_to_markdown_renders_non_text_inline_nodes()
    test_adf_to_markdown_renders_inline_nodes_in_task_item()
    test_adf_to_markdown_renders_table()
    test_adf_to_markdown_renders_blockquote_and_panel()
    test_adf_to_markdown_renders_media_instead_of_dropping()
    test_adf_to_markdown_unknown_block_still_flattens()
    test_render_adf_date_falls_back_on_out_of_range_timestamp()
    test_execute_post_comment_routes_to_native()
    test_post_comment_and_report_use_distinct_sticky_markers()
    test_execute_post_report_posts_github_then_jira()
    test_execute_post_report_strips_embedded_leading_marker_from_github_body()
    test_execute_post_report_dedup_marker_invariant_to_sha_length()
    test_execute_post_report_distinct_commits_same_prefix_do_not_collide()
    test_normalize_commit_sha_falls_back_to_prefix_when_unresolvable()
    test_post_report_resolves_ref_created_by_later_action()
    print("All tests passed.")
