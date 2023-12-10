# %% [markdown]
# # Reference Task
#
# ```{eval-rst}
# .. tags:: Intermediate
# ```
#
# A {py:func}`nebulakit.reference_task` references the Nebula tasks that have already been defined, serialized, and registered.
# You can reference tasks from other projects and create workflows that use tasks declared by others.
# These tasks can be in their own containers, python runtimes, nebulakit versions, and even different languages.
#
# The following example illustrates how to use reference tasks.
#
# :::{note}
# Reference tasks cannot be run locally. You must mock them out.
# :::
# %%
from typing import List

from nebulakit import reference_task, workflow
from nebulakit.types.file import NebulaFile


@reference_task(
    project="nebulasnacks",
    domain="development",
    name="data_types_and_io.file.normalize_columns",
    version="{{ registration.version }}",
)
def normalize_columns(
    csv_url: NebulaFile,
    column_names: List[str],
    columns_to_normalize: List[str],
    output_location: str,
) -> NebulaFile:
    ...


@workflow
def wf() -> NebulaFile:
    return normalize_columns(
        csv_url="https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv",
        column_names=["Name", "Sex", "Age", "Heights (in)", "Weight (lbs)"],
        columns_to_normalize=["Age"],
        output_location="",
    )


# %% [markdown]
# :::{note}
# The macro `{{ registration.version }}` is populated by `nebulactl register` during registration.
# Generally, it is unnecessary for reference tasks, as it is preferable to bind to a specific version of the task or launch plan.
# However, in this example, we are registering both the task `core.nebula_basics.files.normalize_columns` and the workflow that references it.
# Therefore, we need the macro to be updated to the version of a specific Nebulasnacks release.
# This is why `{{ registration.version }}` is used.
#
# A typical reference task would resemble the following:
#
# ```python
# @reference_task(
#      project="nebulasnacks",
#      domain="development",
#      name="core.nebula_basics.files.normalize_columns",
#      version="d06cebcfbeabc02b545eefa13a01c6ca992940c8", # If using GIT for versioning OR 0.16.0, if semver
#  )
#  def normalize_columns(...):
#      ...
# ```
# :::
#
