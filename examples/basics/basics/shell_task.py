# %% [markdown]
# (shell_task)=
#
# # Shell Tasks
#
# ```{eval-rst}
# .. tags:: Basic
# ```
#
# To execute bash scripts within Nebula, you can utilize the {py:class}`~nebulakit.extras.tasks.shell.ShellTask` class.
# This example includes three shell tasks to execute bash commands.
#
# First, import the necessary libraries.
# %%
from pathlib import Path
from typing import Tuple

import nebulakit
from nebulakit import kwtypes, task, workflow
from nebulakit.extras.tasks.shell import OutputLocation, ShellTask
from nebulakit.types.directory import NebulaDirectory
from nebulakit.types.file import NebulaFile

# %% [markdown]
# With the required imports in place, you can proceed to define a shell task.
# To create a shell task, provide a name for it, specify the bash script to be executed,
# and define inputs and outputs if needed.
# %%
t1 = ShellTask(
    name="task_1",
    debug=True,
    script="""
    set -ex
    echo "Hey there! Let's run some bash scripts using Nebula's ShellTask."
    echo "Showcasing Nebula's Shell Task." >> {inputs.x}
    if grep "Nebula" {inputs.x}
    then
        echo "Found it!" >> {inputs.x}
    else
        echo "Not found!"
    fi
    """,
    inputs=kwtypes(x=NebulaFile),
    output_locs=[OutputLocation(var="i", var_type=NebulaFile, location="{inputs.x}")],
)


t2 = ShellTask(
    name="task_2",
    debug=True,
    script="""
    set -ex
    cp {inputs.x} {inputs.y}
    tar -zcvf {outputs.j} {inputs.y}
    """,
    inputs=kwtypes(x=NebulaFile, y=NebulaDirectory),
    output_locs=[OutputLocation(var="j", var_type=NebulaFile, location="{inputs.y}.tar.gz")],
)


t3 = ShellTask(
    name="task_3",
    debug=True,
    script="""
    set -ex
    tar -zxvf {inputs.z}
    cat {inputs.y}/$(basename {inputs.x}) | wc -m > {outputs.k}
    """,
    inputs=kwtypes(x=NebulaFile, y=NebulaDirectory, z=NebulaFile),
    output_locs=[OutputLocation(var="k", var_type=NebulaFile, location="output.txt")],
)


# %% [markdown]
# Here's a breakdown of the parameters of the `ShellTask`:
#
# - The `inputs` parameter allows you to specify the types of inputs that the task will accept
# - The `output_locs` parameter is used to define the output locations, which can be `NebulaFile` or `NebulaDirectory`
# - The `script` parameter contains the actual bash script that will be executed
#   (`{inputs.x}`, `{outputs.j}`, etc. will be replaced with the actual input and output values).
# - The `debug` parameter is helpful for debugging purposes
#
# We define a task to instantiate `NebulaFile` and `NebulaDirectory`.
# A `.gitkeep` file is created in the NebulaDirectory as a placeholder to ensure the directory exists.
# %%
@task
def create_entities() -> Tuple[NebulaFile, NebulaDirectory]:
    working_dir = Path(nebulakit.current_context().working_directory)
    nebulafile = working_dir / "test.txt"
    nebulafile.touch()

    nebuladir = working_dir / "testdata"
    nebuladir.mkdir(exist_ok=True)

    nebuladir_file = nebuladir / ".gitkeep"
    nebuladir_file.touch()
    return nebulafile, nebuladir


# %% [markdown]
# We create a workflow to define the dependencies between the tasks.
# %%
@workflow
def shell_task_wf() -> NebulaFile:
    x, y = create_entities()
    t1_out = t1(x=x)
    t2_out = t2(x=t1_out, y=y)
    t3_out = t3(x=x, y=y, z=t2_out)
    return t3_out


# %% [markdown]
# You can run the workflow locally.
# %%
if __name__ == "__main__":
    print(f"Running shell_task_wf() {shell_task_wf()}")
