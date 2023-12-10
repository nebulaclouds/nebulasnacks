(kftensorflow-plugin)=

# TensorFlow Distributed

```{eval-rst}
.. tags:: Integration, DistributedComputing, MachineLearning, KubernetesOperator, Advanced
```

TensorFlow operator is useful to natively run distributed TensorFlow training jobs on Nebula.
It leverages the [Kubeflow training operator](https://github.com/kubeflow/training-operator).

## Install the plugin

To install the Kubeflow TensorFlow plugin, run the following command:

```
pip install nebulakitplugins-kftensorflow
```

To enable the plugin in the backend, follow instructions outlined in the {std:ref}`nebula:deployment-plugin-setup-k8s` guide.

## Run the example on the Nebula cluster

To run the provided example on the Nebula cluster, use the following command:

```
pynebula run --remote tf_mnist.py \
  mnist_tensorflow_workflow
```

```{auto-examples-toc}
tf_mnist
```
