FROM python:3.10

WORKDIR /app

# API Params
ENV API_URL="http://localhost:3000"
ENV TOKEN=

COPY . .

# Install OpenCV dependencies
RUN apt update && \
    apt install -y \
        ffmpeg \
        libsm6 \
        libxext6

# Install app dependencies
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD ["python3", "./app/main.py"]