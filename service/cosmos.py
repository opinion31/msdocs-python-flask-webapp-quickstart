from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import uuid

credential = DefaultAzureCredential()

# Cosmos DB 계정 연결 문자열
endpoint = "https://networktestcosmos.documents.azure.com:443/"
key = "YIVMHcMc8TpTE1N9AWtPrAorviKHIcYmG3eFBBSOK8aNKcCn6TQ8fQXFAj5G564GavN06H1yH0u4ACDbjB7nKg=="
key_vault_url = "https://artiekeyvault.vault.azure.net/"


# Cosmos DB 클라이언트 생성

# DefaultAzureCredential을 사용하여 인증

# SecretClient 초기화
client = SecretClient(vault_url=key_vault_url, credential=credential)

# 비밀 가져오기
secret_name = "cosmosendpoint"
cosmos_key = client.get_secret(secret_name)

# 비밀 출력
print(f"Retrieved secret value: {retrieved_secret.value}")


# 데이터베이스 및 컨테이너 정보
database_name = "main"


def getCosmosList(container_name):
    client = CosmosClient(endpoint, cosmos_key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    query = "Select * from c"
    items = list(container.query_items(query, enable_cross_partition_query=True))
    return items

def writeCosmos(container_name,writeData):
    client = CosmosClient(endpoint, cosmos_key)
    database = client.get_database_client(database_name)
    writeData['pk'] = str(uuid.uuid4())
    writeData['id'] = writeData['pk']
    container = database.get_container_client(container_name)
    container.create_item(body=writeData)
    return "N"
