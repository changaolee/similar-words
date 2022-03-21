> 基于腾讯中文词向量和 [Milvus](https://milvus.io/cn/docs) 的相似词搜索服务。

## 数据下载

[腾讯中文预训练词向量](https://pan.baidu.com/s/1Xud2TTo861hkdvjleDXslg?pwd=qnft)

## 服务部署

### 1. 启动 Milvus 单机版

```
$ sudo docker-compose up -d
```

```
Creating milvus-etcd  ... done
Creating milvus-minio ... done
Creating milvus-standalone ... done
```

如果 Milvus 单机版启动正常，可以看到有 3 个 Docker 容器在运行（2 个为基础服务，1 个为 Milvus 服务）：

```
$ sudo docker-compose ps
```

```
      Name                     Command                  State                          Ports
----------------------------------------------------------------------------------------------------------------
milvus-etcd         etcd -advertise-client-url ...   Up             2379/tcp, 2380/tcp
milvus-minio        /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp
milvus-standalone   /tini -- milvus run standalone   Up             0.0.0.0:19530->19530/tcp,:::19530->19530/tcp
```

### 2. 启动相似词搜索服务

```
$ docker build -t similar_words:latest .
$ docker run -d -p 5000:5000 -v ./:/app/ --name similar_words similar_words:latest
```

### 3. 导入腾讯中文词向量

```
$ curl 127.0.0.1:5000/init
```

### 4. 相似词搜索

```

```