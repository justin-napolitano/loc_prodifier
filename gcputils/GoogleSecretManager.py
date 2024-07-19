from google.cloud import secretmanager
import os

class GoogleSecretManager:
    def __init__(self, project_id=None):
        """
        Initialize the GoogleSecretManager client.

        Args:
        project_id (str): Google Cloud Project ID. If not provided, it will be read from the environment variable PROJECT_NAME.
        """
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id or os.getenv("PROJECT_NAME")
        if not self.project_id:
            raise ValueError("Project ID must be provided or set in the environment variable PROJECT_NAME")
    
    def access_secret(self, secret_id, version_id='latest'):
        """
        Access the secret version and return the payload.

        Args:
        secret_id (str): The ID of the secret to access.
        version_id (str): The version of the secret to access (default is 'latest').

        Returns:
        str: The secret payload as a string.
        """
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(name=name)
        payload = response.payload.data.decode("UTF-8")
        return payload

# Example usage:
if __name__ == "__main__":
    gsm = GoogleSecretManager()
    mastodon_username = gsm.access_secret("MASTODON_USERNAME")
    mastodon_password = gsm.access_secret("MASTODON_PASSWORD")
    print(f"Username: {mastodon_username}")
    print(f"Password: {mastodon_password}")
