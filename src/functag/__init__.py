import copy
from functools import wraps


def annotate(**kwargs):
    """
    General wrapper to annotate a function with some attribute(s).
    Uses some magic to:

    1. Apply the attribute(s) to the innermost function (if there's other decorators being used).
    2. Enable reference to the function's attribute its own function body.

        - NOTE: Functions require a final 'self=None' argument in their signature to access these attributes.
        This will conflict with instance methods because 'self' is reserved.

            class TweedleDee:
                @annotate('dum')
                def tweedle(self):
                    print(self.dum)
                >>> AttributeError: 'TweedleDee' object has no attribute 'dum'

        A weird workaround is to use a dummy variable name (e.g. def tweedle(self, dum=None))

        You can also use these on class methods (*after* @classmethod):
            class Foo:
                @classmethod
                @output_may_omit(['bar'])
                def bar(cls, self=None):
                    print(self.output_may_omit)

        - NOTE: With both instance methods and class methods, the attribute doesn't seem accessible outside of
        the function.
            print(Foo.bar.output_may_omit)
            >>> AttributeError: 'Foo' object has no attribute 'output_may_omit'

    Requires kwargs to be valid Python variable/attribute names.
    """

    def decorator(func):
        """Testing decorator docstring"""

        @wraps(func)
        def wrapper(*args, **_kwargs):
            f = copy.copy(func)
            while getattr(
                f, "__wrapped__", False
            ):  # Get to the root of multiple stacked decorators.
                f = f.__wrapped__
                # Adds self to default args
            f.__defaults__ = f.__defaults__[:-1] + (f,)

            # Applies keyword args from decorator factory as attributes
            for k, v in kwargs.items():
                setattr(f, k, v)

            return func(*args, **_kwargs)

        # Need to do this again...?
        for k, v in kwargs.items():
            setattr(wrapper, k, v)

        return wrapper

    return decorator
