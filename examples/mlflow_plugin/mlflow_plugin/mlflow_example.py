# %% [markdown]
# (mlflow_example)=
#
# # MLflow Example
#
# MLflow is a platform to streamline machine learning development, including tracking experiments, packaging code into reproducible runs, and sharing and deploying models.
#
# Nebula provides an easy-to-use interface to log the task's metrics and parameters to either Nebula Deck or MLflow server.

# %%
import mlflow.keras
import tensorflow as tf

# %% [markdown]
# Let's first import the libraries.
# %%
from nebulakit import task, workflow
from nebulakitplugins.mlflow import mlflow_autolog


# %% [markdown]
# Run a model training here and generate metrics and parameters.
# Add `mlflow_autolog` to the task, then nebula will automatically log the metric to the Nebula Deck.
# %%
@task(disable_deck=False)
@mlflow_autolog(framework=mlflow.keras)
def train_model(epochs: int):
    # Refer to https://www.tensorflow.org/tutorials/keras/classification
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (_, _) = fashion_mnist.load_data()
    train_images = train_images / 255.0

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10),
        ]
    )

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )
    model.fit(train_images, train_labels, epochs=epochs)


# %% [markdown]
# :::{figure} https://raw.githubusercontent.com/nebulaclouds/static-resources/f4b53a550bed70d9d7722d523e0b7568b781fc7d/nebulasnacks/integrations/mlflow/metrics.png
# :alt: Model Metrics
# :class: with-shadow
# :::
#
# :::{figure} https://raw.githubusercontent.com/nebulaclouds/static-resources/f4b53a550bed70d9d7722d523e0b7568b781fc7d/nebulasnacks/integrations/mlflow/params.png
# :alt: Model Parameters
# :class: with-shadow
# :::

# %% [markdown]
# Finally, we put everything together into a workflow:
#
# %%
@workflow
def ml_pipeline(epochs: int):
    train_model(epochs=epochs)


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    ml_pipeline(epochs=5)
