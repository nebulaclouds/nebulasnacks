# %% [markdown]
# # Running a Workflow
#
# Workflows on their own are not runnable directly. However, a launchplan is always bound to a workflow and you can use
# launchplans to **launch** a workflow. For cases in which you want the launchplan to have the same arguments as a workflow,
# if you are using one of the SDK's to author your workflows - like nebulakit, nebulakit-java etc, then they should
# automatically create a `default launchplan` for the workflow.
#
# A `default launchplan` has the same name as the workflow and all argument defaults are similar. See
# {ref}`Launch Plans` to run a workflow via the default launchplan.
#
# {ref}`Tasks also can be executed <task>` using the launch command.
# One difference between running a task and a workflow via launchplans is that launchplans cannot be associated with a
# task. This is to avoid triggers and scheduling.
#
# ## NebulaRemote
#
# Workflows can be executed with NebulaRemote because under the hood it fetches and triggers a default launch plan.
#
# ```python
# from nebulakit.remote import NebulaRemote
# from nebulakit.configuration import Config
#
# # NebulaRemote object is the main entrypoint to API
# remote = NebulaRemote(
#     config=Config.for_endpoint(endpoint="nebula.example.net"),
#     default_project="nebulasnacks",
#     default_domain="development",
# )
#
# # Fetch workflow
# nebula_workflow = remote.fetch_workflow(name="workflows.example.wf", version="v1")
#
# # Execute
# execution = remote.execute(
#     nebula_workflow, inputs={"mean": 1}, execution_name="workflow-execution", wait=True
# )
#
# # Or use execution_name_prefix to avoid repeated execution names
# execution = remote.execute(
#     nebula_workflow, inputs={"mean": 1}, execution_name_prefix="nebula", wait=True
# )
# ```
#
