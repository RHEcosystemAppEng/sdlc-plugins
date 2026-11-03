"""Skill-eval CI model consistency: both eval workflows must select the same models (TC-7280)."""

import shutil
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]

# Both workflows drive `claude -p` with the run-evals skill; they must agree because
# PR results are compared against the baselines the other workflow produces.
EVAL_WORKFLOWS = [
    ".github/workflows/eval-pr-run.yml",
    ".github/workflows/eval-baseline.yml",
]

# The three model selectors set on the `claude -p` step, with the TC-7274 target values.
TARGET_MODELS = {
    "ANTHROPIC_MODEL": "claude-opus-5-5",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-5-5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-5-5",
}


def eval_step_env(path):
    """Return the env of the step that runs the eval agent (`claude -p`); empty when absent."""
    workflow = yaml.safe_load(path.read_text())
    for job in (workflow.get("jobs") or {}).values():
        for step in (job.get("steps") or []):
            if "claude -p" in (step.get("run") or ""):
                return step.get("env") or {}
    return {}


def model_pins(root):
    """Map each eval workflow to its three ANTHROPIC model vars; unset vars are None."""
    pins = {}
    for rel in EVAL_WORKFLOWS:
        env = eval_step_env(root / rel)
        pins[rel] = {var: env.get(var) for var in TARGET_MODELS}
    return pins


def model_problems(root):
    """List missing vars, non-target models, and cross-workflow disagreement; empty means consistent."""
    pins = model_pins(root)
    problems = []
    for rel, pins_for_workflow in pins.items():
        for var, value in pins_for_workflow.items():
            if not value:
                problems.append(f"{rel}: missing {var}")
            elif value != TARGET_MODELS[var]:
                problems.append(f"{rel}: {var} is {value!r}, expected {TARGET_MODELS[var]!r}")
    for var in TARGET_MODELS:
        values = {rel: pins_for_workflow[var] for rel, pins_for_workflow in pins.items()}
        if len({value for value in values.values() if value}) > 1:
            problems.append(f"{var} disagrees across workflows: {values}")
    return problems


def repo_copy(tmp_path):
    """Copy only the eval workflows into a scratch tree so a test can mutate one safely."""
    for rel in EVAL_WORKFLOWS:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, tmp_path / rel)
    return tmp_path


def test_repository_eval_workflows_pin_target_models():
    """Both eval workflows select the TC-7274 models identically."""
    assert model_problems(ROOT) == []


@pytest.mark.parametrize("rel", EVAL_WORKFLOWS)
@pytest.mark.parametrize("var", sorted(TARGET_MODELS))
def test_single_drifted_var_fails(tmp_path, rel, var):
    """Changing one model var in one workflow is reported as a disagreement."""
    # Given a copy of the workflows where exactly one model var drifts
    root = repo_copy(tmp_path)
    path = root / rel
    original = f'{var}: "{TARGET_MODELS[var]}"'
    assert path.read_text().count(original) == 1
    path.write_text(path.read_text().replace(original, f'{var}: "claude-opus-4-6"'))
    # When the model pins are checked
    problems = model_problems(root)
    # Then both the wrong target and the cross-workflow disagreement are reported
    assert any(p.startswith(f"{var} disagrees across workflows") for p in problems), problems
    assert any(f"{rel}: {var} is 'claude-opus-4-6'" in p for p in problems), problems


@pytest.mark.parametrize("var", sorted(TARGET_MODELS))
def test_missing_var_fails(tmp_path, var):
    """A workflow step without one of the three model selectors fails closed."""
    # Given a workflow whose env no longer sets one model var
    root = repo_copy(tmp_path)
    path = root / ".github/workflows/eval-baseline.yml"
    lines = [line for line in path.read_text().splitlines(keepends=True) if f"{var}:" not in line]
    path.write_text("".join(lines))
    # When the model pins are checked
    problems = model_problems(root)
    # Then the missing selector is reported
    assert f".github/workflows/eval-baseline.yml: missing {var}" in problems, problems


def test_missing_eval_step_fails(tmp_path):
    """Removing the eval step entirely is reported instead of passing vacuously."""
    # Given a workflow with no step that selects a model
    root = repo_copy(tmp_path)
    path = root / ".github/workflows/eval-pr-run.yml"
    path.write_text("name: Eval PR Run\non: {}\njobs: {}\n")
    # When the model pins are checked
    problems = model_problems(root)
    # Then every selector is reported missing for that workflow
    expected = sorted(f".github/workflows/eval-pr-run.yml: missing {var}" for var in TARGET_MODELS)
    assert sorted(problems) == expected
