FROM python:3.9.2
COPY . /app
WORKDIR /app
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
CMD ["flask", "run"]