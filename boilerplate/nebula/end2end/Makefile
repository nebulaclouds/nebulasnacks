# WARNING: THIS FILE IS MANAGED IN THE 'BOILERPLATE' REPO AND COPIED TO OTHER REPOSITORIES.
# ONLY EDIT THIS FILE FROM WITHIN THE 'NEBULACLOUDS/BOILERPLATE' REPOSITORY:
#
# TO OPT OUT OF UPDATES, SEE https://github.com/nebulaclouds/boilerplate/blob/master/Readme.rst

.PHONY: end2end_execute
end2end_execute: export NEBULASNACKS_PRIORITIES ?= P0
end2end_execute: export NEBULASNACKS_VERSION ?= $(shell curl --silent "https://api.github.com/repos/nebulaclouds/nebulasnacks/releases/latest" | jq -r .tag_name)
end2end_execute:
	./boilerplate/nebula/end2end/end2end.sh ./boilerplate/nebula/end2end/functional-test-config.yaml --return_non_zero_on_failure

.PHONY: k8s_integration_execute
k8s_integration_execute:
	echo "pass"
