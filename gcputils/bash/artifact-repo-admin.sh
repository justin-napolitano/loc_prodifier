# Get the project number using the project name
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_NAME --format='get(projectNumber)')

# Grant the Artifact Registry Repository Admin role to the Cloud Build service account
gcloud projects add-iam-policy-binding $PROJECT_NAME \
    --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/artifactregistry.repoAdmin"

# Verify permissions
gcloud projects get-iam-policy $PROJECT_NAME