# %% [markdown]
# (configure-logging)=
#
# # Configuring Logging Links in UI
#
# ```{eval-rst}
# .. tags:: Deployment, Intermediate, UI
# ```
#
# To debug your workflows in production, you want to access logs from your tasks as they run.
# These logs are different from the core Nebula platform logs, are specific to execution, and may vary from plugin to plugin;
# for example, Spark may have driver and executor logs.
#
# Every organization potentially uses different log aggregators, making it hard to create a one-size-fits-all solution.
# Some examples of the log aggregators include cloud-hosted solutions like AWS CloudWatch, GCP Stackdriver, Splunk, Datadog, etc.
#
# Nebula provides a simplified interface to configure your log provider. Nebula-sandbox
# ships with the Kubernetes dashboard to visualize the logs. This may not be safe for production, hence we recommend users
# explore other log aggregators.
#
# ## How to configure?
#
# To configure your log provider, the provider needs to support `URL` links that are shareable and can be templatized.
# The templating engine has access to [these](https://github.com/nebulaclouds/nebulaplugins/blob/b0684d97a1cf240f1a44f310f4a79cc21844caa9/go/tasks/pluginmachinery/tasklog/plugin.go#L7-L16) parameters.
#
# The parameters can be used to generate a unique URL to the logs using a templated URI that pertain to a specific task. The templated URI has access to the following parameters:
#
# ```{eval-rst}
# .. list-table:: Parameters to generate a templated URI
#    :widths: 25 50
#    :header-rows: 1
#
#    * - Parameter
#      - Description
#    * - ``{{ .podName }}``
#      - Gets the pod name as it shows in k8s dashboard
#    * - ``{{ .podUID }}``
#      - The pod UID generated by the k8s at runtime
#    * - ``{{ .namespace }}``
#      - K8s namespace where the pod runs
#    * - ``{{ .containerName }}``
#      - The container name that generated the log
#    * - ``{{ .containerId }}``
#      - The container id docker/crio generated at run time
#    * - ``{{ .logName }}``
#      - A deployment specific name where to expect the logs to be
#    * - ``{{ .hostname }}``
#      - The hostname where the pod is running and logs reside
#    * - ``{{ .podRFC3339StartTime }}``
#      - The pod creation time (in RFC3339 format, e.g. "2021-01-01T02:07:14Z", also conforming to ISO 8601)
#    * - ``{{ .podRFC3339FinishTime }}``
#      - Don't have a good mechanism for this yet, but approximating with ``time.Now`` for now
#    * - ``{{ .podUnixStartTime }}``
#      - The pod creation time (in unix seconds, not millis)
#    * - ``{{ .podUnixFinishTime }}``
#      - Don't have a good mechanism for this yet, but approximating with ``time.Now`` for now
# ```
#
# The parameterization engine uses Golangs native templating format and hence uses `{{ }}`. An example configuration can be seen as follows:
#
# ```yaml
# task_logs:
#   plugins:
#     logs:
#       templates:
#         - displayName: <name-to-show>
#           templateUris:
#             - "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logEventViewer:group=/nebula-production/kubernetes;stream=var.log.containers.{{.podName}}_{{.namespace}}_{{.containerName}}-{{.containerId}}.log"
#             - "https://some-other-source/home?region=us-east-1#logEventViewer:group=/nebula-production/kubernetes;stream=var.log.containers.{{.podName}}_{{.namespace}}_{{.containerName}}-{{.containerId}}.log"
#           messageFormat: 0 # this parameter is optional, but use 0 for "unknown", 1 for "csv", or 2 for "json"
# ```
#
# :::{tip}
# Since helm chart uses the same templating syntax for args (like `{{ }}`), compiling the chart results in helm replacing Nebula log link templates as well. To avoid this, you can use escaped templating for Nebula logs in the helm chart.
# This ensures that Nebula log link templates remain in place during helm chart compilation.
# For example:
#
# If your configuration looks like this:
#
# `https://someexample.com/app/podName={{ "{{" }} .podName {{ "}}" }}&containerName={{ .containerName }}`
#
# Helm chart will generate:
#
# `https://someexample.com/app/podName={{.podName}}&containerName={{.containerName}}`
#
# Nebulapropeller pod would be created as:
#
# `https://someexample.com/app/podName=pname&containerName=cname`
# :::
#
# This code snippet will output two logs per task that use the log plugin.
# However, not all task types use the log plugin; for example, the SageMaker plugin uses the log output provided by Sagemaker, and the Snowflake plugin will use a link to the snowflake console.
#
# ## Datadog Integration
#
# To send your Nebula workflow logs to Datadog, you can follow these steps:
#
# 1. Enable collection of logs from containers and collection of logs using files. The precise configuration steps will vary depending on your specific setup.
#
# For instance, if you're using Helm, use the following config:
#
# ```yaml
# logs:
#   enabled: true
#   containerCollectAll: true
#   containerCollectUsingFiles: true
# ```
#
# If you're using environment variables, use the following config:
#
# ```yaml
# DD_LOGS_ENABLED: "false"
# DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL: "true"
# DD_LOGS_CONFIG_K8S_CONTAINER_USE_FILE: "true"
# DD_CONTAINER_EXCLUDE_LOGS: "name:datadog-agent"  # This is to avoid tracking logs produced by the datadog agent itself
# ```
#
# :::{warning}
# The boolean values have to be represented as strings.
# :::
#
# 2. The Datadog [guide](https://docs.datadoghq.com/containers/kubernetes/log/?tab=daemonset) includes a section on mounting volumes. It is essential (and a prerequisite for proper functioning) to map the volumes "logpodpath" and "logcontainerpath" as illustrated in the linked example. While the "pointerdir" volume is optional, it is recommended that you map it to prevent the loss of container logs during restarts or network issues (as stated in the guide).
#
