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

(getting_started_creating_nebula_project)=

# Creating a Nebula Project

So far we've been dealing with fairly simple workflows composed of a handful of
tasks, all of which can fit into a single Python script. In this guide, you'll
learn how to organize a Nebula project so that it can scale to a larger codebase.

```{admonition} Prerequisites
:class: important

- Install `nebulakit` and `nebulactl` according to the
[introduction guide](getting_started_installation) instructions.
- Install [`git`](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
```

A Nebula project is essentially a directory containing workflows, internal Python
source code, configuration, and other artifacts needed to package up your code
so that it can be run on a Nebula cluster.

`pynebula`, the CLI tool that ships with `nebulakit`, comes with an `init` command
that you can use to quickly initialize a Nebula project according to the
recommended file structure.

```{prompt} bash $
pynebula init my_project
cd my_project
git init  # initialize a git repository
```

## Project Structure

If you examine `my_project`, you'll see the following file structure:

```{code-block} bash
my_project
├── Dockerfile        # Docker image
├── LICENSE
├── README.md
├── docker_build.sh   # Docker build helper script
├── requirements.txt  # Python dependencies
└── workflows
    ├── __init__.py
    └── example.py    # Example Nebula workflows
```

```{note}
You can create your own conventions and file structure for your Nebula projects.
The `pynebula init` command simply provides a good starting point.
```

In the rest of this guide we'll orient you to all the important pieces of the
minimal Nebula project template.

## Create a Virtual Environment

We recommend creating a virtual environment for your Nebula project so you that
you can isolate its dependencies:

```{prompt} bash $
python -m venv ~/venvs/my_project
source ~/venvs/my_project/bin/activate
pip install -r requirements.txt
```

```{note}
You can also use other tools like [miniconda](https://docs.conda.io/en/latest/miniconda.html)
to create a virtual environment.
```

## Example Workflows

The `workflows/example.py` module contains a simple set of tasks and workflows
that you can use to make sure that everything's working as expected:

```{prompt} bash $
python workflows/example.py
```

````{dropdown} See Workflow

```{rli} https://raw.githubusercontent.com/nebulaclouds/nebulakit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/workflows/example.py
:language: python
```

````

````{div} shadow p-3 mb-8 rounded
**Expected output**

```{code-block}
Running wf() DefaultNamedTupleOutput(o0='hello passengers!', o1=17)
```

````

(getting_started_python_dependencies)=

## Python Dependencies

You can specify additional Python dependencies in your project by updating the
`requirements.txt` file. This gives you the flexibility to use any
pip-installable package that your project may need.

```{note}
We recommend using [pip-compile](https://pip-tools.readthedocs.io/en/latest/) to
manage the requirements of your project.
```

````{dropdown} See requirements.txt

```{rli} https://raw.githubusercontent.com/nebulaclouds/nebulakit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/requirements.txt
:caption: requirements.txt
```

````

(getting_started_dockerfile)=

## Dockerfile

The minimal Nebula project ships with a `Dockerfile` that defines the
system requirements for running your tasks and workflows. You can customize this
image to suit your needs:

````{dropdown} See Dockerfile

```{rli} https://raw.githubusercontent.com/nebulaclouds/nebulakit-python-template/main/simple-example/%7B%7Bcookiecutter.project_name%7D%7D/Dockerfile
:language: docker
```

````
```{admonition} ImageSpec
Nebula includes a feature that builds a custom image without having to write a Dockerfile. [Learn more here](https://docs.nebula.org/projects/cookbook/en/latest/auto_examples/customizing_dependencies/image_spec.html#image-spec-example)
```

## What's Next?

In summary, this guide took you through the recommended way of initializing and
structuring a larger Nebula codebase. In the next guide, we'll walk through how
to package and register your tasks and workflows so that they can be executed on
a Nebula cluster.
