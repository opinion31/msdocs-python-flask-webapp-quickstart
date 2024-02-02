from azure.cosmos import CosmosClient
import uuid


# Cosmos DB 계정 연결 문자열
endpoint = "https://networktestcosmos.documents.azure.com:443/"
key = "YIVMHcMc8TpTE1N9AWtPrAorviKHIcYmG3eFBBSOK8aNKcCn6TQ8fQXFAj5G564GavN06H1yH0u4ACDbjB7nKg=="

# Cosmos DB 클라이언트 생성
client = CosmosClient(endpoint, key)

# 데이터베이스 및 컨테이너 정보
database_name = "main"

database = client.get_database_client(database_name)

def getCosmosList(container_name):
    container = database.get_container_client(container_name)
    query = "Select * from c"
    items = list(container.query_items(query, enable_cross_partition_query=True))
    return items

def writeCosmos(container_name,writeData):
    writeData['pk'] = str(uuid.uuid4())
    writeData['id'] = writeData['pk']
    container = database.get_container_client(container_name)
    container.create_item(body=writeData)
    return "N"
