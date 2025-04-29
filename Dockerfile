FROM python:3.13-alpine

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["streamlit", "run", "main.py"]