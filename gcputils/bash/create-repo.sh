#!/bin/bash

# Check if both image_repo and region arguments are provided
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <image_repo> <region>"
  exit 1
fi

# Assign the arguments to variables
image_repo=$1
region=$2

# Create the Artifact Registry repository
gcloud artifacts repositories create $image_repo \
    --repository-format=docker \
    --location=$region \
    --description="Docker repository for $image_repo"

# Verify the repository creation
gcloud artifacts repositories list --location=$region
