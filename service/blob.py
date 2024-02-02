from azure.storage.blob import BlobServiceClient, BlobClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
import io

account_name = "cxpnetworkteststorage"
account_key = "uTEPQVdrJgNFBW4Cx30ZXlAXCyW3rKHPE6LnrMG/G7e/s/UJIadtTiB6PJBNvJ8yD/OxZRmzDxOl+AStHu/rtg=="
container_name = "pdf"

blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)


def save_blob_from_sas(blob_sas_url, destination_file_path):

    # BlobClient를 생성합니다.
    blob_client = BlobClient.from_blob_url(blob_sas_url)

    # Blob에서 데이터를 가져와서 로컬 파일에 쓰기합니다.
    with open(destination_file_path, "wb") as my_blob:
        download_stream = blob_client.download_blob()
        my_blob.write(download_stream.readall())

def getBlobList(container):
    container_client = blob_service_client.get_container_client(container)
    resultList = container_client.list_blobs()
    blobnameList = []
    for result in resultList :
        blobnameList.append(result.name)
    return blobnameList

def upload_file_to_blob(stream, container_name, blob_name):
    # BlobServiceClient를 생성합니다.
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

    # ContainerClient를 생성합니다.
    container_client = blob_service_client.get_container_client(container_name)

    print(blob_name)

    # BlobClient를 생성하여 로컬 파일을 Blob에 업로드합니다.
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(io.BytesIO(stream),overwrite=True)

def generate_blob_sas_url(container_name, blob_name):
    # BlobServiceClient를 생성합니다.
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

    # BlobClient를 생성합니다.
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # SAS 토큰을 생성합니다.
    sas_token = generate_blob_sas(
        blob_client.account_name,
        blob_client.container_name,
        blob_client.blob_name,
        account_key=blob_client.credential.account_key,
        permission=BlobSasPermissions(read=True),  # 필요한 권한을 지정합니다. 여기서는 읽기 권한만 부여됩니다.
        expiry=datetime.utcnow() + timedelta(days=1)  # 만료 시간을 지정합니다. 예제에서는 1시간 후에 만료됩니다.
    )

    # Blob SAS URL을 생성합니다.
    blob_sas_url = f"https://{blob_client.account_name}.blob.core.windows.net/{blob_client.container_name}/{blob_client.blob_name}?{sas_token}"

    return blob_sas_url

def download_blob(container,blob_name):
    container_client = blob_service_client.get_container_client(container)
    blob_client = container_client.get_blob_client(blob_name)
    download_stream = blob_client.download_blob()
    return download_stream
