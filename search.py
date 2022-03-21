from milvus import Milvus, IndexType, MetricType, Status


class Search(object):
    _HOST = "milvus_cpu_1.1.1"
    _PORT = "19530"

    _VECTOR_DIM = 200
    _INDEX_FILE_SIZE = 1024
    _COLLECTION_NAME = "word_vector"

    def __init__(self):
        self.milvus = Milvus(host=self._HOST, port=self._PORT)

    def _create_collection(self):
        param = {
            'collection_name': self._COLLECTION_NAME,
            'dimension': self._VECTOR_DIM,
            'index_file_size': self._INDEX_FILE_SIZE,
            'metric_type': MetricType.IP  # 內积类型，计算余弦相似度
        }
        self.milvus.create_collection(param)

    def init_vector(self):
        # collection 存在则删除后创建
        status, ok = self.milvus.has_collection(self._COLLECTION_NAME)
        if ok:
            self.milvus.drop_collection(self._COLLECTION_NAME)
            self.milvus.drop_index(self._COLLECTION_NAME)
            self.milvus.flush()
        self._create_collection()

        with open("./Tencent_AILab_ChineseEmbedding.txt", "r", encoding="utf-8") as f:
            for line in f:
                word, embedding = line.split(" ", 1)
                embedding = embedding.split()
                if len(embedding) != 200:
                    continue
                print(word, embedding)
                break

    def query_vector(self):
        pass
