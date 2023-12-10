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

# override the toc-determined page navigation order
next-page: getting_started/nebula_fundamentals
next-page-title: Nebula Fundamentals
---

(getting_started_index)=

# Getting Started

{doc}`Example Tags <_tags/tagsindex>`

## Introduction to Nebula

Nebula is a workflow orchestrator that seamlessly unifies data,
machine learning, and analytics stacks for building robust and reliable
applications.

This introduction provides a quick overview of how to get Nebula up and running
on your local machine.

````{dropdown} Want to try Nebula on the browser?
:title: text-muted
:animate: fade-in-slide-down

The introduction below is also available on a hosted sandbox environment, where
you can get started with Nebula without installing anything locally.

```{link-button} https://sandbox.union.ai/
---
classes: try-hosted-nebula btn-warning btn-block
text: Try Hosted Nebula Sandbox
---
```

```{div} text-muted
*Courtesy of [Union.ai](https://www.union.ai/)*
```

````

(getting_started_installation)=

## Installation

```{admonition} Prerequisites
:class: important

[Install Docker](https://docs.docker.com/get-docker/) and ensure that you
have the Docker daemon running.

Nebula supports any [OCI-compatible](https://opencontainers.org/) container
technology (like [Podman](https://podman.io/),
[LXD](https://linuxcontainers.org/lxd/introduction/), and
[Containerd](https://containerd.io/)) when running tasks on a Nebula cluster, but
for the purpose of this guide, `nebulactl` uses Docker to spin up a local
Kubernetes cluster so that you can interact with it on your machine.
```

First install [nebulakit](https://pypi.org/project/nebulakit/), Nebula's Python SDK and [Scikit-learn](https://scikit-learn.org/stable).

```{prompt} bash $
pip install nebulakit nebulakitplugins-deck-standard scikit-learn
```

Then install [nebulactl](https://docs.nebula.org/projects/nebulactl/en/latest/),
which the command-line interface for interacting with a Nebula backend.

````{tabbed} Homebrew

```{prompt} bash $
brew install nebulaclouds/homebrew-tap/nebulactl
```

````

````{tabbed} Curl

```{prompt} bash $
curl -sL https://ctl.nebula.org/install | sudo bash -s -- -b /usr/local/bin
```

````

## Creating a Workflow

The first workflow we'll create is a simple model training workflow that consists
of three steps that will:

1. 🍷 Get the classic [wine dataset](https://scikit-learn.org/stable/datasets/toy_dataset.html#wine-recognition-dataset)
   using [sklearn](https://scikit-learn.org/stable/).
2. 📊 Process the data that simplifies the 3-class prediction problem into a
   binary classification problem by consolidating class labels `1` and `2` into
   a single class.
3. 🤖 Train a `LogisticRegression` model to learn a binary classifier.

First, we'll define three tasks for each of these steps. Create a file called
`example.py` and copy the following code into it.

```{code-cell} python
:tags: [remove-output]

import pandas as pd
from sklearn.datasets import load_wine
from sklearn.linear_model import LogisticRegression

import nebulakit.extras.sklearn
from nebulakit import task, workflow


@task
def get_data() -> pd.DataFrame:
    """Get the wine dataset."""
    return load_wine(as_frame=True).frame

@task
def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """Simplify the task from a 3-class to a binary classification problem."""
    return data.assign(target=lambda x: x["target"].where(x["target"] == 0, 1))

@task
def train_model(data: pd.DataFrame, hyperparameters: dict) -> LogisticRegression:
    """Train a model on the wine dataset."""
    features = data.drop("target", axis="columns")
    target = data["target"]
    return LogisticRegression(max_iter=3000, **hyperparameters).fit(features, target)
```

As we can see in the code snippet above, we defined three tasks as Python
functions: `get_data`, `process_data`, and `train_model`.

In Nebula, **tasks** are the most basic unit of compute and serve as the building
blocks 🧱 for more complex applications. A task is a function that takes some
inputs and produces an output. We can use these tasks to define a simple model
training workflow:

```{code-cell} python
@workflow
def training_workflow(hyperparameters: dict) -> LogisticRegression:
    """Put all of the steps together into a single workflow."""
    data = get_data()
    processed_data = process_data(data=data)
    return train_model(
        data=processed_data,
        hyperparameters=hyperparameters,
    )
```

```{note}
A task can also be an isolated piece of compute that takes no inputs and
produces no output, but for the most part to do something useful a task
is typically written with inputs and outputs.
```

A **workflow** is also defined as a Python function, and it specifies the flow
of data between tasks and, more generally, the dependencies between tasks 🔀.

::::{dropdown} {fa}`info-circle` The code above looks like Python, but what do `@task` and `@workflow` do exactly?
:title: text-muted
:animate: fade-in-slide-down

Nebula `@task` and `@workflow` decorators are designed to work seamlessly with
your code-base, provided that the _decorated function is at the top-level scope
of the module_.

This means that you can invoke tasks and workflows as regular Python methods and
even import and use them in other Python modules or scripts.

:::{note}
A {func}`task <nebulakit.task>` is a pure Python function, while a {func}`workflow <nebulakit.workflow>`
is actually a [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) that
only supports a subset of Python's semantics. Learn more in the
{ref}`Nebula Fundamentals <workflows_versus_task_syntax>` section.
:::

::::

(intro_running_nebula_workflows)=

## Running Nebula Workflows in Python

You can run the workflow in `example.py` on a local Python by using `pynebula`,
the CLI that ships with `nebulakit`.

```{prompt} bash $
pynebula run example.py training_workflow \
    --hyperparameters '{"C": 0.1}'
```

:::::{dropdown} {fa}`info-circle` Running into shell issues?
:title: text-muted
:animate: fade-in-slide-down

If you're using Bash, you can ignore this 🙂
You may need to add .local/bin to your PATH variable if it's not already set,
as that's not automatically added for non-bourne shells like fish or xzsh.

To use pynebula, make sure to set the /.local/bin directory in PATH

:::{code-block} fish
set -gx PATH $PATH ~/.local/bin
:::
:::::

:::::{dropdown} {fa}`info-circle` Why use `pynebula run` rather than `python example.py`?
:title: text-muted
:animate: fade-in-slide-down

`pynebula run` enables you to execute a specific workflow using the syntax
`pynebula run <path/to/script.py> <workflow_or_task_function_name>`.

Keyword arguments can be supplied to `pynebula run` by passing in options in
the format `--kwarg value`, and in the case of `snake_case_arg` argument
names, you can pass in options in the form of `--snake-case-arg value`.

::::{note}
If you want to run a workflow with `python example.py`, you would have to write
a `main` module conditional at the end of the script to actually run the
workflow:

```python
if __name__ == "__main__":
    training_workflow(hyperparameters={"C": 0.1})
```

This becomes even more verbose if you want to pass in arguments:

```python
if __name__ == "__main__":
    import json
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--hyperparameters", type=json.loads)
    ...  # add the other options

    args = parser.parse_args()
    training_workflow(hyperparameters=args.hyperparameters)
```

::::

:::::

(getting_started_nebula_cluster)=

## Running Workflows in a Nebula Cluster

You can also use `pynebula run` to execute workflows on a Nebula cluster.
To do so, first spin up a local demo cluster. `nebulactl` uses Docker to create
a local Kubernetes cluster and minimal Nebula backend that you can use to run
the example above:

```{important}
Before you start the local cluster, make sure that you allocate a minimum of
`4 CPUs` and `3 GB` of memory in your Docker daemon. If you're using the
[Docker Desktop](https://www.docker.com/products/docker-desktop/), you can
do this easily by going to:

`Settings > Resources > Advanced`

Then set the **CPUs** and **Memory** sliders to the appropriate levels.
```

```{prompt} bash $
nebulactl demo start
```

````{div} shadow p-3 mb-8 rounded
**Expected Output:**

```{code-block}
👨‍💻 Nebula is ready! Nebula UI is available at http://localhost:30080/console 🚀 🚀 🎉
❇️ Run the following command to export sandbox environment variables for accessing nebulactl
	export NEBULACTL_CONFIG=~/.nebula/config-sandbox.yaml
🐋 Nebula sandbox ships with a Docker registry. Tag and push custom workflow images to localhost:30000
📂 The Minio API is hosted on localhost:30002. Use http://localhost:30080/minio/login for Minio console
```

```{important}
Make sure to export the `NEBULACTL_CONFIG=~/.nebula/config-sandbox.yaml` environment
variable in your shell.
```
````

Then, run the workflow on the Nebula cluster with `pynebula run` using the
`--remote` flag:

```{prompt} bash $
pynebula run --remote example.py training_workflow \
    --hyperparameters '{"C": 0.1}'
```

````{div} shadow p-3 mb-8 rounded

**Expected Output:** A URL to the workflow execution on your demo Nebula cluster:

```{code-block}
Go to http://localhost:30080/console/projects/nebulasnacks/domains/development/executions/<execution_name> to see execution in the console.
```

Where ``<execution_name>`` is a unique identifier for the workflow execution.

````

## Inspect the Results

Navigate to the URL produced by `pynebula run`. This will take you to
NebulaConsole, the web UI used to manage Nebula entities such as tasks,
workflows, and executions.

![getting started console](https://github.com/nebulaclouds/static-resources/raw/main/nebulasnacks/getting_started/getting_started_console.gif)

```{note}
There are a few features about NebulaConsole worth pointing out in the GIF above:

- The default execution view shows the list of tasks executing in sequential order.
- The right-hand panel shows metadata about the task execution, including logs, inputs, outputs, and task metadata.
- The **Graph** view shows the execution graph of the workflow, providing visual information about the topology
  of the graph and the state of each node as the workflow progresses.
- On completion, you can inspect the outputs of each task, and ultimately, the overarching workflow.
```

## Summary

🎉 **Congratulations! In this introductory guide, you:**

1. 📜 Created a Nebula script, which trains a binary classification model.
2. 🚀 Spun up a demo Nebula cluster on your local system.
3. 👟 Ran a workflow locally and on a demo Nebula cluster.

## What's Next?

Follow the rest of the sections in the documentation to get a better
understanding of the key constructs that make Nebula such a powerful
orchestration tool 💪.

```{admonition} Recommendation
:class: tip

If you're new to Nebula we recommend that you go through the
{ref}`Nebula Fundamentals <getting_started_fundamentals>` and
{ref}`Core Use Cases <getting_started_core_use_cases>` section before diving
into the other sections of the documentation.
```

```{list-table}
:header-rows: 0
:widths: 10 30

* - {ref}`🔤 Nebula Fundamentals <getting_started_fundamentals>`
  - A brief tour of the Nebula's main concepts and development lifecycle
* - {ref}`🌟 Core Use Cases <getting_started_core_use_cases>`
  - An overview of core uses cases for data, machine learning, and analytics
    practitioners.
* - {ref}`📖 User Guide <userguide>`
  - A comprehensive view of Nebula's functionality for data scientists,
    ML engineers, data engineers, and data analysts.
* - {ref}`📚 Tutorials <tutorials>`
  - End-to-end examples of Nebula for data/feature engineering, machine learning,
    bioinformatics, and more.
* - {ref}`🚀 Deployment Guide <deployment>`
  - Guides for platform engineers to deploy a Nebula cluster on your own
    infrastructure.
```

```{toctree}
:maxdepth: 1
:hidden:

|plane| Getting Started <self>
|book-reader| User Guide <userguide>
|chalkboard| Tutorials <tutorials>
|project-diagram| Concepts <https://docs.nebula.org/en/latest/concepts/basics.html>
|rocket| Deployment <https://docs.nebula.org/en/latest/deployment/index.html>
|book| API Reference <https://docs.nebula.org/en/latest/reference/index.html>
|hands-helping| Community <https://docs.nebula.org/en/latest/community/index.html>
```

```{toctree}
:maxdepth: -1
:caption: Getting Started
:hidden:

Introduction to Nebula <self>
getting_started/nebula_fundamentals
getting_started/core_use_cases
```

```{toctree}
:maxdepth: -1
:caption: User Guide
:hidden:

📖 User Guide <userguide>
🌳 Environment Setup <environment_setup>
🔤 Basics <auto_examples/basics/index>
⌨️ Data Types and IO <auto_examples/data_types_and_io/index>
🔮 Advanced Composition <auto_examples/advanced_composition/index>
🧩 Customizing Dependencies <auto_examples/customizing_dependencies/index>
🏡 Development Lifecycle <auto_examples/development_lifecycle/index>
⚗️ Testing <auto_examples/testing/index>
🚢 Productionizing <auto_examples/productionizing/index>
🏗 Extending <auto_examples/extending/index>
📝 Contributing <contribute>
```

```{toctree}
:maxdepth: -1
:caption: Tutorials
:hidden:

Tutorials <tutorials>
Model Training <ml_training>
feature_engineering
bioinformatics_examples
nebula_lab
```

```{toctree}
:maxdepth: -1
:caption: Integrations
:hidden:

Integrations <integrations>
auto_examples/airflow_plugin/index
auto_examples/athena_plugin/index
auto_examples/aws_batch_plugin/index
auto_examples/sagemaker_pytorch_plugin/index
auto_examples/sagemaker_training_plugin/index
auto_examples/bigquery_plugin/index
auto_examples/k8s_dask_plugin/index
auto_examples/databricks_plugin/index
auto_examples/dbt_plugin/index
auto_examples/dolt_plugin/index
auto_examples/duckdb_plugin/index
auto_examples/greatexpectations_plugin/index
auto_examples/hive_plugin/index
auto_examples/k8s_pod_plugin/index
auto_examples/mlflow_plugin/index
auto_examples/mmcloud_plugin/index
auto_examples/modin_plugin/index
auto_examples/kfmpi_plugin/index
auto_examples/onnx_plugin/index
auto_examples/papermill_plugin/index
auto_examples/pandera_plugin/index
auto_examples/kfpytorch_plugin/index
auto_examples/ray_plugin/index
auto_examples/sensor/index
auto_examples/snowflake_plugin/index
auto_examples/k8s_spark_plugin/index
auto_examples/sql_plugin/index
auto_examples/kftensorflow_plugin/index
auto_examples/whylogs_plugin/index
```

```{toctree}
:maxdepth: -1
:caption: Tags
:hidden:

_tags/tagsindex
```
