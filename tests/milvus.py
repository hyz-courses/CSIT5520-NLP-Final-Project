"""
Basic testing of functionality of milvus instance.
Please run this script in server.

Run:
/root/venv/backend-venv/bin/python /root/code/CSIT5520-NLP-Final-Project/test.py
"""
import os
import time
from typing import List
import numpy as np
from pymilvus import MilvusClient, DataType
from core.embed import embed_text
from proj.context import get_project_context
from core.obj.dao import TextEmbeddingList

client = MilvusClient(uri="http://localhost:19530", token="root:Milvus")

def insert_test(text_embs: TextEmbeddingList):
    if client is None:
        print("Error: Milvus client not connected. Please start Milvus server.")
        return None

    insert_data = [
        {
            "my_id": i, 
            "my_vector": emb, 
            "my_varchar": text
        } 
        for i, (text, emb) in enumerate(text_embs)
    ]
    res = client.insert(collection_name="test", data=insert_data)

    print("字段创建成功!\n")

    return res

if __name__ == "__main__":
    import asyncio

    # DROP TABLE test IF EXISTS test;

    client.drop_collection(collection_name="test")

    # Schema 创建测试
    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=True)

    schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)

    schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=1024)

    schema.add_field(field_name="my_varchar", datatype=DataType.VARCHAR, max_length=65535)

    # DataType.TIMESTAMPTZ

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

    large_text = """
如果以电子形式寄送，则让学校通过加密方式把成绩单发送到pgdoc@ust.hk。注意，这里的加密方式指的是诸如港科大的区块链加密成绩单之类的加密方法，不是简单地发邮件附件。如果你的学校不知道什么叫加密方式，反过来询问你的话，可能是不具备这种方法，那么就需要使用实体寄送的形式。（注：其实这里说到底还是一个信任问题，往年也有同学所在的学校无法提供实体寄送，电子的也只能发邮件，在让科大相信这是学校官方的教务处邮箱以后，科大还是接受了发邮件附件的形式。总之发邮件不是一个首选，其他方法均不可行的话也可以试着与科大研究生院沟通、抄送原所在学校的教务机构，让学校与学校沟通确认。）
    """ * 50

    chunks = [
        large_text,

        "作为非香港永久性居民，来香港上学需要办理学生签证。在以前，学生签证是一张粉色的硬纸片，因此俗称「粉签」。从2021年12月28日起，香港开始实施「电子签证」安排，学生签证也以电子签证的形式发出。建议大家在交流时直接称学生签证为「学生签证」而不是「电子签证」以避免歧义，因为包括IANG签证在内的许多签证目前都是电子签证形式。",
        
        "科大常见的租房地点离科大最近的是大埔仔村，分为上村和下村，步行到学校5~10分钟，是热爱学术的同学的不二之选。如果还是想住得离商场、闹市近一些，那么可以选择坑口、将军澳、宝琳地铁站附近。比如坑口地铁站、将军澳地铁站、宝琳地铁站上盖有许多小区，从这些地铁站乘坐小巴大巴即可到达科大。以上这些是大部分科大同学选择的租房地点，我们建立的各片区居住群也是根据这些地方来的。",

        "把申请材料全部放在一个信封里，信封外面贴上Cover Letter，然后整体放在顺丰包裹里，寄到科大。把申请材料和Cover letter全部放在一个信封里，Cover letter放在最上面，然后整体放在顺丰包裹里，寄到科大。把申请材料和Cover letter全部放在一起，Cover letter放在最上面，然后整体放在顺丰包裹里，寄到科大。科大的官方位置、行政位置是「香港九龙清水湾」，但实际位置、地理位置是「香港新界西贡清水湾」。",

        "香港租房的渠道首先介绍香港本地的四大地产代理公司，分别是：中原地产、美联物业、立嘉阁和香港置业。这四大地产代理商都有自己的官方网站和APP，网站里房源信息也有清晰的描述；如果你身在香港，也可以上这些网站找一下分行地址，亲身前去。这四大地产代理公司旗下都是持牌照的专业中介，只要你把需求报给中介，就能给你找到可供选择的房源，随后你可以通过中介约亲身看房、与房东签约等等。一般来说，如果通过中介成功找到房源，租客与房东各需要付半个月的房租作为佣金。中原地产：https://hk.centanet.com/info/index"
    ]


    text_embedding_list = asyncio.run(embed_text(chunks))

    time.sleep(2)

    insert_test(text_embedding_list)

    res = client.query(
        collection_name="test",
        # filter="my_id > 0",
        output_fields=["my_varchar"],
        limit=5
    )

    # print(res)

    print("插入数据成功")

    query = "Which house renting agency should I pick?"

    query_emb = asyncio.run(embed_text([query]))

    search_res = client.search(
        collection_name="test",
        data=[query_emb.embeddings[0]],
        output_fields=["my_varchar"],
        limit=2
    )

    print(search_res)



    

# print("字段创建成功!\n")

# time.sleep(2)

# # 查询测试

# res = client.query(
#     collection_name="test",
#     filter="my_id > 0",
#     output_fields=["*"]
# )

# print(res)
# print("查询成功!\n")