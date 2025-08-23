from typing import Callable, Any
from inspect import Signature, signature


def assert_has_params(func: Callable[..., Any], *param_names: str) -> Signature:
    """
    Check that a specified set of parameters are in the function signature. 
    Used in signature-based decorators.
    """
    func_sig = signature(func)
    unrecognized_params = {p for p in param_names if p not in func_sig.parameters}
    if unrecognized_params:
        raise ValueError(
            f"Unrecognized parameters given to {func.__name__}: {unrecognized_params}"
        )
    return func_sig