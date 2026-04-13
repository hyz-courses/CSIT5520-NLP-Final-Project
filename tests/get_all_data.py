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
    for offset in range(0, total, BATCH_SIZE):
        res = client.query(
            collection_name=COLLECTION_NAME,
            filter=f"id >= {offset}",
            output_fields=ORDERED_FIELDS,
            limit=BATCH_SIZE
        )

        # File write
        for item in res:
            ordered_item = dict([(field, item[field]) for field in ORDERED_FIELDS])
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

        print(f"Output: {min(offset + BATCH_SIZE, total)} / {total}")

print(f"\n Output successfully at：{OUTPUT_FILE}")