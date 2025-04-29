FROM python:3.11-alpine

RUN apk add --no-cache openjdk11 bash curl build-base

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH="$JAVA_HOME/bin:$PATH"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["streamlit", "run", "main.py"]