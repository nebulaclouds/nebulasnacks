# %% [markdown]
# (remote_launchplan)=
#
# # Running a Launchplan
#
# ## Nebulactl
#
# This is multi-steps process where we create an execution spec file, update the spec file and then create the execution.
# More details can be found [here](https://docs.nebula.org/projects/nebulactl/en/stable/gen/nebulactl_create_execution.html).
#
# **Generate an execution spec file**
#
# ```
# nebulactl get launchplan -p nebulasnacks -d development myapp.workflows.example.my_wf  --execFile exec_spec.yaml
# ```
#
# **Update the input spec file for arguments to the workflow**
#
# ```
# ....
# inputs:
#     name: "adam"
# ....
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
# A launch plan can be launched via NebulaRemote programmatically.
#
# ```python
# from nebulakit.remote import NebulaRemote
# from nebulakit.configuration import Config
# from nebulakit import LaunchPlan
#
# # NebulaRemote object is the main entrypoint to API
# remote = NebulaRemote(
#     config=Config.for_endpoint(endpoint="nebula.example.net"),
#     default_project="nebulasnacks",
#     default_domain="development",
# )
#
# # Fetch launch plan
# nebula_lp = remote.fetch_launch_plan(
#     name="workflows.example.wf", version="v1", project="nebulasnacks", domain="development"
# )
#
# # Execute
# execution = remote.execute(
#     nebula_lp, inputs={"mean": 1}, execution_name="lp-execution", wait=True
# )
#
# # Or use execution_name_prefix to avoid repeated execution names
# execution = remote.execute(
#     nebula_lp, inputs={"mean": 1}, execution_name_prefix="nebula", wait=True
# )
# ```
#
