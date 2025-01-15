import importlib
import importlib.util
from typing import Sequence, TypeAlias, Union

from functag import annotate

INSTALLED_PACKAGES = {
    pkg_name: (importlib.util.find_spec(pkg_name) is not None)
    for pkg_name in ("pandera", "polars", "pandas")
}

if (INSTALLED_PACKAGES["polars"]) and (INSTALLED_PACKAGES["pandas"]):
    import pandas as pd
    import polars as pl

    DataFrame: TypeAlias = Union[pl.DataFrame, pl.LazyFrame, pd.DataFrame]

    def requires(cols: Sequence):
        """
        Annotate which columns are required in a DataFrame function.
        """
        return annotate(required_cols=cols)

    def output_may_omit(cols: Sequence):
        """
        Annotate which columns may be missing in the output of a function vs. the Schema.
        Check this with errors.catch_missing_cols instead of setting columns as optional in a schema.
        """
        return annotate(output_may_omit=set(cols))

    def lookup(data: Union[DataFrame, Sequence[DataFrame]]):
        """
        Annotate which lookup DataFrames the function uses.
        """
        return annotate(references_df=data)

    def attaches(cols: Sequence):
        """
        Annotate which columns are attached and joined in a DataFrame function.
        """
        return annotate(attaches_cols=cols)


if pandera_installed := (importlib.util.find_spec("pandera") is not None):
    import pandera as pa

    def schemas(schemas: Union[Sequence[pa.DataFrameModel], pa.DataFrameModel]):
        """
        Annotate which schemas a function references.
        NOTE: You can omit for methods of the models themselves.
            - TODO: May want to enable retrieving from function signature and perhaps even namespace!
        """
        if not isinstance(schemas, Sequence):
            schemas = (schemas,)
        return annotate(schemas=schemas)
