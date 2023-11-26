FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

ENV MONGODB_URL = "mongodb://localhost:27017"

CMD ["python3", "/app/main.py"]