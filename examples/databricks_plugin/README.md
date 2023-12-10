# Databricks

```{eval-rst}
.. tags:: Spark, Integration, DistributedComputing, Data, Advanced
```

Nebula can be seamlessly integrated with the [Databricks](https://www.databricks.com/) service,
enabling you to effortlessly submit Spark jobs to the Databricks platform.

## Install the plugin

The Databricks plugin comes bundled with the Spark plugin.
To execute it locally, run the following command:

```
pip install nebulakitplugins-spark
```

If you intend to run the plugin on the Nebula cluster, you must first set it up on the backend.
Please refer to the
{std:ref}`Databricks plugin setup guide <nebula:deployment-plugin-setup-webapi-databricks>`
for detailed instructions.

## Run the example on the Nebula cluster

To run the provided example on the Nebula cluster, use the following command:

```
pynebula run --remote \
  --image ghcr.io/nebulaclouds/nebulacookbook:databricks_plugin-latest \
  https://raw.githubusercontent.com/nebulaclouds/nebulasnacks/master/examples/databricks_plugin/databricks_plugin/databricks_job.py \
  my_databricks_job
```

:::{note}
Using Spark on Databricks is incredibly simple and offers comprehensive versioning through a
custom-built Spark container. This built container also facilitates the execution of standard Spark tasks.

To utilize Spark, the image should employ a base image provided by Databricks,
and the workflow code must be copied to `/databricks/driver`.

```{literalinclude} ../../../examples/databricks_plugin/Dockerfile
:language: docker
:emphasize-lines: 1,7-8,20
```

:::

```{auto-examples-toc}
databricks_job
```
