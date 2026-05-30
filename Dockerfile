FROM python:3.11-alpine AS builder


WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel jaraco.context
RUN pip install --no-cache-dir --user -r requirements.txt



FROM python:3.11-alpine


LABEL org.opencontainers.image.authors="Kacper Koźliński"
LABEL org.opencontainers.image.description="Zadanie 1 - Aplikacja Pogodowa"


WORKDIR /app

RUN apk update && apk upgrade --no-cache && \
    pip install --no-cache-dir --upgrade pip setuptools wheel jaraco.context

COPY --from=builder /root/.local /root/.local

COPY main.py .
COPY tlo.jpg .


ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1


EXPOSE 8501


HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8501/ || exit 1


ENTRYPOINT ["python", "main.py"]