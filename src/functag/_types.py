from enum import Enum
from typing import Any, Callable, ParamSpec, TypeAlias, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
F: TypeAlias = Callable[P,R]
F_Opt: TypeAlias = Callable[P, R | None]
F_Any= TypeVar('F_Any', bound=Callable[..., Any])

class Handler(Enum): 
    RAISE: "raise"
    WARN_RETURN_NONE: "warn_return_none"
    WARN_AND_CALL: "warn_and_call"

class Quantifier(Enum): 
    ALL: "all"
    AT_LEAST_ONE: "at_least_one"
    EXACTLY_ONE: "exactly_one"

class ParamValidationResult(NamedTuple): 
    violation: bool 
    msg: str | None
