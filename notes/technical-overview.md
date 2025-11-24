---
slug: github-loc-prodifier-note-technical-overview
id: github-loc-prodifier-note-technical-overview
title: Loc Prodifier
repo: justin-napolitano/loc_prodifier
githubUrl: https://github.com/justin-napolitano/loc_prodifier
generatedAt: '2025-11-24T18:40:47.330Z'
source: github-auto
summary: >-
  Loc Prodifier is a Python tool that merges data from staging tables to
  production tables in Google BigQuery, ensuring no duplicates. It runs locally
  or on Google Cloud Run for scalable processing.
tags: []
seoPrimaryKeyword: ''
seoSecondaryKeywords: []
seoOptimized: false
topicFamily: null
topicFamilyConfidence: null
kind: note
entryLayout: note
showInProjects: false
showInNotes: true
showInWriting: false
showInLogs: false
---

Loc Prodifier is a Python tool that merges data from staging tables to production tables in Google BigQuery, ensuring no duplicates. It runs locally or on Google Cloud Run for scalable processing.

## Key Features

- Merges data without duplicates.
- Supports parallel execution of multiple tables.
- Configurable via command-line arguments.

## Tech Stack

- Python 3.7+
- Google BigQuery
- Google Cloud Run
- Docker

## Getting Started

1. Clone the repo:

   ```sh
   git clone https://github.com/justin-napolitano/loc_prodifier.git
   cd loc_prodifier
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

### Running Locally

Ensure you have your Google Cloud credentials JSON. Then run:

```sh
python loc_prodifier.py --dataset_id your_dataset_id --staging_table_id your_staging_table_id --prod_table_id your_prod_table_id --local
```

### Gotchas

Make sure your Google Cloud project has BigQuery and Cloud Run enabled before you run this!
