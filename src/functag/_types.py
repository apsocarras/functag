import importlib
import importlib.util
from typing import (
    Any,
    Iterator,
    Protocol,
    Sequence,
    SupportsIndex,
    TypeAlias,
    TypeVar,
    Union,
    overload,
)

_KT = TypeVar("_KT")
_KT_co = TypeVar("_KT_co", covariant=True)
_KT_contra = TypeVar("_KT_contra", contravariant=True)
_VT = TypeVar("_VT")
_VT_co = TypeVar("_VT_co", covariant=True)
_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)


class StrictSequenceStr(Protocol[_T_co]):
    @overload
    def __getitem__(self, index: SupportsIndex, /) -> _T_co: ...
    @overload
    def __getitem__(self, index: slice, /) -> Sequence[_T_co]: ...
    def __contains__(self, value: object, /) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T_co]: ...
    def index(self, value: Any, start: int = 0, stop: int = ..., /) -> int: ...
    def count(self, value: Any, /) -> int: ...
    def __reversed__(self) -> Iterator[_T_co]: ...


INSTALLED_PACKAGES = {
    pkg_name: (importlib.util.find_spec(pkg_name) is not None)
    for pkg_name in ("pandera", "polars", "pandas")
}

if (INSTALLED_PACKAGES["polars"]) and (INSTALLED_PACKAGES["pandas"]):
    import pandas as pd
    import polars as pl

    DataFrame: TypeAlias = Union[pl.DataFrame, pl.LazyFrame, pd.DataFrame]

elif INSTALLED_PACKAGES["polars"]:
    import polars as pl

    DataFrame: TypeAlias = Union[pl.DataFrame, pl.LazyFrame]

elif INSTALLED_PACKAGES["pandas"]:
    import pandas as pd

    DataFrame: TypeAlias = Union[pd.DataFrame]
