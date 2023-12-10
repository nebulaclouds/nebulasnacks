# %% [markdown]
# (dataclass)=
#
# # Data Class
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# When you've multiple values that you want to send across Nebula entities, you can use a `dataclass`.
#
# Nebulakit uses the [Mashumaro library](https://github.com/Fatal1ty/mashumaro)
# to serialize and deserialize dataclasses.
#
# :::{important}
# If you're using Nebulakit version below v1.10, you'll need to decorate with `@dataclass_json` using
# `from dataclass_json import dataclass_json` instead of inheriting from Mashumaro's `DataClassJSONMixin`.
# :::
#
# To begin, import the necessary dependencies.
# %%
import os
import tempfile
from dataclasses import dataclass

import pandas as pd
from nebulakit import task, workflow
from nebulakit.types.directory import NebulaDirectory
from nebulakit.types.file import NebulaFile
from nebulakit.types.structured import StructuredDataset
from mashumaro.mixins.json import DataClassJSONMixin


# %% [markdown]
# ## Python types
# We define a `dataclass` with `int`, `str` and `dict` as the data types.
# %%
@dataclass
class Datum(DataClassJSONMixin):
    x: int
    y: str
    z: dict[int, str]


# %% [markdown]
# You can send a `dataclass` between different tasks written in various languages, and input it through the Nebula console as raw JSON.
#
# :::{note}
# All variables in a data class should be **annotated with their type**. Failure to do should will result in an error.
# :::
#
# Once declared, a dataclass can be returned as an output or accepted as an input.
# %%
@task
def stringify(s: int) -> Datum:
    """
    A dataclass return will be treated as a single complex JSON return.
    """
    return Datum(x=s, y=str(s), z={s: str(s)})


@task
def add(x: Datum, y: Datum) -> Datum:
    """
    Nebulakit automatically converts the provided JSON into a data class.
    If the structures don't match, it triggers a runtime failure.
    """
    x.z.update(y.z)
    return Datum(x=x.x + y.x, y=x.y + y.y, z=x.z)


# %% [markdown]
# ## Nebula types
# We also define a data class that accepts {std:ref}`StructuredDataset <structured_dataset>`,
# {std:ref}`NebulaFile <files>` and {std:ref}`NebulaDirectory <folder>`.
# %%
@dataclass
class NebulaTypes(DataClassJSONMixin):
    dataframe: StructuredDataset
    file: NebulaFile
    directory: NebulaDirectory


@task
def upload_data() -> NebulaTypes:
    """
    Nebulakit will upload NebulaFile, NebulaDirectory and StructuredDataset to the blob store,
    such as GCP or S3.
    """
    # 1. StructuredDataset
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})

    # 2. NebulaDirectory
    temp_dir = tempfile.mkdtemp(prefix="nebula-")
    df.to_parquet(temp_dir + "/df.parquet")

    # 3. NebulaFile
    file_path = tempfile.NamedTemporaryFile(delete=False)
    file_path.write(b"Hello, World!")

    fs = NebulaTypes(
        dataframe=StructuredDataset(dataframe=df),
        file=NebulaFile(file_path.name),
        directory=NebulaDirectory(temp_dir),
    )
    return fs


@task
def download_data(res: NebulaTypes):
    assert pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]}).equals(res.dataframe.open(pd.DataFrame).all())
    f = open(res.file, "r")
    assert f.read() == "Hello, World!"
    assert os.listdir(res.directory) == ["df.parquet"]


# %% [markdown]
# A data class supports the usage of data associated with Python types, data classes,
# nebula file, nebula directory and structured dataset.
#
# We define a workflow that calls the tasks created above.
# %%
@workflow
def dataclass_wf(x: int, y: int) -> (Datum, NebulaTypes):
    o1 = add(x=stringify(s=x), y=stringify(s=y))
    o2 = upload_data()
    download_data(res=o2)
    return o1, o2


# %% [markdown]
# You can run the workflow locally as follows:
# %%
if __name__ == "__main__":
    dataclass_wf(x=10, y=20)

# %% [markdown]
# To trigger a task that accepts a dataclass as an input with `pynebula run`, you can provide a JSON file as an input:
# ```
# pynebula run \
#   https://raw.githubusercontent.com/nebulaclouds/nebulasnacks/master/examples/data_types_and_io/data_types_and_io/dataclass.py \
#   add --x dataclass_input.json --y dataclass_input.json
# ```
