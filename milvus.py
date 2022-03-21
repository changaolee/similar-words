class Milvus(object):
    _collection = None
    _collection_name = "word_vector"

    def init_vector(self):
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
