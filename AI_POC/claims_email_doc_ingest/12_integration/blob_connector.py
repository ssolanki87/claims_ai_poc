from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from typing import List, Dict, Optional, BinaryIO
from datetime import datetime
from pathlib import Path
import json

class BlobConnector:
    """Azure Blob Storage connector for claims data"""
    
    def __init__(self, connection_string: str, logger=None):
        self.connection_string = connection_string
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.logger = logger
    
    def list_emails(self, container_name: str, prefix: str = "") -> List[str]:
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blobs = container_client.list_blobs(name_starts_with=prefix)
            return [blob.name for blob in blobs]
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error listing blobs: {str(e)}")
            raise
    
    def read_email_blob(self, container_name: str, blob_name: str) -> Dict:
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_name
            )
            download_stream = blob_client.download_blob()
            content = download_stream.readall()
            email_data = json.loads(content.decode('utf-8'))
            return email_data
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading blob {blob_name}: {str(e)}")
            raise
    
    def read_attachment(self, container_name: str, blob_name: str) -> bytes:
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_name
            )
            download_stream = blob_client.download_blob()
            return download_stream.readall()
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading attachment {blob_name}: {str(e)}")
            raise
    
    def write_processed_data(self, container_name: str, blob_name: str, data: Dict) -> str:
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_name
            )
            json_data = json.dumps(data, indent=2, default=str)
            blob_client.upload_blob(json_data, overwrite=True)
            if self.logger:
                self.logger.info(f"Written processed data to {blob_name}")
            return blob_client.url
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error writing blob {blob_name}: {str(e)}")
            raise
    
    def move_to_archive(self, source_container: str, dest_container: str, blob_name: str) -> bool:
        try:
            source_blob = self.blob_service_client.get_blob_client(
                container=source_container,
                blob=blob_name
            )
            dest_blob = self.blob_service_client.get_blob_client(
                container=dest_container,
                blob=f"archived_{datetime.now().strftime('%Y%m%d')}_{blob_name}"
            )
            dest_blob.start_copy_from_url(source_blob.url)
            source_blob.delete_blob()
            if self.logger:
                self.logger.info(f"Archived blob {blob_name}")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error archiving blob {blob_name}: {str(e)}")
            return False
