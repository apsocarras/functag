import warnings

import pytest

from functag import requires


@requires("a", "b", quantifier="all", handler="raise")
def all_required(a=None, b=None):
    return a + b


@requires("x", "y", quantifier="at_least_one", handler="warn_None")
def at_least_one_required(x=None, y=None):
    return x or y


@requires(
    "p",
    "q",
    quantifier="exactly_one",
    handler="warn_default",
)
def exactly_one_required(p=None, q=None):
    return p or q


def test_all_required():
    assert all_required(a=1, b=2) == 3
    with pytest.raises(ValueError):
        all_required(a=1)


def test_at_least_one_required():
    assert at_least_one_required(x=1) == 1
    assert at_least_one_required(y=2) == 2
    assert at_least_one_required(x=1, y=2) == 1

    with warnings.catch_warnings(record=True) as captured:
        assert at_least_one_required() is None
        assert "requires at least one of" in str(captured[0].message)


def test_exactly_one_required():
    assert exactly_one_required(p=1) == 1
    assert exactly_one_required(q=2) == 2

    with warnings.catch_warnings(record=True) as captured:
        assert exactly_one_required() is None
        assert "requires exactly one of" in str(captured[0].message)

    with warnings.catch_warnings(record=True) as captured:
        assert exactly_one_required(p=1, q=2) == 1
        assert "requires exactly one of" in str(captured[0].message)
