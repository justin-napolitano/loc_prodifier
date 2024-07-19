#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 PROJECT_NAME IMAGE_NAME JOB_NAME ENV"
    exit 1
fi

# Assign arguments to variables
PROJECT_NAME=$1
IMAGE_NAME=$2
JOB_NAME=$3
ENV=$4
REGION="us-west2"
SERVICE_ACCOUNT="general-purpose-account@${PROJECT_NAME}.iam.gserviceaccount.com"
DOCKERFILE_PATH="Dockerfile"
REPO_NAME="python-rss-reader"

# Determine the tag based on the environment
if [ "$ENV" == "dev" ]; then
    TAG="dev"
elif [ "$ENV" == "prod" ]; then
    TAG="prod"
else
    echo "Invalid environment. Please use 'dev' or 'prod'."
    exit 1
fi

# Create cloudbuild.yaml
cat <<EOF > cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'us-west2-docker.pkg.dev/$PROJECT_NAME/$REPO_NAME/$IMAGE_NAME:$TAG', '.']

  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'us-west2-docker.pkg.dev/$PROJECT_NAME/$REPO_NAME/$IMAGE_NAME:$TAG']

  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'jobs', 'create', '$JOB_NAME',
           '--image', 'us-west2-docker.pkg.dev/$PROJECT_NAME/$REPO_NAME/$IMAGE_NAME:$TAG',
           '--region', '$REGION']

  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['scheduler', 'jobs', 'create', 'http', '$JOB_NAME-scheduler',
           '--schedule', '0 * * * *',
           '--uri', 'https://$REGION-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$PROJECT_NAME/jobs/$JOB_NAME:run',
           '--http-method', 'POST',
           '--time-zone', 'UTC',
           '--oidc-service-account-email', '$SERVICE_ACCOUNT']

timeout: '1200s'
EOF

# Echo out a summary of the work done
echo "Summary of actions:"
echo "1. Built Docker image: us-west2-docker.pkg.dev/$PROJECT_NAME/$REPO_NAME/$IMAGE_NAME:$TAG"
echo "2. Pushed Docker image to repository: us-west2-docker.pkg.dev/$PROJECT_NAME/$REPO_NAME/$IMAGE_NAME:$TAG"
echo "3. Created Cloud Run job: $JOB_NAME using image us-west2-docker.pkg.dev/$PROJECT_NAME/$REPO_NAME/$IMAGE_NAME:$TAG"
echo "4. Scheduled Cloud Run job: $JOB_NAME-scheduler to run every hour"
echo "5. Cloud Run job region: $REGION"
echo "6. Scheduler job region: $REGION"
