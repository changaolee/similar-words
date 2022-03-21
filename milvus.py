from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)


class Milvus(object):
    _collection = None
    _collection_name = "word_vector"

    def __init__(self):
        connections.connect("default", host="localhost", port="19530")
        self._load_collection()

    def _load_collection(self):
        if not utility.has_collection(self._collection_name):
            fields = [
                FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False),
                FieldSchema(name="word", dtype=DataType.STRING),
                FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=200)
            ]
            schema = CollectionSchema(fields, "Tencent AILab ChineseEmbedding.")

            # 创建 collection
            collection = Collection(self._collection_name, schema)

            # 创建索引
            index_params = {
                "metric_type": "IP",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 1024}
            }
            collection.create_index("embeddings", index_params)

        # 加载 collection
        self._collection = Collection(self._collection_name)
        self._collection.load()

    def init_vector(self):
        if utility.has_collection(self._collection_name):
            utility.drop_collection(self._collection_name)
            self._load_collection()
        with open("./Tencent_AILab_ChineseEmbedding.txt", "w", encoding="utf-8") as f:
            for line in f:
                word, embedding = line.split(" ", 1)
                embedding = embedding.split()
                print(word, embedding)
                break

    def query_vector(self):
        pass
