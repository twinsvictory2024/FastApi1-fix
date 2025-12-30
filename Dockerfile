FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev --no-install-recommends

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]