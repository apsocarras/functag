from functools import wraps
from typing import Any, Callable, Generator


def send_to_coro(coro: Callable[..., Generator[Any, Any, Any]]) -> Callable:
    """
    Decorator to send a decorated function to a generator produced by a Coroutine (here, a function that returns a Generator: Callable[..., Generator[Any, Any, Any]]).

    @send_to_coro is intended to be equivalent to the rather opaque
        @lambda coro: wraps(coro)(lambda *args, **kwargs: [ci := coro(*args, **kwargs), next(ci), lambda v=None: ci.send(v)][-1])
        def func(...) -> Generator:
            ...
        (See https://www.dontusethiscode.com/blog/2024-05-22_registration-decorators.html)

    """

    @wraps(coro)
    def wrapper(*args: Any, **kwargs: Any) -> Callable[[Any | None], None]:
        ci: Generator = coro(*args, **kwargs)
        next(ci)
        return lambda v: ci.send(v)

    return wrapper


@send_to_coro
def registry() -> Generator[Any, Any, Any]:
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
    funcs = [f := (yield ...)]  # list awaits a function to be sent in
    while f := (
        yield f
    ):  # Keep yielding the last function and awaiting new one to be sent
        funcs.append(f)
    if (yield ...):  # if sent None
        raise ValueError("Registry is finalized")
    yield from funcs
