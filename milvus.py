from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)


class Milvus(object):
    _collection_name = "word_vector"

    def __init__(self):
        connections.connect("default", host="localhost", port="19530")

    def init_vector(self):
        if utility.has_collection(self._collection_name):
            utility.drop_collection(self._collection_name)
        fields = [
            FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=False),
            FieldSchema(name="word", dtype=DataType.STRING),
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=200)
        ]

    def query_vector(self):
        pass
