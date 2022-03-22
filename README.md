> 基于腾讯中文词向量和 [Milvus](https://milvus.io/cn/docs) 的相似词搜索服务。

## 数据下载

[腾讯中文预训练词向量](https://pan.baidu.com/s/1Xud2TTo861hkdvjleDXslg?pwd=qnft)

## 服务部署

### 1. 创建 Docker 网络

```
$ sudo docker network create -d bridge milvus
```

### 2. 启动 Milvus Docker 容器

拉取 CPU 版本的 Milvus 镜像

```
$ sudo docker pull milvusdb/milvus:1.1.1-cpu-d061621-330cc6
```

启动 Docker 容器，将本地的文件路径映射到容器中：

```
$ sudo docker run -d --name milvus_cpu_1.1.1 \
    -p 19530:19530 \
    -p 19121:19121 \
    -v (pwd)/similar_words/milvus/db:/var/lib/milvus/db \
    -v (pwd)/similar_words/milvus/conf:/var/lib/milvus/conf \
    -v (pwd)/similar_words/milvus/logs:/var/lib/milvus/logs \
    -v (pwd)/similar_words/milvus/wal:/var/lib/milvus/wal \
    --network milvus \
    --name milvus_cpu_1.1.1 \
    milvusdb/milvus:1.1.1-cpu-d061621-330cc6
```

确认 Milvus 运行状态：

```
$ sudo docker ps
```

如果 Milvus 服务没有正常启动，执行以下命令查询错误日志：

```
$ sudo docker logs milvus_cpu_1.1.1
```

### 2. 启动 Redis Docker 容器

```
$ sudo docker pull redis:latest
$ sudo [docker run -d \
  -p 16379:6379 \
  --network milvus \
  --name similar_words_redis \
  redis:latest]()
```

### 3. 启动相似词搜索服务

```
$ docker build -t similar_words:latest .
$ docker run -d \
  -p 5000:5000 \
  -v (pwd)/similar_words:/app \
  -v (pwd)/Tencent_AILab_ChineseEmbedding.txt:/app/Tencent_AILab_ChineseEmbedding.txt \
  --network milvus \
  --name similar_words \
  similar_words:latest
```

### 3. 导入腾讯中文词向量

```
$ curl 127.0.0.1:5000/init
```

### 4. 相似词搜索

```

```