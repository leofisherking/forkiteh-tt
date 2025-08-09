FROM python:3.13-alpine AS builder

RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.13-alpine

WORKDIR /app

COPY --from=builder /install /usr/local
COPY src ./src
COPY alembic.ini .
COPY alembic ./alembic

COPY start.sh .

EXPOSE 8000

ENV PYTHONPATH=./src

CMD ["./start.sh"]
