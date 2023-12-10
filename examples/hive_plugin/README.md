# Hive

```{eval-rst}
.. tags:: Integration, Data, Advanced
```

Nebula backend can be connected with various hive services. Once enabled it can allow you to query a hive service (e.g. Qubole) and retrieve typed schema (optionally).
This section will provide how to use the Hive Query Plugin using nebulakit python

## Installation

To use the nebulakit hive plugin simply run the following:

```{eval-rst}
.. prompt:: bash

    pip install nebulakitplugins-hive
```

## No Need of a dockerfile

This plugin is purely a spec. Since SQL is completely portable there is no need to build a Docker container.

% TODO: write a subsection for "Configuring the backend to get hive working"

```{auto-examples-toc}
hive
```