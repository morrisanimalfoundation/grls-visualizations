#!/usr/bin/env bash

# Should provide the directory where this script lives in most cases.
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# The name of our image from the Gitlab Container Registry.
IMAGE_NAME="registry.gitlab.com/morrisanimalfoundation/dsg/data-commons-visualizations"

# Build the image with our special build args.
# These matter more on Jenkins, but need to be placeheld anyway.
docker image build -t $IMAGE_NAME --build-arg USER_ID=$(id -u ${USER}) .

# Run the container in a disposable manner.
# Add a volume to the current working dir.
# Swap commands depending on operating system.
if ! command -v winpty &> /dev/null
then
  docker run --rm -it -v $SCRIPT_DIR:/workspace $IMAGE_NAME bash
else
  winpty docker run --rm -it -v $SCRIPT_DIR:/workspace $IMAGE_NAME bash
fi