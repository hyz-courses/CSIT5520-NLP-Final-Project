from pymilvus import MilvusClient
import json

COLLECTION_NAME = "pipeline"
OUTPUT_FILE = "resources/milvus_storage.jsonl"
ORDERED_FIELDS = ["id", "title1", "title2", "text", "upload_time"]
BATCH_SIZE = 10

client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")

total = client.get_collection_stats(collection_name=COLLECTION_NAME)["row_count"]
print(f"Row Count: {total}")

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