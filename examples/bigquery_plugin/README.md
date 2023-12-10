(big-query)=

# BigQuery

```{eval-rst}
.. tags:: GCP, Data, Integration, Advanced
```

Nebula backend can be connected with BigQuery service. Once enabled, it can allow you to query a BigQuery table.
This section will provide how to use the BigQuery Plugin using nebulakit python.

## Installation

To use the nebulakit bigquery plugin simply run the following:

```{eval-rst}
.. prompt:: bash

    pip install nebulakitplugins-bigquery
```

This plugin is purely a spec. Since SQL is completely portable, there is no need to build a Docker container.

## Configuring the backend to get bigquery working

BigQuery plugins are [enabled in nebulapropeller's config](https://docs.nebula.org/en/latest/deployment/plugin_setup/gcp/bigquery.html#deployment-plugin-setup-gcp-bigquery)

```{auto-examples-toc}
bigquery
```
