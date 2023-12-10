# %% [markdown]
# # Inspecting Workflow and Task Executions
#
# ## Nebulactl
#
# Nebulactl supports inspecting execution by retrieving its details. For a deeper dive, refer to the
# [API reference](https://docs.nebula.org/projects/nebulactl/en/stable/gen/nebulactl_get_execution.html) guide.
#
# Monitor the execution by providing the execution id from create command which can be task or workflow execution.
#
# ```
# nebulactl get execution -p nebulasnacks -d development <execid>
# ```
#
# For more details use `--details` flag which shows node executions along with task executions on them.
#
# ```
# nebulactl get execution -p nebulasnacks -d development <execid> --details
# ```
#
# If you prefer to see yaml/json view for the details then change the output format using the -o flag.
#
# ```
# nebulactl get execution -p nebulasnacks -d development <execid> --details -o yaml
# ```
#
# To see the results of the execution you can inspect the node closure outputUri in detailed yaml output.
#
# ```
# "outputUri": "s3://my-s3-bucket/metadata/propeller/nebulasnacks-development-<execid>/n0/data/0/outputs.pb"
# ```
#
# ## NebulaRemote
#
# With NebulaRemote, you can fetch the inputs and outputs of executions and inspect them.
#
# ```python
# from nebulakit.remote import NebulaRemote
#
# # NebulaRemote object is the main entrypoint to API
# remote = NebulaRemote(
#     config=Config.for_endpoint(endpoint="nebula.example.net"),
#     default_project="nebulasnacks",
#     default_domain="development",
# )
#
# execution = remote.fetch_execution(
#     name="fb22e306a0d91e1c6000", project="nebulasnacks", domain="development"
# )
#
# input_keys = execution.inputs.keys()
# output_keys = execution.outputs.keys()
#
# # The inputs and outputs correspond to the top-level execution or the workflow itself.
# # To fetch a specific output, say, a model file:
# model_file = execution.outputs["model_file"]
# with open(model_file) as f:
#     ...
#
# # You can use NebulaRemote.sync() to sync the entity object's state with the remote state during the execution run.
# synced_execution = remote.sync(execution, sync_nodes=True)
# node_keys = synced_execution.node_executions.keys()
#
# # node_executions will fetch all the underlying node executions recursively.
# # To fetch output of a specific node execution:
# node_execution_output = synced_execution.node_executions["n1"].outputs["model_file"]
# ```
#
