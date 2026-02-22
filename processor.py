import os
from azure.storage.blob import BlobServiceClient

# This handles the "Enterprise Storage" requirement of your job role
def upload_to_azure(local_file_path, connection_string, container_name):
    try:
        # Connect to Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=os.path.basename(local_file_path))
        
        print(f"Uploading {local_file_path} to Azure...")
        with open(local_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print("✅ Upload Successful!")
    except Exception as e:
        print(f"❌ Azure Error: {e}")
