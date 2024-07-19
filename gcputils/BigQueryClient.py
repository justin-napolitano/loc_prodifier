from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import os
import logging
from google.api_core.exceptions import GoogleAPIError

class BigQueryClient:
    def __init__(self, project_id, credentials_path=None):
        """
        Initializes the Google BigQuery client.

        Args:
            project_id (str): The Google Cloud project ID.
            credentials_path (str, optional): Path to the JSON file containing service account credentials.
                                              If not provided, it will use the default credentials from the environment.
        """
        self.project_id = project_id
        self.credentials_path = credentials_path
        self.client = self._create_client()

    def _create_client(self):
        """
        Creates and returns the Google BigQuery client.

        Returns:
            google.cloud.bigquery.Client: The initialized Google BigQuery client.
        """
        if self.credentials_path:
            client = bigquery.Client.from_service_account_json(self.credentials_path, project=self.project_id)
        else:
            client = bigquery.Client(project=self.project_id)
        return client

    def create_dataset(self, dataset_id, location="US"):
        """
        Creates a new dataset in the Google BigQuery project.

        Args:
            dataset_id (str): The dataset ID to create.
            location (str): The location where the dataset will be created.

        Returns:
            google.cloud.bigquery.Dataset: The created dataset.
        """
        dataset_ref = bigquery.DatasetReference(self.project_id, dataset_id)
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location

        dataset = self.client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset {dataset.dataset_id} created.")
        return dataset

    # Function to check if a table exists
    def table_exists(self, dataset_id, table_id):
        try:
            self.client.get_table(f"{dataset_id}.{table_id}")
            return True
        # except Exception as e
        except NotFound :
            # raise e
            return False
        
    def create_table(self, dataset_id, table_id, schema):
        """
        Creates a new table in the specified dataset in Google BigQuery.

        Args:
            dataset_id (str): The dataset ID where the table will be created.
            table_id (str): The table ID to create.
            schema (list): The schema of the table to create.

        Returns:
            google.cloud.bigquery.Table: The created table.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = bigquery.Table(table_ref, schema=schema)

        table = self.client.create_table(table, exists_ok=True)
        print(f"Table {table.table_id} created in dataset {dataset_id}.")
        return table
    
    def wait_for_result(query_job):
        try:
         # print(query_job.done())
            while query_job.done() != True:
                logging.info(f"Waiting for query job {query_job.job_id} to complete")

            if query_job.errors:
                raise GoogleAPIError(query_job.errors)
            
            return query_job
        
        except GoogleAPIError as e:
            logging.error(f"An error occurred: {e}")    
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")


    def query(self, query):
        """
        Executes a query in Google BigQuery.

        Args:
            query (str): The SQL query to execute.

        Returns:
            google.cloud.bigquery.job.QueryJob: The query job.
        """
        query_job = self.client.query(query)
        # return query_job
        results = query_job.result()
        for row in results:
            print(row)
        return results

    def query_and_wait(self,query):

        
        try:
            query_job = self.client.query(query)
         # print(query_job.done())
            while query_job.done() != True:
                logging.info(f"Waiting for query job {query_job.job_id} to complete")

            if query_job.errors:
                raise GoogleAPIError(query_job.errors)
            
            return query_job
        
        except GoogleAPIError as e:
            logging.error(f"An error occurred: {e}")    
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        

    def load_data_from_json(self, dataset_id, table_id, json_data, schema):
        """
        Loads data from a JSON object into a BigQuery table.

        Args:
            dataset_id (str): The dataset ID where the table exists.
            table_id (str): The table ID where data will be loaded.
            json_data (list): The JSON data to load into the table.
            schema (list): The schema of the table.

        Returns:
            google.cloud.bigquery.job.LoadJob: The load job.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.schema = schema
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON

        load_job = self.client.load_table_from_json(json_data, table_ref, job_config=job_config)
        load_job.result()
        print(f"Loaded {load_job.output_rows} rows into {dataset_id}:{table_id}.")
        return load_job
    
    def load_dataframe_to_table(self, dataset_id, table_id, dataframe):
        """
        Loads a Pandas DataFrame to a BigQuery table.

        Args:
            dataset_id (str): The dataset ID where the table exists.
            table_id (str): The table ID where data will be loaded.
            dataframe (pd.DataFrame): The DataFrame to load into the table.

        Returns:
            google.cloud.bigquery.job.LoadJob: The load job.
        """
        table_ref = self.client.dataset(dataset_id).table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

        load_job = self.client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
        load_job.result()
        print(f"Loaded {load_job.output_rows} rows into {dataset_id}:{table_id}.")
        return load_job

# Example usage:

def test():
    project_id = os.environ.get("GCP_PROJECT_ID")
    # credentials_path = "path/to/your/credentials.json"  # Optional if using default credentials
    bq = BigQueryClient(project_id, credentials_path=None)

    # Create a dataset
    dataset_id = "my_dataset"
    bq.create_dataset(dataset_id)

    # Create a table
    table_id = "my_table"
    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("age", "INTEGER"),
    ]
    bq.create_table(dataset_id, table_id, schema)

    # Query data
    query = f"""
    SELECT *
    FROM `{project_id}.{dataset_id}.{table_id}`
    """
    bq.query(query)

    # Load data from JSON
    json_data = [
        {"name": "John Doe", "age": 30},
        {"name": "Jane Smith", "age": 25},
    ]
    bq.load_data_from_json(dataset_id, table_id, json_data, schema)

if __name__ == "__main__":
    test()
