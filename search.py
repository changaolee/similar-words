from milvus import Milvus, IndexType, MetricType, Status
import redis


class Search(object):
    _HOST = "milvus_cpu_1.1.1"
    _PORT = "19530"

    _VECTOR_DIM = 200
    _INDEX_FILE_SIZE = 1024
    _COLLECTION_NAME = "word_vector"

    _WORD_TO_ID_KEY = "word_to_id"
    _ID_TO_WORD_KEY = "id_to_word"

    def __init__(self):
        self.milvus = Milvus(host=self._HOST, port=self._PORT)
        self.db = redis.StrictRedis(host="localhost", port=6379)

    def _create_collection(self):
        param = {
            'collection_name': self._COLLECTION_NAME,
            'dimension': self._VECTOR_DIM,
            'index_file_size': self._INDEX_FILE_SIZE,
            'metric_type': MetricType.IP  # 內积类型，计算余弦相似度
        }
        self.milvus.create_collection(param)

    def _create_index(self):
        ivf_param = {'nlist': 16384}
        self.milvus.create_index(self._COLLECTION_NAME, IndexType.IVF_FLAT, ivf_param)

    def _add_idx_word_map(self, idx: int, word: str):
        self.db.hset(self._ID_TO_WORD_KEY, idx, word)
        self.db.hset(self._WORD_TO_ID_KEY, word, idx)

    def init_vector(self):
        # collection 存在则删除后创建
        status, ok = self.milvus.has_collection(self._COLLECTION_NAME)
        if ok:
            self.milvus.drop_collection(self._COLLECTION_NAME)
            self.milvus.drop_index(self._COLLECTION_NAME)
            self.milvus.flush()
        self._create_collection()

        with open("/app/Tencent_AILab_ChineseEmbedding.txt", "r", encoding="utf-8") as f:
            idx = 0
            for line in f:
                word, embedding = line.split(" ", 1)
                embedding = embedding.split()
                if len(embedding) != 200:
                    continue

                # 添加 id 和单词映射关系
                self._add_idx_word_map(idx, word)

                # 插入词向量
                self.milvus.insert(collection_name=self._COLLECTION_NAME, records=[embedding], ids=[idx])

                idx += 1

                # todo: test
                if idx > 100:
                    break

        # 导入后创建索引
        self._create_index()

    def query_vector(self):
        pass
