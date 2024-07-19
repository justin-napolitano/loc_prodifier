import argparse
import logging
from google.cloud import bigquery
from gcputils.BigQueryClient import BigQueryClient
from google.api_core.exceptions import GoogleAPIError
import os


def initialize_bq_client(project_id, credentials_path=None):
    return BigQueryClient(project_id, credentials_path=credentials_path)

# Function to check if a table exists
def table_exists(client, dataset_id, table_id):
    try:
        client.get_table(f"{dataset_id}.{table_id}")
        return True
    except bigquery.NotFound:
        return False

def merge(bq_client,dataset_id, staging_table_id, prod_table_id,unique_column ="id"):
    # Initialize BigQuery client
    # bq_client = bigquery.Client()
        # Check if the staging and production tables exist
    if not bq_client.table_exists(dataset_id, staging_table_id):
        logging.error(f"Staging table: {staging_table_id} does not exist")
    elif not bq_client.table_exists(dataset_id, prod_table_id):
        logging.error(f"Production table: {prod_table_id} does not exist")
    else:
        # Define the MERGE statement
        merge_query = f"""
        MERGE `{dataset_id}.{prod_table_id}` T
        USING `{dataset_id}.{staging_table_id}` S
        ON T.{unique_column} = S.{unique_column}
        WHEN NOT MATCHED THEN
        INSERT ROW
        """
    
    query_job = bq_client.query_and_wait(merge_query)
    if query_job.result():
        logging.info(f"Inserted records from {staging_table_id} into {prod_table_id} without duplicates")
    return query_job


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert records from staging table to production table without duplicates.")
    parser.add_argument("--dataset_id", required=True, help="The dataset ID.")
    parser.add_argument("--staging_table_id", required=True, help="The staging table ID.")
    parser.add_argument("--prod_table_id", required=True, help="The production table ID.")
    parser.add_argument('--local', action='store_true', help='Run the script locally with credentials path')

    args = parser.parse_args()

    project_id = os.getenv('GCP_PROJECT_ID', 'smart-axis-421517')
    # logging.info(f"I wonder if the ARg parser is killing it...")
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    credentials_path = None
    if args.local:
        credentials_path = os.getenv('GCP_CREDENTIALS_PATH', 'secret.json')

    bq_client = initialize_bq_client(project_id, credentials_path)

    logging.info(f"Initalized BQClient")


    merge_query_job = merge(bq_client, args.dataset_id, args.staging_table_id, args.prod_table_id)
    logging.info(f"Merge Query Job ID: {merge_query_job.job_id}")
