"""Throwaway failing test for TC-6192 CI-fail acceptance scenario.

Deliberately fails to drive one CI check to a failure conclusion so the
verify-pr dispatch can be observed running (and posting) despite CI failure.
Safe to delete after TC-6192.
"""


def test_tc6192_intentional_failure():
    """Always fails on purpose (TC-6192 CI-fail scenario)."""
    assert False, "intentional failure for TC-6192 CI-fail acceptance scenario"
