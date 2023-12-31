#!/bin/sh
#
# Usage: ./scripts/serialize-example.sh <example-dir> <version>

dir="$1"
version="$2"

build() {
    docker build . -t "$1"
}

# NOTE: the additional images are for the multi-image containerization examples
serialize() {
    docker run -i --rm -v "$(pwd)":/root "$2" \
        pynebula --pkgs "$1" \
        package \
        --image "$2" \
        --image mindmeld="ghcr.io/nebulaclouds/nebulacookbook:core-latest" \
        --image borebuster="ghcr.io/nebulaclouds/nebulakit:py3.9-latest" \
        --output /root/nebula-package.tgz \
        --force
}

if [ -z "$version" ]
then
    version="latest"
fi

example_name=$(basename -- "$dir")
image_uri=ghcr.io/nebulaclouds/nebulacookbook:"$example_name"-"$version"
(cd "$dir" && build "$image_uri" && serialize "$example_name" "$image_uri")
echo "$image_uri"
