---
slug: github-loc-prodifier
title: 'Loc Prodifier: Automating BigQuery Data Merges with Google Cloud'
repo: justin-napolitano/loc_prodifier
githubUrl: https://github.com/justin-napolitano/loc_prodifier
generatedAt: '2025-11-23T09:14:59.421244Z'
source: github-auto
summary: >-
  Technical overview of Loc Prodifier, a Python tool automating staging-to-production merges in
  BigQuery with Google Cloud workflows and CI/CD.
tags:
  - bigquery
  - google-cloud
  - data-ingestion
  - python
  - cloud-run
seoPrimaryKeyword: bigquery data merge
seoSecondaryKeywords:
  - google cloud workflows
  - python data pipeline
  - cloud run deployment
seoOptimized: true
---

# Loc Prodifier: A Technical Overview

## Motivation

Data pipelines frequently require merging incremental or staging data into production datasets without introducing duplicates. In Google BigQuery, this often involves writing custom SQL MERGE statements and managing orchestration for multiple tables. Loc Prodifier addresses this by providing a Python-based solution that merges staging tables into production tables while avoiding duplicate records, supporting both local execution and cloud deployment.

## Problem Statement

Merging data from staging to production tables in BigQuery can be error-prone and repetitive, especially when handling multiple tables in parallel. Manual SQL scripts lack scalability and automation, and integrating with Google Cloud services requires additional tooling. Loc Prodifier aims to automate and standardize this process.

## Implementation Details

### Core Functionality

At its core, the main script (`loc_prodifier.py`) uses a BigQuery client wrapper (`gcputils.BigQueryClient`) to:

- Verify the existence of staging and production tables.
- Execute a MERGE SQL statement that inserts records from the staging table into the production table only when they do not already exist, based on a unique key (defaulting to `id`).

This approach prevents duplicate records during data ingestion.

### Google Cloud Utilities

The project includes a `gcputils` submodule that encapsulates common Google Cloud client functionality:

- `BigQueryClient.py`: Wraps BigQuery client creation, dataset and table management.
- `gcpclient.py`: Handles Google Cloud Storage operations.
- `GoogleCloudLogging.py`: Integrates with Google Cloud Logging for centralized log management.
- `GoogleSecretManager.py`: Provides access to secrets stored in Google Secret Manager.

This modular design promotes reuse and cleaner code.

### Orchestration and Deployment

- **Cloud Workflows**: The `workflow.yaml` defines a workflow that accepts parameters like dataset ID and table lists, then executes HTTP POST calls to trigger the merge operation in parallel across multiple tables. This enables scalable and automated processing.

- **Cloud Build and Cloud Run**: The `cloudbuild.yaml` automates building a Docker image containing the script, pushing it to Google Artifact Registry, and deploying a Cloud Run job. This supports continuous integration and deployment pipelines.

- **Docker**: A `Dockerfile` enables containerization for consistent environment setup, facilitating local testing and cloud deployment.

### Assumptions and Notes

- The unique key for merging defaults to `id` but can be customized.
- The script supports a `--local` flag to differentiate between local and cloud execution contexts.
- Authentication and authorization rely on Google Cloud credentials, either via environment or service account JSON files.
- The workflow uses HTTP calls to invoke the Cloud Run service, requiring appropriate IAM permissions and authentication tokens.

## Practical Considerations

- The modular `gcputils` submodule can be reused across projects, reducing duplication.
- The Cloud Build pipeline is partially commented out for repository creation, suggesting manual setup or customization.
- Logging integration is prepared but could be expanded for better observability.
- The workflow design assumes familiarity with Google Cloud Workflows and Cloud Run.

## Summary

Loc Prodifier is a practical tool for managing BigQuery data merges with a focus on preventing duplicates and enabling scalable, parallel execution. It leverages Google Cloud services and best practices such as containerization, CI/CD pipelines, and modular client utilities. The project serves as a reference implementation for data engineers seeking to automate BigQuery merges in a cloud-native environment.
