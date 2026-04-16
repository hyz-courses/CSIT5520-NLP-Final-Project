from pymilvus import DataType, MilvusClient
from proj.context import get_project_context


root, env = get_project_context()

client = MilvusClient(uri=env.MILVUS_URI, token=env.MILVUS_TOKEN)

# Check if collection exists
if client.has_collection(collection_name=env.MILVUS_COLLECTION):
    print(f"Collection '{env.MILVUS_COLLECTION}' exists, dropping...")
    client.drop_collection(collection_name=env.MILVUS_COLLECTION)
else:
    print(f"Collection '{env.MILVUS_COLLECTION}' does not exist, creating new one...")

# Create Schema
schema = MilvusClient.create_schema(enable_dynamic_field=True)
schema.add_field(field_name="chunk_id", datatype=DataType.INT64, auto_id=True, is_primary=True)
schema.add_field(
    field_name="original_filename", datatype=DataType.VARCHAR, max_length=1024
)
schema.add_field(field_name="title1", datatype=DataType.VARCHAR, max_length=1024)
schema.add_field(field_name="title2", datatype=DataType.VARCHAR, max_length=1024, nullable=True)
schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
schema.add_field(field_name="upload_time", datatype=DataType.TIMESTAMPTZ)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
schema.add_field(field_name="chunk_hash", datatype=DataType.VARCHAR, max_length=64)

# Config Index
index_params = client.prepare_index_params()
index_params.add_index(field_name="original_filename", index_type="AUTOINDEX")
index_params.add_index(field_name="title1", index_type="AUTOINDEX")
index_params.add_index(field_name="title2", index_type="AUTOINDEX")
index_params.add_index(field_name="text", index_type="AUTOINDEX")
index_params.add_index(field_name="upload_time", index_type="AUTOINDEX")
index_params.add_index(
    field_name="vector", index_type="AUTOINDEX", metric_type="COSINE"
)

# Collection Creation
client.create_collection(
    collection_name=env.MILVUS_COLLECTION, schema=schema, index_params=index_params
)

client.load_collection(collection_name=env.MILVUS_COLLECTION)

res = client.get_load_state(collection_name=env.MILVUS_COLLECTION)

print(res)
print("Milvus collection created and loaded successfully!")
