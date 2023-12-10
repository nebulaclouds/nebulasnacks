(env_setup)=

# Environment Setup

## Prerequisites

- Make sure you have [docker](https://docs.docker.com/get-docker/) and [git](https://git-scm.com/) installed.
- Install {doc}`nebulactl <nebulactl:index>`, the commandline interface for Nebula.

## Repo setup

As we intend to execute the code locally, duplicate this code block into `hello_world.py`.

```python
from nebulakit import task, workflow

@task
def say_hello() -> str:
    return "Hello, World!"

@workflow
def hello_world_wf() -> str:
    res = say_hello()
    return res

if __name__ == "__main__":
    print(f"Running hello_world_wf() {hello_world_wf()}")
```

To install `nebulakit`, run the following command:

```
pip install nebulakit
```

:::{tip}
**Recommended**: Create a new python virtual environment to make sure it doesn't interfere with your
development environment. You can do this by running the following commands in your terminal:

```{prompt} bash
python -m venv ~/venvs/nebula-examples
source ~/venvs/nebula-examples/bin/activate
```

:::

To make sure everything is working in your virtual environment, run `hello_world.py` locally:

```{prompt} bash
python hello_world.py
```

Expected output:

```{prompt}
Running hello_world_wf() Hello, World!
```

## Create a local demo Nebula cluster

```{important}
Make sure the Docker daemon is running before starting the demo cluster.
```

Use `nebulactl` to start a demo Nebula cluster:

```{prompt} bash
nebulactl demo start
```

After this completes, be sure to export the Nebula config as it will be essential later. Run the command in the output that looks like this:
```{prompt} bash
export NEBULACTL_CONFIG= ~/<pathTo>/.nebula/config-sandbox.yaml
```

## Running workflows

Now you can run the example workflow locally using the default Docker image bundled with `nebulakit`:

```{prompt} bash
pynebula run hello_world.py hello_world_wf
```

:::{note}
The initial arguments of `pynebula run` take the form of
`path/to/script.py <task_or_workflow_name>`, where `<task_or_workflow_name>`
refers to the function decorated with `@task` or `@workflow` that you wish to run.
:::

To run the workflow on the demo Nebula cluster, all you need to do is supply the `--remote` flag:

```
pynebula run --remote hello_world.py hello_world_wf
```

You can also run the code directly from a remote source:

```
pynebula run --remote \
    https://raw.githubusercontent.com/nebulaclouds/nebulasnacks/master/examples/basics/basics/hello_world.py \
    hello_world_wf
```

You should see an output that looks like:

```{prompt}
Go to https://<nebula_admin_url>/console/projects/nebulasnacks/domains/development/executions/<execution_name> to see execution in the console.
```

You can visit this URL to inspect the execution as it runs:

:::{figure} https://raw.githubusercontent.com/nebulaclouds/static-resources/main/common/first_run_console.gif
:alt: A quick visual tour for launching your first Workflow.
:::

Finally, run a workflow that takes some inputs, for example the `workflow.py` example:

```{prompt} bash
pynebula run --remote \
    https://raw.githubusercontent.com/nebulaclouds/nebulasnacks/master/examples/basics/basics/workflow.py \
    simple_wf --x '[-3,0,3]' --y '[7,4,-2]'
```

:::{note}
We're passing in the workflow inputs as additional options to `pynebula run`. In the above example, the
inputs are `--x '[-3,0,3]'` and `--y '[7,4,-2]'`. For snake-case argument names like `arg_name`, you can provide the
option as `--arg-name`.
:::

## Visualizing workflows

Workflows can be visualized as DAGs on the UI.
However, you can visualize workflows on the browser and in the terminal by _just_ using your terminal.

To view workflow on the browser:

```{prompt} bash $
nebulactl get workflows \
    --project nebulasnacks \
    --domain development \
    --version <version> \
    -o doturl \
    basics.workflow.simple_wf
```

To view workflow as a `strict digraph` on the command line:

```{prompt} bash $
nebulactl get workflows \
    --project nebulasnacks \
    --domain development \
    --version <version> \
    -o dot \
    basics.workflow.simple_wf
```

Replace `<version>` with the version obtained from the console UI,
which might resemble something like `BLrGKJaYsW2ME1PaoirK1g==`.

:::{tip}
Running most of the examples in the **User Guide** only requires the default Docker image that ships with Nebula.
Many examples in the {ref}`tutorials` and {ref}`integrations` section depend on additional libraries such as
`sklearn`, `pytorch` or `tensorflow`, which will not work with the default docker image used by `pynebula run`.

These examples will explicitly show you which images to use for running these examples by passing in the Docker
image you want to use with the `--image` option in `pynebula run`.
:::

🎉 Congrats! Now you can run all the examples in the {ref}`userguide` 🎉

## What's next?

Try out the examples in the {doc}`Basics <auto_examples/basics/index>` section.
