from milvus import Milvus, IndexType, MetricType, Status
import redis


class Search(object):
    _HOST = "similar_words_milvus"
    _PORT = "19530"

    _REDIS_HOST = "similar_words_redis"
    _REDIS_PORT = 6379

    _VECTOR_DIM = 200
    _INDEX_FILE_SIZE = 1024
    _COLLECTION_NAME = "word_vector"

    _WORD_TO_ID_KEY = "word_to_id"
    _ID_TO_WORD_KEY = "id_to_word"

    def __init__(self):
        self.milvus = Milvus(host=self._HOST, port=self._PORT)
        self.db = redis.StrictRedis(host=self._REDIS_HOST, port=self._REDIS_PORT)

    def _create_collection(self):
        param = {
            'collection_name': self._COLLECTION_NAME,
            'dimension': self._VECTOR_DIM,
            'index_file_size': self._INDEX_FILE_SIZE,
            'metric_type': MetricType.IP  # 內积类型，计算余弦相似度
        }
        self.milvus.create_collection(param)

    def _create_index(self):
        ivf_param = {'nlist': 1024}
        self.milvus.create_index(self._COLLECTION_NAME, IndexType.IVF_SQ8, ivf_param)

    def _add_ids_words_map(self, ids: list, words: list):
        self.db.hset(self._ID_TO_WORD_KEY, mapping=dict(zip(ids, words)))
        self.db.hset(self._WORD_TO_ID_KEY, mapping=dict(zip(words, ids)))

    def _get_words_vector(self, words: list):
        ids = self.db.hmget(self._WORD_TO_ID_KEY, words)
        if not ids:
            return []
        ids = list(map(int, ids))
        _, vectors = self.milvus.get_entity_by_id(collection_name=self._COLLECTION_NAME, ids=ids)
        return vectors

    def _ids_to_words(self, ids: list):
        return list(map(lambda x: x.decode("utf-8"), self.db.hmget(self._ID_TO_WORD_KEY, ids))) if ids else []

    def _batch_add_vector(self, ids, words, vectors):
        # 添加 id 和单词映射关系
        self._add_ids_words_map(ids, words)

        # 插入词向量
        self.milvus.insert(
            collection_name=self._COLLECTION_NAME,
            records=vectors,
            ids=ids)

    def init_vector(self):
        # collection 存在则删除后创建
        status, ok = self.milvus.has_collection(self._COLLECTION_NAME)
        if ok:
            self.milvus.drop_collection(self._COLLECTION_NAME)
            self.milvus.drop_index(self._COLLECTION_NAME)
            self.milvus.flush()
        self._create_collection()

        # 创建索引
        self._create_index()

        with open("/app/Tencent_AILab_ChineseEmbedding.txt", "r", encoding="utf-8") as f:
            idx, ids, words, vectors = 0, [], [], []
            for line in f:
                word, embedding = line.split(" ", 1)
                embedding = embedding.split()
                if len(embedding) != 200:
                    continue

                ids.append(idx)
                words.append(word)
                vectors.append(list(map(float, embedding)))
                idx += 1

                if len(ids) > 1000:
                    self._batch_add_vector(ids, words, vectors)
                    ids, words, vectors = [], [], []

        if len(ids):
            self._batch_add_vector(ids, words, vectors)

    def query_word(self, word: str, top_k: int):
        [vector] = self._get_words_vector([word])
        if not vector:
            return []
        search_params = {'nprobe': 16}
        _, results = self.milvus.search(
            collection_name=self._COLLECTION_NAME,
            query_records=[vector],
            top_k=top_k,
            params=search_params)
        ids = []
        for raw_result in results:
            for result in raw_result:
                ids.append(int(result.id))
        words = self._ids_to_words(ids)
        return words
