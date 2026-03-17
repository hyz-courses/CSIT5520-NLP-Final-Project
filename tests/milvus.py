"""
Basic testing of functionality of milvus instance.
Please run this script in server.

Run:
/root/venv/backend-venv/bin/python /root/code/CSIT5520-NLP-Final-Project/test.py
"""

import time
import numpy as np
from pymilvus import MilvusClient, DataType

client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")

# DROP TABLE test IF EXISTS test;
client.drop_collection(collection_name="test")

# Schema 创建测试
schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=True)

schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)

schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=5)

schema.add_field(field_name="my_varchar", datatype=DataType.VARCHAR, max_length=512)

index_params = client.prepare_index_params()

index_params.add_index(field_name="my_id", index_type="AUTOINDEX")

index_params.add_index(
    field_name="my_vector", index_type="AUTOINDEX", metric_type="COSINE"
)

client.create_collection(
    collection_name="test", schema=schema, index_params=index_params
)

res = client.get_load_state(collection_name="test")

print(res)
print("Schema创建成功\n")

# 字段插入测试

data = [
    {"my_id": i, "my_vector": np.random.random(5).tolist(), "my_varchar": f"test_{i}"}
    for i in range(15)
]

res = client.insert(
    collection_name="test",
    data=data
)

print(res)
print("字段创建成功!\n")

time.sleep(2)

# 查询测试

res = client.query(
    collection_name="test",
    filter="my_id > 0",
    output_fields=["*"]
)

print(res)
print("查询成功!\n")