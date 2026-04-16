from pymilvus import MilvusClient
import json

COLLECTION_NAME = "pipelinev2"
OUTPUT_FILE = "resources/milvus_storage.jsonl"
ORDERED_FIELDS = ["chunk_id", "chunk_hash", "title1", "title2", "text", "upload_time"]

client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")
state = client.get_load_state(collection_name=COLLECTION_NAME)
print("集合加载状态：", state)

client.flush(collection_name=COLLECTION_NAME)

total = client.get_collection_stats(collection_name=COLLECTION_NAME)["row_count"]
print(f"Row Count: {total}")

if total == 0:
    exit()

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    res = client.query(
        collection_name=COLLECTION_NAME,
        # filter=f"",
        output_fields=ORDERED_FIELDS,
        # limit=BATCH_SIZE
        limit=total
    )

    # File write
    for item in res:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

    # print(f"Output: {min(offset + BATCH_SIZE, total)} / {total}")

print(f"\n Output successfully at：{OUTPUT_FILE}")