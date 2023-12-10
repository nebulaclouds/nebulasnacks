---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(getting_started_run_and_schedule)=

# Running and Scheduling Workflows

Nebula supports the development and debugging of tasks and workflows in a local
setting, which increases the iteration speed of building out your data-
or machine-learning-driven applications.

Running your workflows locally is great for the initial stages of testing, but
what if you need to make sure that they run as intended on a Nebula cluster?
What if you need to run them on a regular cadence?

In this guide we'll cover how to run and schedule workflows for both development
and production use cases.

```{admonition} Prerequisites
:class: important

This guide assumes that you've completed the previous guides for
{ref}`Initializing a Nebula project <getting_started_creating_nebula_project>` and
{ref}`Packaging and Registering Workflows <getting_started_package_register>`.
```

## Create a `NebulaRemote` Object

In the {ref}`Introduction to Nebula <intro_running_nebula_workflows>`, you saw
how to run Nebula workflows with `pynebula run` in the case that you're working
with standalone scripts.

Once you're working with larger projects where you've registered workflows
to a Nebula cluster, we recommend using the {py:class}`~nebulakit.remote.remote.NebulaRemote`
client to run workflows from a Python runtime. First, let's create a `NebulaRemote`
object:

```{code-cell} ipython3
:tags: [remove-output]

from nebulakit.configuration import Config
from nebulakit.remote import NebulaRemote

remote = NebulaRemote(
    config=Config.auto(),
    default_project="nebulasnacks",
    default_domain="development",
)
```

## Running a Workflow

You can run workflows using the `NebulaRemote` {py:meth}`~nebulakit.remote.remote.NebulaRemote.execute`
method, where you need to pass in a dictionary of `inputs` that adhere to the
interface defined by the workflow.

`````{tabs}

````{group-tab} Locally Imported

If you have access to the `@workflow`-decorated function in your Python runtime
environment, you can import and execute it directly:

Before execute it directly, you need to register the workflow first.

```{prompt} bash $
pynebula register wf.py
```

```{code-block} python

from workflows.example import wf

execution = remote.execute(
    wf,
    inputs={"name": "Kermit"},
)
```

````

````{group-tab} Remotely Fetched

Execute a workflow by fetching a `NebulaWorkflow` object from the remote
**NebulaAdmin** service, which essentially contains the metadata representing a
Nebula workflow that exists on a Nebula cluster backend.

```{code-block} python
nebula_wf = remote.fetch_workflow(name="workflows.example.wf")
execution = remote.execute(nebula_wf, inputs={"name": "Kermit"})
```

````

`````

```{note}
You can also launch workflows via `nebulactl` which you can learn more about in
the {ref}`User Guide <remote_launchplan>`.
```

## Running a Launchplan

Similar to workflows, you can run launch plans with `NebulaRemote`:

`````{tabs}

````{group-tab} Locally Imported

If you have a `LaunchPlan` defined in your Python runtime environment, you can
execute it directly:

```{code-block} python

from workflows.example import wf

launch_plan = LaunchPlan.get_or_create(
    wf, name="launch_plan", default_inputs={"name": "Elmo"},
)

execution = remote.execute(launch_plan, inputs={})
```

````

````{group-tab} Remotely Fetched

Execute a task by fetching a `NebulaLaunchPlan` object from the remote
**NebulaAdmin** service, which essentially contains the metadata representing a
Nebula task that exists on a Nebula cluster backend.

This example assumes that you've added a `launch_plan` with some default inputs
to the `example.py` script and registered it to the backend:

```{code-block} python
nebula_launchplan = remote.fetch_launch_plan(name="workflows.example.launch_plan")
execution = remote.execute(nebula_launchplan, inputs={})
```

````

`````

## Running a Task

You can also run individual tasks on a Nebula cluster using `NebulaRemote`:

`````{tabs}

````{group-tab} Locally Imported

If you have access to the `@task`-decorated function in your Python runtime
environment, you can import and execute it directly:

```{code-block} python

from workflows.example import say_hello

execution = remote.execute(say_hello, inputs={"name": "Kermit"})
```

````

````{group-tab} Remotely Fetched

Execute a task by fetching a `NebulaWorkflow` object from the remote
**NebulaAdmin** service, which essentially contains the metadata representing a
Nebula task that exists on a Nebula cluster backend.

```{code-block} python
nebula_task = remote.fetch_task(name="workflows.example.say_hello")
execution = remote.execute(nebula_task, inputs={"name": "Kermit"})
```

````

`````

```{note}
You can also launch tasks via `nebulactl`, learn more in the {ref}`User Guide <remote_task>`
```

## Fetching Inputs and Outputs of an Execution

By default, {py:meth}`NebulaRemote.execute <nebulakit.remote.remote.NebulaRemote.execute>`
is non-blocking, but you can also pass in `wait=True` to make it synchronously
wait for the task or workflow to complete.

Print out the Nebula console url corresponding to your execution with:

```{code-block} python
print(f"Execution url: {remote.generate_console_url(execution)}")
```

Synchronize the state of the Nebula execution object with the remote state during
execution with the {py:meth}`~nebulakit.remote.remote.NebulaRemote.sync` method:

```{code-block} python
synced_execution = remote.sync(execution)
print(synced_execution.inputs)  # print out the inputs
```

You can also wait for the execution after you've launched it and access the
outputs:

```{code-block} python
completed_execution = remote.wait(execution)
print(completed_execution.outputs)  # print out the outputs
```

## Scheduling a Launch Plan

Finally, you can create a {py:class}`~nebulakit.LaunchPlan` that's scheduled
to run at a particular cadence by specifying the `schedule` argument:

```{code-block} python
from nebulakit import LaunchPlan, CronSchedule

from workflows.example import wf


launch_plan = LaunchPlan.get_or_create(
    wf,
    name="wf_launchplan",
    # run this launchplan every minute
    schedule=CronSchedule(schedule="*/1 * * * *"),
    default_inputs={"name": "Elmo"},
)
```

You can also specify a fixed-rate interval:

```{code-block} python
from datetime import timedelta
from nebulakit import FixedRate


launch_plan = LaunchPlan.get_or_create(
    wf,
    name="wf_launchplan",
    schedule=FixedRate(duration=timedelta(minutes=1)),
    default_inputs={"name": "Elmo"},
)
```

### Passing in the Scheduled Kick-off Time

Suppose that your workflow is parameterized to take in a `datetime` argument,
which determines how the workflow is executed (e.g. reading in data using the
current date).

You can specify a `kickoff_time_input_arg` in the schedule so that it
automatically passes the cron schedule kick-off time into the workflow:

```{code-cell} ipython
from datetime import datetime
from nebulakit import workflow, LaunchPlan, CronSchedule


@workflow
def process_data_wf(kickoff_time: datetime):
    # read data and process it based on kickoff_time
    ...

process_data_lp = LaunchPlan.get_or_create(
    process_data_wf,
    name="process_data_lp",
    schedule=CronSchedule(
        schedule="*/1 * * * *",
        kickoff_time_input_arg="kickoff_time",
    )
)
```

### Registering Launch Plans

Any of the methods described in the {doc}`package_register` guide will register
a launchplan as long as it's defined in any of the Python modules that you
want to register to a Nebula backend.

### Activating a Schedule

Once you've registered your launch plan, You can use the `NebulaRemote` client or
the `nebulactl` CLI to activate the schedule:

:::::{tabs}

::::{group-tab} `NebulaRemote`

:::{code-block}
launchplan_id = remote.fetch_launch_plan(name="process_data_lp").id
remote.client.update_launch_plan(launchplan_id, "ACTIVE")
:::

::::

::::{group-tab} `nebulactl`

:::{code-block} bash
nebulactl update launchplan -p nebulaexamples -d development \
 process_data_lp --version <VERSION> --activate
:::

::::

:::::

### Deactivating a Schedule

Similarly, you can deactivate a launchplan with:

:::::{tabs}

::::{group-tab} `NebulaRemote`

:::{code-block}
launchplan_id = remote.fetch_launch_plan(name="process_data_lp").id
remote.client.update_launch_plan(launchplan_id, "INACTIVE")
:::

::::

::::{group-tab} `nebulactl`

:::{code-block} bash
nebulactl update launchplan -p nebulaexamples -d development \
 process_data_lp --version <VERSION> --archive
:::

::::

:::::

## What's Next?

In this guide, you learned about how to:

- Run tasks, workflows, and launch plans using `NebulaRemote`.
- Create a cron schedule to run a launch plan at a specified time interval.

In the next guide, you'll learn how to visualize tasks using Nebula Decks.
