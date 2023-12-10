# %% [markdown]
# (folder)=
#
# # Nebula Directory
#
# ```{eval-rst}
# .. tags:: Data, Basic
# ```
#
# In addition to files, folders are another fundamental operating system primitive.
# Nebula supports folders in the form of
# [multi-part blobs](https://github.com/nebulaclouds/nebulaidl/blob/master/protos/nebulaidl/core/types.proto#L73).
#
# To begin, import the libraries.
# %%
import csv
import os
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import List

import nebulakit
from nebulakit import task, workflow
from nebulakit.types.directory import NebulaDirectory


# %% [markdown]
# Building upon the previous example demonstrated in the {std:ref}`file <file>` section,
# let's continue by considering the normalization of columns in a CSV file.
#
# The following task downloads a list of URLs pointing to CSV files
# and returns the folder path in a `NebulaDirectory` object.
# %%
@task
def download_files(csv_urls: List[str]) -> NebulaDirectory:
    working_dir = nebulakit.current_context().working_directory
    local_dir = Path(os.path.join(working_dir, "csv_files"))
    local_dir.mkdir(exist_ok=True)

    # get the number of digits needed to preserve the order of files in the local directory
    zfill_len = len(str(len(csv_urls)))
    for idx, remote_location in enumerate(csv_urls):
        local_image = os.path.join(
            # prefix the file name with the index location of the file in the original csv_urls list
            local_dir,
            f"{str(idx).zfill(zfill_len)}_{os.path.basename(remote_location)}",
        )
        urllib.request.urlretrieve(remote_location, local_image)
    return NebulaDirectory(path=str(local_dir))


# %% [markdown]
# :::{note}
# You can annotate a `NebulaDirectory` when you want to download or upload the contents of the directory in batches.
# For example,
#
# ```{code-block}
# @task
# def t1(directory: Annotated[NebulaDirectory, BatchSize(10)]) -> Annotated[NebulaDirectory, BatchSize(100)]:
#     ...
#     return NebulaDirectory(...)
# ```
#
# Nebulakit efficiently downloads files from the specified input directory in 10-file chunks.
# It then loads these chunks into memory before writing them to the local disk.
# The process repeats for subsequent sets of 10 files.
# Similarly, for outputs, Nebulakit uploads the resulting directory in chunks of 100.
# :::
#
# We define a helper function to normalize the columns in-place.
#
# :::{note}
# This is a plain Python function that will be called in a subsequent Nebula task. This example
# demonstrates how Nebula tasks are simply entrypoints of execution, which can themselves call
# other functions and routines that are written in pure Python.
# :::
# %%
def normalize_columns(
    local_csv_file: str,
    column_names: List[str],
    columns_to_normalize: List[str],
):
    # read the data from the raw csv file
    parsed_data = defaultdict(list)
    with open(local_csv_file, newline="\n") as input_file:
        reader = csv.DictReader(input_file, fieldnames=column_names)
        for row in (x for i, x in enumerate(reader) if i > 0):
            for column in columns_to_normalize:
                parsed_data[column].append(float(row[column].strip()))

    # normalize the data
    normalized_data = defaultdict(list)
    for colname, values in parsed_data.items():
        mean = sum(values) / len(values)
        std = (sum([(x - mean) ** 2 for x in values]) / len(values)) ** 0.5
        normalized_data[colname] = [(x - mean) / std for x in values]

    # overwrite the csv file with the normalized columns
    with open(local_csv_file, mode="w") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns_to_normalize)
        writer.writeheader()
        for row in zip(*normalized_data.values()):
            writer.writerow({k: row[i] for i, k in enumerate(columns_to_normalize)})


# %% [markdown]
# We then define a task that accepts the previously downloaded folder, along with some metadata about the
# column names of each file in the directory and the column names that we want to normalize.
# %%
@task
def normalize_all_files(
    csv_files_dir: NebulaDirectory,
    columns_metadata: List[List[str]],
    columns_to_normalize_metadata: List[List[str]],
) -> NebulaDirectory:
    for local_csv_file, column_names, columns_to_normalize in zip(
        # make sure we sort the files in the directory to preserve the original order of the csv urls
        [os.path.join(csv_files_dir, x) for x in sorted(os.listdir(csv_files_dir))],
        columns_metadata,
        columns_to_normalize_metadata,
    ):
        normalize_columns(local_csv_file, column_names, columns_to_normalize)
    return NebulaDirectory(path=csv_files_dir.path)


# %% [markdown]
# Compose all of the above tasks into a workflow. This workflow accepts a list
# of URL strings pointing to a remote location containing a CSV file, a list of column names
# associated with each CSV file, and a list of columns that we want to normalize.
# %%
@workflow
def download_and_normalize_csv_files(
    csv_urls: List[str],
    columns_metadata: List[List[str]],
    columns_to_normalize_metadata: List[List[str]],
) -> NebulaDirectory:
    directory = download_files(csv_urls=csv_urls)
    return normalize_all_files(
        csv_files_dir=directory,
        columns_metadata=columns_metadata,
        columns_to_normalize_metadata=columns_to_normalize_metadata,
    )


# %% [markdown]
# You can run the workflow locally as follows:
# %%
if __name__ == "__main__":
    csv_urls = [
        "https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv",
        "https://people.sc.fsu.edu/~jburkardt/data/csv/faithful.csv",
    ]
    columns_metadata = [
        ["Name", "Sex", "Age", "Heights (in)", "Weight (lbs)"],
        ["Index", "Eruption length (mins)", "Eruption wait (mins)"],
    ]
    columns_to_normalize_metadata = [
        ["Age"],
        ["Eruption length (mins)"],
    ]

    print(f"Running {__file__} main...")
    directory = download_and_normalize_csv_files(
        csv_urls=csv_urls,
        columns_metadata=columns_metadata,
        columns_to_normalize_metadata=columns_to_normalize_metadata,
    )
    print(f"Running download_and_normalize_csv_files on {csv_urls}: " f"{directory}")
