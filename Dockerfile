FROM python:3.9.2
WORKDIR /app
COPY ./requirements.txt .
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN pip install -r requirements.txt
CMD ["flask", "run"]