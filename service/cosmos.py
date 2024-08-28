from azure.cosmos import CosmosClient
import uuid


# Cosmos DB 계정 연결 문자열
endpoint = "https://dev-ai-krc-cosmos.documents.azure.com:443/"
# key = "M1a3s4WV3i2j5c82hvuz6TXyxgfYkVI3xDS2KT4O2LCdIPTFUUhUznW0nxW754Q5CbzyeLohn4ZkACDbDrrYQg=="

# Cosmos DB 클라이언트 생성

# 데이터베이스 및 컨테이너 정보
database_name = "main"


def getCosmosList(container_name):
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    query = "Select * from c"
    items = list(container.query_items(query, enable_cross_partition_query=True))
    return items

def writeCosmos(container_name,writeData):
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    writeData['pk'] = str(uuid.uuid4())
    writeData['id'] = writeData['pk']
    container = database.get_container_client(container_name)
    container.create_item(body=writeData)
    return "N"
