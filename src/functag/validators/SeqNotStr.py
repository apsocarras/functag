from inspect import BoundArguments
from typing import Any
from .._types import F, F_Any, Handler, ParamValidationResult
from .ParamValidator import ParamValidator


class SeqNotStr(ParamValidator): 
    def __init__(*param_names: str, handler: Handler = Handler.RAISE, callback: F_Any| None = None):
        """
        Decorator to ensure at runtime that specified parameters are not of type `str`.
        This is because we have no `char` type in Python, and `str` is a `Sequence[str]`.

        Parameters
        ----------
        *param_names : str
            Names of parameters to check. Must exist in the function signature.
        handler : Handler
            Determines behavior when a violation is detected:
            - Handler.RAISE: raises ValueError
            - Handler.WARN_RETURN_NONE: issues a warning and returns None
            - Handler.WARN_KEEP_RETURN: issues a warning but still calls the function
        handler_callback : Callable[..., Any] | None
            Will be called when a violation occurs.

        Returns
        -------
        Callable
            A decorated function returning the original return type, or None depending
            on handler behavior.

        Notes
        -----
        - Parameters specified in `param_names` must exist in the function's signature; otherwise
        a ValueError is raised at decoration time.
        """

        super().__init__(*param_names, handler, callback)

    def _validate(self, bound_args: BoundArguments, func: F | None) -> ParamValidationResult:
        param_strs = {
            name: bound_args.arguments[name]
            for name in self.param_names
            if isinstance(bound_args.arguments[name], str)
        }
        violation = any(param_strs)
        msg =  f"Provided parameters should not be `str`: {param_strs}. `{func.__name__}`" if violation else None
        return ParamValidationResult(violation=violation, msg=msg)
