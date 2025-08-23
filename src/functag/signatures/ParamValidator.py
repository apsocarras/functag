from abc import ABC
from ast import Call
from collections.abc import Mapping
from platform import architecture
from typing import Any, Callable, Literal, Never, TypeAlias, TypeVar, ParamSpec, overload
from inspect import BoundArguments, Signature, signature
import warnings

from ._handle_handler import handle_handler
from .._types import F, P, R, F_Any, F_Opt, Handler, Quantifier, ParamValidationResult
from .assert_has_params import assert_has_params 


class ParamValidator(ABC):
    """
    Base class for parameter-checking decorators. 
    """

    def __init__(
        *param_names: str, 
        handler: Handler = Handler.RAISE, 
        callback: F_Any | None = None
    ): 
        self._param_names = (*param_names)
        self._handler = handler
        self._callback = callback
        super().__init__()

    @abstractmethod 
    def _validate(self, bound_args: BoundArguments, func: F | None, *args: Any, **kwargs: Any) -> ParamValidationResult: ...

    @property 
    def param_names(self) -> tuple[str, ...]: return self._param_names

    @property 
    def handler(self) -> Handler: return self._handler

    def callback(self) -> F_Any | None: return self._callback

    def __call__(self, func: F) -> F | F_Opt:
        func_sig: Signature = assert_has_params(func, *self.param_names)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None: 
            nonlocal func_sig
            bound_args: BoundArguments = func_sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            violation, msg = self._validate(bound_args, func)
            if violation: 
                return handle_handler(lambda: func(*args, **kwargs), msg, self.handler, self._callback)
            return func(*args, **kwargs)
        return wrapper


    
    