(mlflow)=

# MLFlow

```{eval-rst}
.. tags:: Integration, Data, Metrics, Intermediate
```

The MLflow Tracking component is an API and UI for logging parameters,
code versions, metrics, and output files when running your machine learning code and for later visualizing the results

First, install the Nebula MLflow plugin:

```{eval-rst}
.. prompt:: bash $

    pip install nebulakitplugins-mlflow
```

To log the metrics and parameters to Nebula deck, add {py:func}`@mlflow_autolog <nebulakitplugins.mlflow.mlflow_autolog>` to the task. For example

```python
@task(disable_deck=False)
@mlflow_autolog(framework=mlflow.keras)
def train_model(epochs: int):
...
```

To log the metric and parameters to a remote mlflow server, add default environment variable [MLFLOW_TRACKING_URI](https://mlflow.org/docs/latest/tracking.html#logging-to-a-tracking-server) to the nebulapropeller config map.

```{eval-rst}
.. prompt:: bash $

    kubectl edit cm nebula-propeller-config
```

```yaml
plugins:
  k8s:
    default-cpus: 100m
    default-env-vars:
    - MLFLOW_TRACKING_URI: postgresql+psycopg2://postgres:@postgres.nebula.svc.cluster.local:5432/nebulaadmin
```

:::{figure} https://raw.githubusercontent.com/nebulaclouds/static-resources/f4b53a550bed70d9d7722d523e0b7568b781fc7d/nebulasnacks/integrations/mlflow/server.png
:alt: MLflow UI
:class: with-shadow
:::

```{auto-examples-toc}
mlflow_example
```
