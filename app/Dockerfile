FROM python:3.8-slim

RUN apt-get update && apt-get install -y tini && apt-get clean

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev build-essential

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["/usr/bin/tini", "--"]  

CMD ["python", "app.py"]