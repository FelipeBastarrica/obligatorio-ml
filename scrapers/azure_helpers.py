import os

from azure.storage.blob import BlobServiceClient

CONNECT_STR = os.getenv("DefaultEndpointsProtocol=https;AccountName=cs210032001db9f06eb;AccountKey=Q7i41vK6zB2p/aKXulAdSROpoIou5uYj+EulJri7p9VI9VH4Us+Rlj+9fo5GC78TxSlPNQEWaDVY+AStDBpAfA==;EndpointSuffix=core.windows.net")
CONTAINER_NAME = os.environ.get("cs210032001db9f06eb")
#https://cs210032001db9f06eb.blob.core.windows.net

blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=cs210032001db9f06eb;AccountKey=Q7i41vK6zB2p/aKXulAdSROpoIou5uYj+EulJri7p9VI9VH4Us+Rlj+9fo5GC78TxSlPNQEWaDVY+AStDBpAfA==;EndpointSuffix=core.windows.net")
container_client = blob_service_client.get_container_client(container="container-ml")

# Function that uploads the blob using container credentials
def upload_blob(path, buf):
    container_client.upload_blob(name=path, data=buf.getvalue())

# Function that uploads properties file to container
def append_file_to_blob(path):
    with open(path, mode="rb") as data:
        blob_client = container_client.upload_blob(name=path, data=data, blob_type="AppendBlob")
        properties = blob_client.get_blob_properties()

