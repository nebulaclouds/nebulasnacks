# Airflow Provider

```{eval-rst}
.. tags:: Integration, Intermediate
```

```{image} https://img.shields.io/badge/Blog-Airflow-blue?style=for-the-badge
:target: https://blog.nebula.org/scale-airflow-for-machine-learning-tasks-with-the-nebula-airflow-provider
:alt: Airflow Blog Post
```

The `airflow-provider-nebula` package provides an operator, a sensor, and a hook that integrates Nebula into Apache Airflow.
`NebulaOperator` is helpful to trigger a task/workflow in Nebula and `NebulaSensor` enables monitoring a Nebula execution status for completion.

The primary use case of this provider is to **scale Airflow for machine learning tasks using Nebula**.
With the Nebula Airflow provider, you can construct your ETL pipelines in Airflow and machine learning pipelines in Nebula
and use the provider to trigger machine learning or Nebula pipelines from within Airflow.

## Installation

```
pip install airflow-provider-nebula
```

All the configuration options for the provider are available in the provider repo's [README](https://github.com/nebulaclouds/airflow-provider-nebula#readme).

```{auto-examples-toc}
airflow
```
