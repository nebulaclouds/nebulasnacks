# %% [markdown]
# (integrations_sql_sqlite3)=
#
# # Sqlite3
#
# The following example shows how you can write SQLite3 queries using the SQLite3Task, which is bundled as part of the
# core nebulakit. Since SQL Queries are portable across workflows and Nebula installations (as long as the data exists),
# this task will always run with a pre-built container, specifically the [nebulakit container](https://github.com/nebulaclouds/nebulakit/blob/v0.19.0/Dockerfile.py38)
# itself. Therefore, users are not required to build a container for SQLite3. You can simply implement the task - register and
# execute it immediately.
#
# In some cases local execution is not possible - e.g. Snowflake. But for SQLlite3 local execution is also supported.
# %%
import pandas
from nebulakit import kwtypes, task, workflow
from nebulakit.extras.sqlite3.task import SQLite3Config, SQLite3Task

# %% [markdown]
# SQLite3 queries in nebula produce a Schema output. The data in this example is
# taken from [here](https://www.sqlitetutorial.net/sqlite-sample-database/).
# %%
from nebulakit.types.schema import NebulaSchema

EXAMPLE_DB = "https://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip"

# %% [markdown]
# the task is declared as a regular task. Alternatively it can be declared within a workflow just at the point of using
# it (example later)
# %%
sql_task = SQLite3Task(
    name="sqlite3.sample",
    query_template="select TrackId, Name from tracks limit {{.inputs.limit}}",
    inputs=kwtypes(limit=int),
    output_schema_type=NebulaSchema[kwtypes(TrackId=int, Name=str)],
    task_config=SQLite3Config(uri=EXAMPLE_DB, compressed=True),
)


# %% [markdown]
# As described elsewhere NebulaSchemas can be easily be received as pandas Dataframe and Nebula will autoconvert them
# %%
@task
def print_and_count_columns(df: pandas.DataFrame) -> int:
    return len(df[df.columns[0]])


# %% [markdown]
# The task can be used normally in the workflow, passing the declared inputs
# %%
@workflow
def wf() -> int:
    return print_and_count_columns(df=sql_task(limit=100))


# %% [markdown]
# It can also be executed locally.
# %%
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running main {wf()}")


# %% [markdown]
# As mentioned earlier it is possible to also write the SQL Task inline as follows
# %%
@workflow
def query_wf() -> int:
    df = SQLite3Task(
        name="sqlite3.sample_inline",
        query_template="select TrackId, Name from tracks limit {{.inputs.limit}}",
        inputs=kwtypes(limit=int),
        output_schema_type=NebulaSchema[kwtypes(TrackId=int, Name=str)],
        task_config=SQLite3Config(uri=EXAMPLE_DB, compressed=True),
    )(limit=100)
    return print_and_count_columns(df=df)


# %% [markdown]
# It can also be executed locally.
#
# %%
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running main {query_wf()}")
