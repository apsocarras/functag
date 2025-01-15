from functools import wraps
from typing import Callable, Type, overload


def abridge_repr(cls: Type):
    """
    Abridged the __repr__ method of a class to exclude values which were set as None.
    """
    original_repr = cls.__repr__

    @wraps(cls.__repr__)
    def _abridged_repr(self):
        repr_str = original_repr(self)
        class_name = self.__class__.__name__
        attrs = repr_str[len(class_name) + 1 : -1]
        filtered_attrs = ", ".join(
            attr for attr in attrs.split(", ") if "None" not in attr
        )
        if any("None" in attr for attr in attrs):
            filtered_attrs += ", ..."

        return f"{class_name}({filtered_attrs})"

    cls.__repr__ = _abridged_repr
    return cls


@overload
def dynamic_init_signature(cls_init: Callable, **kwargs):
    """
    Modify the signature of a class __init__ to show kwargs as named arguments
    """
    from inspect import Parameter, signature

    # Get the original signature of the init method
    init_signature = signature(cls_init)

    # Create new parameters from named_args
    new_parameters = []
    for key, value in kwargs.items():
        new_parameters.append(
            Parameter(key, kind=Parameter.KEYWORD_ONLY, default=value)
        )

    # Retain the original parameters, except **kwargs
    existing_parameters = [
        param
        for param in init_signature.parameters.values()
        if param.kind != Parameter.VAR_KEYWORD
    ]

    # Create a new function with the updated signature
    new_signature = init_signature.replace(
        parameters=existing_parameters + new_parameters
    )
    # cls_init.__signature__ = new_signature
    return new_signature


@overload
def dynamic_init_signature(cls: Type, **new_kwargs):
    """
    Modify the signature of a class __init__ to show injected kwargs as named arguments.
    Only really useful for dynamically generating classes from class factories.
    TODO: Generated class signatures still look like they would be missing type hints.


    Usage:

    ```python
    from functag.class_decorators import dynamic_init_signature
    import inspaect

    class MyClass():
        def __init__(self, a: Any):
            self.a = a

    new_kwargs = {'b': Any, 'c': Sequence[Any]}
    dynamic_init_signature(MyClass.__ini___, new_kwargs)

    ```

    """
    original_init = cls.__init__
    cls.__init__.__signature__ = dynamic_init_signature(original_init, **new_kwargs)
    return cls
