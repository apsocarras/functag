from typing import Any, Callable
from .._types import Handler
import warnings


def handle_handler(func: Callable[..., Any], msg: str, handler: Handler, callback: Callable[..., Any] | None = None):
    """Handler handling Handler handler"""
    
    if callback is not None: 
        callback()

    match handler:
        case Handler.RAISE:
            raise ValueError(msg)
        case Handler.WARN_RETURN_NONE:
            warnings.warn(msg)
            return None
        case Handler.WARN_AND_CALL:
            warnings.warn(msg)
            return func()
