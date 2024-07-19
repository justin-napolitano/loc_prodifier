from google.cloud import storage
import os
import logging
import re

class GCSClient:
    def __init__(self, project_id, credentials_path=None):
        """
        Initializes the Google Cloud Storage client.

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
        Creates and returns the Google Cloud Storage client.

        Returns:
            google.cloud.storage.Client: The initialized Google Cloud Storage client.
        """
        if self.credentials_path:
            print("trying creds file")
            client = storage.Client.from_service_account_json(self.credentials_path)
        else:
            client = storage.Client(project=self.project_id)
        return client

    def list_buckets(self):
        """
        Lists all buckets in the Google Cloud Storage project.

        Returns:
            list: A list of bucket names.
        
        Source: 
            https://cloud.google.com/storage/docs/listing-buckets
        """
        buckets = [bucket.name for bucket in self.client.list_buckets()]
        return buckets
    
    def create_bucket(self, bucket_name):
        """
        Creates a new bucket in the Google Cloud Storage project if it does not already exist.

        Args:
            bucket_name (str): The name of the bucket to create.

        Returns:
            str: The name of the created bucket.

        Source: 
            https://cloud.google.com/storage/docs/creating-buckets
        """
        bucket = self.client.bucket(bucket_name)
        if not bucket.exists():
            bucket.create()
            return f"Bucket '{bucket_name}' created successfully."
        else:
            return f"Bucket '{bucket_name}' already exists."
        
    def put_blob_from_string(self, bucket, source_string, destination_blob_name, overwrite=False):
        print(overwrite)
        """
        Uploads an object to a blob in a Google Cloud Storage bucket.

        Args:
            bucket (str or google.cloud.storage.Bucket): The name of the bucket or an already instantiated bucket object.
            source_string (str): The object to be uploaded.
            destination_blob_name (str): The name to give to the uploaded file in the bucket.
            overwrite (bool, optional): Whether to overwrite an existing blob if it already exists. Default is False.

        Returns:
            str: The URL of the uploaded object.

        Source: https://cloud.google.com/storage/docs/uploading-objects-from-memory
        """
        if isinstance(bucket, str):
            bucket = self.client.bucket(bucket)
        blob = bucket.blob(destination_blob_name)

        # Check if the blob exists and overwrite is False
        if blob.exists() and not overwrite:
            print(f"Blob '{destination_blob_name}' already exists. To overwrite, set overwrite=True.")
            return blob
    

        # Upload the blob
        blob.upload_from_string(source_string)

        print(f"Object uploaded to {destination_blob_name} in bucket {bucket.name}")
        print(blob)
        return blob
    
    def get_blob(self, bucket_name, source_blob_name, destination_file_name):
        """
        Downloads a blob from the specified bucket in Google Cloud Storage.

        Args:
            bucket_name (str): Name of the bucket.
            source_blob_name (str): Name of the blob in the bucket.
            destination_file_name (str): File name to save the blob as locally.
        """
        # Get the bucket
        bucket = self.client.bucket(bucket_name)

        # Get the blob
        blob = bucket.blob(source_blob_name)

        # Download the blob to a file
        blob.download_to_filename(destination_file_name)

        print(f"Blob '{source_blob_name}' downloaded to '{destination_file_name}'.")
        return blob
    
    def list_blobs(self, bucket_name):
        """
        Lists all blobs in the specified bucket in Google Cloud Storage.

        Args:
            bucket_name (str): Name of the bucket.

        Returns:
            list: A list of blob names.
        """
        # Get the bucket
        bucket = self.client.bucket(bucket_name)
        
        # List all blobs in the bucket
        blobs = list(bucket.list_blobs())
        
        blob_names = [blob.name for blob in blobs]
        return blob_names

    def pop_blob(self, bucket_name, patterns_file = None):
        """
        Selects and removes the first blob from the specified bucket in Google Cloud Storage,
        excluding any blobs that match patterns from the provided file.

        Args:
            bucket_name (str): Name of the bucket.
            patterns_file (str, optional): Path to the file containing regex patterns to exclude.

        Returns:
            google.cloud.storage.blob.Blob: The first blob from the bucket that doesn't match any pattern.
        """
        # Load regex patterns from file
        patterns = []
        if patterns_file:
            with open(patterns_file, 'r') as file:
                patterns = [line.strip() for line in file]

        # Get the bucket
        bucket = self.client.bucket(bucket_name)
        
        # List all blobs in the bucket
        blobs = list(bucket.list_blobs())
        
        if not blobs:
            print(f"No blobs found in bucket '{bucket_name}'.")
            return None

        # Filter blobs based on regex patterns
        for blob in blobs:
            if not any(re.search(pattern, blob.name) for pattern in patterns):
                print(f"First valid blob selected: {blob.name}")
                return blob

        print("No valid blobs found after applying regex patterns.")
        return None

    def download_blob_to_memory(self, bucket_name, blob_name):
        """
        Downloads a blob from the specified bucket to memory.

        Args:
            bucket_name (str): Name of the bucket.
            blob_name (str): Name of the blob to download.

        Returns:
            string: The string content of the blob.
        """
        # Get the bucket
        bucket = self.client.bucket(bucket_name)
        
        # Get the blob
        blob = bucket.blob(blob_name)

        # Download the blob to a string
        blob_data = blob.download_as_string()
        
        # Parse the JSON content
        # json_content = json.loads(blob_data)
        
        print(f"Blob '{blob_name}' downloaded to memory.")
        return blob_data
    
    def copy_blob(self, source_bucket_name, source_blob_name, destination_bucket_name, destination_blob_name):
        """
        Copies a blob from one bucket to another.

        Args:
            source_bucket_name (str): Name of the source bucket.
            source_blob_name (str): Name of the source blob.
            destination_bucket_name (str): Name of the destination bucket.
            destination_blob_name (str): Name of the destination blob.

        Returns:
            google.cloud.storage.blob.Blob: The copied blob.
        """
        source_bucket = self.client.bucket(source_bucket_name)
        source_blob = source_bucket.blob(source_blob_name)
        destination_bucket = self.client.bucket(destination_bucket_name)
        blob_copy = source_bucket.copy_blob(source_blob, destination_bucket, destination_blob_name)
        return blob_copy

    def delete_blob(self, bucket_name, blob_name):
        """
        Deletes a blob from the specified bucket.

        Args:
            bucket_name (str): Name of the bucket.
            blob_name (str): Name of the blob to delete.
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()


# Example usage:

def test():
    project_id = os.environ.get("GCP_PROJECT_ID")
    # credentials_path = "path/to/your/credentials.json"  # Optional if using default credentials
    gcs = GCSClient(project_id, credentials_path=None)

    # List buckets
    buckets = gcs.list_buckets()
    print("Buckets:", buckets)

    # List all blobs in a specific bucket
    blob_names = gcs.list_blobs("your-bucket-name")
    print("Blobs in bucket:", blob_names)

    # Pop the first valid blob from a specific bucket, excluding blobs that match patterns in patterns.txt
    first_blob = gcs.blob_pop("your-bucket-name", "patterns.txt")
    if first_blob:
        print(f"First valid blob name: {first_blob.name}")
        
        # Download the JSON content of the first valid blob to memory
        json_content = gcs.download_blob_to_memory("your-bucket-name", first_blob.name)
        print("JSON content of the first valid blob:", json_content)

if __name__ == "__main__":
    test()
