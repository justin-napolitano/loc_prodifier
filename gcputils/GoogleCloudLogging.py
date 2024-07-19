from google.cloud import logging as cloud_logging
import os
import logging

class GoogleCloudLogging:
    def __init__(self, project_id, credentials_path=None):
        """
        Initializes the Google Cloud Logging client.

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
        Creates and returns the Google Cloud Logging client.

        Returns:
            google.cloud.logging.Client: The initialized Google Cloud Logging client.
        """
        if self.credentials_path:
            client = cloud_logging.Client.from_service_account_json(self.credentials_path, project=self.project_id)
        else:
            client = cloud_logging.Client(project=self.project_id)
        return client

    def setup_logging(self):
        """
        Sets up logging to integrate with Google Cloud Logging.
        """
        handler = self.client.get_default_handler()
        cloud_logger = logging.getLogger()
        cloud_logger.setLevel(logging.INFO)
        cloud_logger.addHandler(handler)

    def log_text(self, message, severity='INFO'):
        """
        Logs a message to Google Cloud Logging.

        Args:
            message (str): The message to log.
            severity (str, optional): The severity level of the log. Default is 'INFO'.
        """
        logger = self.client.logger('default_logger')
        logger.log_text(message, severity=severity)
        print(f"Logged: {message} with severity {severity}")

# Example usage:

def test():
    project_id = os.environ.get("GCP_PROJECT_ID")
    # credentials_path = "path/to/your/credentials.json"  # Optional if using default credentials
    gcl = GoogleCloudLogging(project_id, credentials_path=None)

    # Setup logging
    gcl.setup_logging()

    # Log a message
    gcl.log_text("This is a test log message.")

if __name__ == "__main__":
    test()