# %% [markdown]
# # NebulaOperator Example
#
# This tutorial will walk you through constructing an Airflow DAG using the `NebulaOperator`.
#
# :::{note}
# The provider source code can be found in the [airflow-provider-nebula](https://github.com/nebulaclouds/airflow-provider-nebula) repository.
# :::
#
# Watch a demo of this provider below! It demonstrates an example of pulling NYC taxi data from S3, uploading it to CrateDB,
# and building an XGBoost model. The extract and load steps are handled by Airflow and the machine learning task is offloaded to Nebula
# using the Nebula Airflow Provider.
#
# ```{eval-rst}
# ..  youtube:: F2JyA0O2U4M
# ```
#
# The Airflow DAG demonstrated in the video is available [here](https://github.com/nebulaclouds/airflow-provider-nebula/blob/master/demo/dags/nyc_taxi.py).
#
# ## Environment Setup
#
# **AIRFLOW**
#
# Astronomer's CLI is the fastest and easiest way to set up Airflow.
#
# Download the [Astro CLI](https://github.com/astronomer/astro-cli) and then initialize a new astro project.
#
# ```
# mkdir nebula-astro-project
# cd nebula-astro-project
# astro dev init
# ```
#
# The directory structure of `nebula-astro-project` would look as follows:
#
# ```
# .
# ├── Dockerfile
# ├── README.md
# ├── airflow_settings.yaml
# ├── dags
# │   ├── example-dag-advanced.py
# │   └── example-dag-basic.py
# ├── include
# ├── packages.txt
# ├── plugins
# ├── requirements.txt
# └── tests
#     └── dags
#         └── test_dag_integrity.py
# ```
#
# **NEBULA**
#
# The [getting started tutorial](https://docs.nebula.org/en/latest/getting_started/index.html) should help you with setting up Nebula.
#
# ## Create an Airflow Connection
#
# Hit `http://localhost:8080/`, give the credentials (default username and password: `admin`), navigate to `Connections` and create a
# Nebula connection.
#
# ```{image} https://raw.githubusercontent.com/nebulaclouds/static-resources/main/nebulasnacks/integrations/airflow/airflow_connection.png
# :alt: Airflow Connection
# ```
#
# Click `Save` in the end.
#
# :::{note}
# Use external IP as the Nebula `Host`. You can {std:ref}`deploy <deployment>` Nebula on an on-prem machine or on cloud.
# :::
#
# ## Register Nebula Code
#
# At the Nebula end, we'll train an XGBoost model on Pima Indians Diabetes Dataset.
# The source code is available [here](https://github.com/nebulaclouds/nebulasnacks/blob/master/cookbook/case_studies/pima_diabetes/diabetes.py).
#
# Register the example on the Nebula backend before proceeding with running the Airflow DAG.
#
# - Configure nebulactl config at `~/.nebula/config.yaml` to point to the relevant endpoint.
#
#   ```yaml
#   admin:
#     endpoint: dns:///<your-endpoint>
#     insecure: true # Set to false to enable TLS/SSL connection.
#     authType: Pkce # authType: Pkce # if using authentication or just drop this.
#   ```
#
# - Clone the [nebulasnacks repository](https://github.com/nebulaclouds/nebulasnacks) and go into the `examples` directory.
#
#   ```
#   git clone https://github.com/nebulaclouds/nebulasnacks
#   cd nebulasnacks/examples
#   ```
#
# - Serialize the workflow.
#
#   ```
#   pynebula --pkgs pima_diabetes package --image "ghcr.io/nebulaclouds/nebulacookbook:pima_diabetes-latest" -f
#   ```
#
# - Register the workflow.
#
#   ```
#   nebulactl register files --project nebulasnacks --domain development --archive nebula-package.tgz --version v1
#   ```

# %% [markdown]
# ## Create an Airflow DAG
#
# Place the following file under the `dags/` directory. You can name it `example_dag_nebula.py`.
# %%
from datetime import datetime, timedelta

from airflow import DAG
from nebula_provider.operators.nebula import NebulaOperator
from nebula_provider.sensors.nebula import NebulaSensor

with DAG(
    dag_id="example_nebula",
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    dagrun_timeout=timedelta(minutes=60),
    catchup=False,
) as dag:
    task = NebulaOperator(
        task_id="diabetes_predictions",
        nebula_conn_id="nebula_conn",
        project="nebulasnacks",
        domain="development",
        launchplan_name="ml_training.pima_diabetes.diabetes.diabetes_xgboost_model",
        inputs={"test_split_ratio": 0.66, "seed": 5},
    )

    sensor = NebulaSensor(
        task_id="sensor",
        execution_name=task.output,
        project="nebulasnacks",
        domain="development",
        nebula_conn_id="nebula_conn",
    )

    task >> sensor

# %% [markdown]
# Also, add `airflow-provider-nebula` package to `requirements.txt` under the astro project.

# %% [markdown]
# ## Run the Workflow
#
# - Run the command `astro dev start`.
# - Trigger the Airflow DAG by clicking the "Trigger DAG" button on the Airflow UI.
# - Verify if Nebula execution got triggered on the NebulaConsole by going to `http://<path>` and navigating to the workflow page.

# %% [markdown]
# That's about it! With the Nebula Airflow Provider, you get to reap the benefits of Nebula, a full-fledged machine learning orchestration service,
# as an extension to Airflow.
# For more example DAGs, refer to [this folder](https://github.com/nebulaclouds/airflow-provider-nebula/tree/master/nebula_provider/example_dags).
#
