FROM python:3.9.2
COPY . /app
WORKDIR /app
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt
CMD ["flask", "run"]