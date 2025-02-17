"""Check that basic features work.

Catch cases where e.g. files are missing so the import doesn't work. It is
recommended to check that e.g. assets are included."""

import warnings
from typing import Sequence

from functag import warn_str


@warn_str("phrases")
def make_shout(phrases: Sequence[str]) -> list[str]:
    return [f"{phrase.upper()}!" for phrase in phrases]


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    a = make_shout("`str` should not be a Sequence[str]")

b = make_shout(
    phrases=(
        "Python should have a `char` type",
        "Or at least Intersection",
        "Or maybe Complement",
        "`str` should not be a `Sequence[str]`",
    )
)

if (a is None) and (
    b
    == [
        "PYTHON SHOULD HAVE A `CHAR` TYPE!",
        "OR AT LEAST INTERSECTION!",
        "OR MAYBE COMPLEMENT!",
        "`STR` SHOULD NOT BE A `SEQUENCE[STR]`!",
    ]
):
    print("Smoke test successful")
else:
    raise RuntimeError(f"a={a}, b={b}")
