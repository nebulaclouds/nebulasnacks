(plugins-snowflake)=

# Snowflake

```{eval-rst}
.. tags:: Integration, Data, Advanced, SQL
```

Nebula can be seamlessly integrated with the [Snowflake](https://www.snowflake.com) service,
providing you with a straightforward means to query data in Snowflake.

## Install the plugin

To use the Snowflake plugin, run the following command:

```
pip install nebulakitplugins-snowflake
```

If you intend to run the plugin on the Nebula cluster, you must first set it up on the backend.
Please refer to the
{std:ref}`Snowflake plugin setup guide <nebula:deployment-plugin-setup-webapi-snowflake>`
for detailed instructions.

## Run the example on the Nebula cluster

To run the provided example on the Nebula cluster, use the following command:

```
pynebula run --remote \
  https://raw.githubusercontent.com/nebulaclouds/nebulasnacks/master/examples/snowflake_plugin/snowflake_plugin/snowflake.py \
  snowflake_wf --nation_key 10
```

```{auto-examples-toc}
snowflake
```
