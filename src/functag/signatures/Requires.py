from ast import Call
from platform import architecture
from typing import Any, Callable, Literal, Never, TypeAlias, TypeVar, ParamSpec, overload
from inspect import BoundArguments, Signature, signature
from typing_extensions import override
import warnings


from .ParamValidator import ParamValidationResult, ParamValidator

from ._handle_handler import handle_handler
from .._types import Handler, Quantifier, P, R, F, F_Opt, F_Any
from .assert_has_params import assert_has_params 


class Requires(ParamValidator):

    def __init__(
        *param_names: str, 
        quantifier: Quantifier,
        handler: Handler = Handler.RAISE, 
        callback: F_Any | None = None
    ): 
        """
        Decorator to enforce that certain parameters of a function are provided at runtime. 

        Parameters
        ----------
        *param_names : str
            Names of parameters to validate.
        quantifier : Quantifier
            Rule for how many parameters must be provided.
            - All listed parameters are provided (Quantifier.ALL)
            - Exactly one parameter is provided (Quantifier.EXACTLY_ONE)
            - At least one parameter is provided (Quantifier.AT_LEAST_ONE)
        handler : Handler
            How to handle violations.
            - Handler.RAISE (default): raises ValueError
            - Handler.WARN_AND_CALL: issues a warning but still calls the function
            - Handler.WARN_RETURN_NONE: issues a warning and returns None
        callback : Callable[..., Any] | None
            Will be called when parameters do not meet requirements, BEFORE the function is called.

        Returns
        -------
        Callable
            A decorated function with the same signature as the original function.
            If handler=Handler.WARN_RETURN_NONE, the return type is None.
        
        Usage
        -----
        >>> @requires('x', 'y', quantifier=Quantifier.EXACTLY_ONE, handler=Handler.RAISE)
        ... def foo(x=None, y=None):
        ...    return x or y
        >>> foo_just_one()
        ValueError(`foo_just_one` requires exactly one of: {x: None, y: None}) 
        >>> foo_just_one(x=1, y=2)
        ValueError(`foo_just_one` requires exactly one of: {x: 1, y: 2}) 
        >>> foo_just_one(y=2)
        
        >>> @requires('x', 'y', callback=lambda: print("Bar! Bar! Bar!"))
        >>> def foo_all(x=None, y=None): 
        ...    return x and y 
        >>> foo_all(1)
        Bar! Bar! Bar! 
        ValueError(`foo_all` requires all of: {x: 1, y: None}) 

        Notes
        -----
        - Parameters specified in `param_names` must exist in the function's signature; otherwise
        a ValueError is raised at decoration time.
        """

        self._quantifier = quantifier
        super().__init__(*param_names, handler=handler, callback=callback)

    @override
    def _validate(self, bound_args: BoundArguments, func: F) -> ParamValidationResult:

        params = {p: bound_args.arguments.get(p, None) for p in self.param_names}
        have_vals = sum(v is not None for v in params.values())
        violation = (
            ((self._quantifier == Quantifier.ALL) and (have_vals != len(self.param_names)))
            or (self._quantifier == Quantifier.AT_LEAST_ONE and have_vals == 0)
            or (self._quantifier == Quantifier.EXACTLY_ONE and have_vals != 1)
        )
        msg =  (
            f"`{func.__name__}` requires {' '.join(self._quantifier.name.split('_'))} of: {self.param_names}."
            f" Provided: {params}"
        ) if violation else None 
            
        return ParamValidationResult(violation=violation, msg=msg)