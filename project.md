---
slug: github-loc-prodifier
id: github-loc-prodifier
title: 'Loc Prodifier: Merging Data in Google BigQuery'
repo: justin-napolitano/loc_prodifier
githubUrl: https://github.com/justin-napolitano/loc_prodifier
generatedAt: '2025-11-24T21:35:30.714Z'
source: github-auto
summary: >-
  A Python tool for merging staging data into BigQuery production tables while avoiding duplicates,
  with support for local and Cloud Run execution.
tags:
  - python
  - google bigquery
  - google cloud run
  - docker
  - data merging
  - cloud workflows
seoPrimaryKeyword: google bigquery data merging
seoSecondaryKeywords:
  - python bigquery tool
  - cloud run deployment
  - docker for bigquery
  - data processing workflows
  - parallel data execution
seoOptimized: true
topicFamily: datascience
topicFamilyConfidence: 0.9
kind: project
entryLayout: project
showInProjects: true
showInNotes: false
showInWriting: false
showInLogs: false
---

## Overview

Loc Prodifier is a Python tool designed to merge data from staging tables into production tables within Google BigQuery while preventing duplicate records. It supports both local execution and deployment on Google Cloud Run, enabling scalable and parallel processing of multiple tables using Google Cloud Workflows.

## Features

- Merges data from staging tables into production tables without duplicates.
- Supports parallel execution across multiple tables.
- Can run locally with custom credentials or be deployed on Google Cloud Run.
- Configurable via command-line arguments.

## Tech Stack

- Python 3.7+
- Google Cloud BigQuery
- Google Cloud Run
- Google Cloud Workflows
- Docker

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Google Cloud SDK
- Docker
- Google Cloud project with BigQuery, Cloud Run, and Artifact Registry enabled

### Installation

1. Clone the repository:

```sh
git clone https://github.com/justin-napolitano/loc_prodifier.git
cd loc_prodifier
```

2. Install required Python packages:

```sh
pip install -r requirements.txt
```

### Running Locally

Ensure you have your Google Cloud credentials JSON file. Run:

```sh
python loc_prodifier.py --dataset_id your_dataset_id --staging_table_id your_staging_table_id --prod_table_id your_prod_table_id --local
```

### Running with Docker

1. Build the Docker image:

```sh
docker build -t my-bigquery-script .
```

2. Run the container:

```sh
docker run --rm my-bigquery-script --dataset_id your_dataset_id --staging_table_id your_staging_table_id --prod_table_id your_prod_table_id --local
```

### Deploying to Google Cloud Run

1. Use the provided `cloudbuild.yaml` to build and push the Docker image to Artifact Registry.
2. Deploy the Cloud Run job using the Cloud Build steps or manually with gcloud commands.
3. Use `workflow.yaml` to orchestrate parallel merges via Google Cloud Workflows.

## Project Structure

```
loc_prodifier/
├── cloudbuild.yaml        # Cloud Build configuration for building and deploying
├── Dockerfile             # Docker image build instructions
├── gcputils/              # Google Cloud utility submodule (BigQuery, Storage, Logging, Secrets)
│   ├── BigQueryClient.py  # BigQuery client wrapper
│   ├── gcpclient.py       # Google Cloud Storage client
│   ├── GoogleCloudLogging.py # Cloud Logging client
│   ├── GoogleSecretManager.py # Secret Manager client
│   └── ...
├── loc_prodifier.py       # Main script for merging tables
├── readme-prodifier.md    # Original README content
├── requirements.txt       # Python dependencies
└── workflow.yaml          # Cloud Workflows definition for parallel execution
```

## Future Work / Roadmap

- Add support for configurable merge conditions and update clauses.
- Enhance error handling and logging integration.
- Provide more detailed usage examples and automated tests.
- Expand support for additional data sources or cloud providers.
- Implement monitoring and alerting for workflow executions.

---

*Note: Some documentation and features are inferred based on available code and files.*

