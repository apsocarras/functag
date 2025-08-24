from ast import Call
from functools import wraps
from typing import Annotated, Any, Callable, Generator, ParamSpec, TypeVar
from .._types import P, R

S = Annotated[TypeVar("S"), 'Sent into Generator']
Y = Annotated[TypeVar("Y"), 'Yielded by Generator']


def callable_coro(coro: Callable[P, Generator[Y, S, R]]) -> Callable[P, Callable[[S | None], Y]]:
    """
    Decorator that wraps the generator semantics (`next`, `send`) of a generator-based Coroutine into a Callable.
    (In this context, a Coroutine is a function that returns a Generator: Callable[..., Generator[Y, S, R]]).

    See: https://www.dontusethiscode.com/blog/2024-05-22_registration-decorators.html

    Equivalent to the rather opaque: 
    @lambda coro: wraps(coro)(
        lambda *args, **kwargs: [ci := coro(*args, **kwargs), 
        next(ci), 
        lambda v=None: ci.send(v)][-1]
    )
    def func(...) -> Generator:
        ...

    Usage
    -----

    >>> def running_avg(): 
    ...     total, count, average = 0.0, 0, None
    ...     while True: 
    ...         value = yield average
    ...         total += value 
    ...         count += 1
    ...         average = total / count
    
    >>> c1 = running_avg()
    >>> c2 = callable_coro(running_avg)
    >>> print(next(c1), c2())
    None, None
    >>> print(c1.send(10), c2(10))
    10.0, 10.0
    >>> print(c1.send(20), c2(20))
    15.0, 15.0
    """

    @wraps(coro)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Callable[[S | None], Y]:
        ci: Generator = coro(*args, **kwargs)
        next(ci)
        return lambda v: ci.send(v)

    return wrapper


@callable_coro
def registry() -> Generator[Y, S, R]:
    """
    Coroutine to store a registry of functions.

    By using a generator, we make the registry "finalized" as it can only be iterated over once.
        (See: https://www.dontusethiscode.com/blog/2024-05-22_registration-decorators.html)

    Usage:
    --------
    Finalize = None
    reg = registry()

    @reg
    def f():
        pass

    @reg
    def g():
        pass

    reg(Finalize)
    print(f'{[*iter(reg, None)] = }')
    >>> [<function f at 0x7b327c51d870>, <function g at 0x7b327c51d6c0>]
    """
    funcs = [f := (yield ...)]  # awaits a function to be sent in, initializing a list
    while f := (
        yield f # keeps waiting for the next function to be sent in, appending, until f is None/Falsy
    ):
        funcs.append(f)
    if (yield ...):  # if sent None
        raise ValueError("Registry is finalized")
    yield from funcs
