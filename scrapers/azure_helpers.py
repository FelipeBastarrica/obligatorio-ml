import os

from azure.storage.blob import BlobServiceClient

CONNECT_STR = os.getenv("<STRING_KEY>")
CONTAINER_NAME = os.environ.get("<CONTAINER_NAME>")
#https://cs210032001db9f06eb.blob.core.windows.net

blob_service_client = BlobServiceClient.from_connection_string("<STRING_KEY>")
container_client = blob_service_client.get_container_client(container="<CONTAINER_NAME>")

# Function that uploads the blob using container credentials
def upload_blob(path, buf):
    container_client.upload_blob(name=path, data=buf.getvalue())

# Function that uploads properties file to container
def append_file_to_blob(path):
    with open(path, mode="rb") as data:
        blob_client = container_client.upload_blob(name=path, data=data, blob_type="AppendBlob")
        properties = blob_client.get_blob_properties()

