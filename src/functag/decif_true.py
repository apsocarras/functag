
from typing import Callable, TypeVar, ParamSpec
from functool import wraps 

P = ParamSpec("P")
R = TypeVar("R")

def decif_true(
    decorator: Callable[[Callable[P,R]], Callable[P,R]],
    on: bool
)-> Callable[[Callable[P,R]], Callable[P,R]]:
    """
    Return a decorator which conditionally applies `decorator` depending on `on`
    """
    def wrapper(func: Callable[P,R]) -> Callable[P, R]: 
        if on: 
            return decorator(func)
        else: 
            @wraps(func)
            def identical(*args: P.args, **kwargs: P.kwargs)-> R:
                return func(*args, **kwargs)
            return identical
    return wrapper