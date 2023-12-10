# %% [markdown]
# (remote_task)=
#
# # Running a Task
#
# ## Nebulactl
#
# This is a multi-step process where we create an execution spec file, update the spec file, and then create the execution.
# More details can be found in the [Nebulactl API reference](https://docs.nebula.org/projects/nebulactl/en/stable/gen/nebulactl_create_execution.html).
#
# **Generate execution spec file**
#
# ```
# nebulactl get tasks -d development -p nebulasnacks workflows.example.generate_normal_df  --latest --execFile exec_spec.yaml
# ```
#
# **Update the input spec file for arguments to the workflow**
#
# ```
# iamRoleARN: 'arn:aws:iam::12345678:role/defaultrole'
# inputs:
#   n: 200
#   mean: 0.0
#   sigma: 1.0
# kubeServiceAcct: ""
# targetDomain: ""
# targetProject: ""
# task: workflows.example.generate_normal_df
# version: "v1"
# ```
#
# **Create execution using the exec spec file**
#
# ```
# nebulactl create execution -p nebulasnacks -d development --execFile exec_spec.yaml
# ```
#
# **Monitor the execution by providing the execution id from create command**
#
# ```
# nebulactl get execution -p nebulasnacks -d development <execid>
# ```
#
# ## NebulaRemote
#
# A task can be launched via NebulaRemote programmatically.
#
# ```python
# from nebulakit.remote import NebulaRemote
# from nebulakit.configuration import Config, SerializationSettings
#
# # NebulaRemote object is the main entrypoint to API
# remote = NebulaRemote(
#     config=Config.for_endpoint(endpoint="nebula.example.net"),
#     default_project="nebulasnacks",
#     default_domain="development",
# )
#
# # Get Task
# nebula_task = remote.fetch_task(name="workflows.example.generate_normal_df", version="v1")
#
# nebula_task = remote.register_task(
#     entity=nebula_task,
#     serialization_settings=SerializationSettings(image_config=None),
#     version="v2",
# )
#
# # Run Task
# execution = remote.execute(
#      nebula_task, inputs={"n": 200, "mean": 0.0, "sigma": 1.0}, execution_name="task-execution", wait=True
# )
#
# # Or use execution_name_prefix to avoid repeated execution names
# execution = remote.execute(
#      nebula_task, inputs={"n": 200, "mean": 0.0, "sigma": 1.0}, execution_name_prefix="nebula", wait=True
# )
#
# # Inspecting execution
# # The 'inputs' and 'outputs' correspond to the task execution.
# input_keys = execution.inputs.keys()
# output_keys = execution.outputs.keys()
# ```
#
