(aws-athena)=

# AWS Athena

```{eval-rst}
.. tags:: Data, Integration, AWS, Advanced
```

## Executing Athena Queries

Nebula backend can be connected with Athena. Once enabled, it allows you to query AWS Athena service (Presto + ANSI SQL Support) and retrieve typed schema (optionally).
This plugin is purely a spec and since SQL is completely portable, it has no need to build a container. Thus this plugin example does not have any Dockerfile.

### Installation

To use the nebulakit Athena plugin, simply run the following:

```{eval-rst}
.. prompt:: bash

    pip install nebulakitplugins-athena
```

Now let's dive into the code.

```{auto-examples-toc}
athena
```
