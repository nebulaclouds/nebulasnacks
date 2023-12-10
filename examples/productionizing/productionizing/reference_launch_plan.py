# %% [markdown]
# # Reference Launch Plan
#
# ```{eval-rst}
# .. tags:: Intermediate
# ```
#
# A {py:func}`nebulakit.reference_launch_plan` references previously defined, serialized, and registered Nebula launch plans.
# You can reference launch plans from other projects and create workflows that use launch plans declared by others.
#
# The following example illustrates how to use reference launch plans.
#
# :::{note}
# Reference launch plans cannot be run locally. You must mock them out.
# :::

# %%
from typing import List

from nebulakit import reference_launch_plan, workflow
from nebulakit.types.file import NebulaFile


@reference_launch_plan(
    project="nebulasnacks",
    domain="development",
    name="data_types_and_io.file.normalize_csv_file",
    version="{{ registration.version }}",
)
def normalize_csv_file(
    csv_url: NebulaFile,
    column_names: List[str],
    columns_to_normalize: List[str],
    output_location: str,
) -> NebulaFile:
    ...


@workflow
def reference_lp_wf() -> NebulaFile:
    return normalize_csv_file(
        csv_url="https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv",
        column_names=["Name", "Sex", "Age", "Heights (in)", "Weight (lbs)"],
        columns_to_normalize=["Age"],
        output_location="",
    )


# %% [markdown]
# It's important to verify that the workflow interface corresponds to that of the referenced workflow.
#
# :::{note}
# The macro `{{ registration.version }}` is populated by `nebulactl register` during registration.
# Generally, it is unnecessary for reference launch plans, as it is preferable to bind to a specific version of the task or launch plan.
# However, in this example, we are registering both the launch plan `core.nebula_basics.files.normalize_csv_file` and the workflow that references it.
# Therefore, we need the macro to be updated to the version of a specific Nebulasnacks release.
# This is why `{{ registration.version }}` is used.
#
# A typical reference launch plan would resemble the following:
#
# ```python
# @reference_launch_plan(
#     project="nebulasnacks",
#     domain="development",
#     name="core.nebula_basics.files.normalize_csv_file",
#     version="d06cebcfbeabc02b545eefa13a01c6ca992940c8", # If using GIT for versioning OR 0.16.0, if semver
# )
# def normalize_csv_file(...):
#     ...
# ```
# :::
#
