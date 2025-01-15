import importlib
import importlib.util
import logging
from typing import Sequence, Union

from functag import annotate

logger = logging.getLogger(__name__)

DATAFRAME_PACKAGES = (
    "pandera",
    "polars",
    "pandas",
)

INSTALLED_PACKAGES = {
    pkg_name: (importlib.util.find_spec(pkg_name) is not None)
    for pkg_name in (DATAFRAME_PACKAGES)
}
if not any(INSTALLED_PACKAGES["polars"], INSTALLED_PACKAGES["pandas"]):
    logger.info("Need one of `polars` or `pandas` to use dataframe.py annotations.")
else:
    from functag._types import DataFrame, StrictSequenceStr

    def requires(cols: StrictSequenceStr):
        """
        Annotate which columns are required in a DataFrame function.
        """
        return annotate(required_cols=cols)

    def output_may_omit(cols: StrictSequenceStr):
        """
        Annotate which columns may be missing in the output of a function vs. the Schema.
        Check this with errors.catch_missing_cols instead of setting columns as optional in a schema.
        """
        return annotate(output_may_omit=set(cols))

    def attaches(cols: StrictSequenceStr):
        """
        Annotate which columns are attached and joined in a DataFrame function.
        """
        return annotate(attaches_cols=cols)

    def lookup(data: Union[DataFrame, Sequence[DataFrame]]):
        """
        Annotate which lookup DataFrames the function uses.
        """
        return annotate(references_df=data)


if INSTALLED_PACKAGES["pandera"]:
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
