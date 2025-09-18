FROM python:3.13.7-alpine3.22

# Install system build dependencies + Cython
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    gcc \
    python3-dev \
    py3-pip \
    libxml2-dev \
    libxslt-dev \
    openssl-dev \
    cython

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD [ "python", "app.py" ]