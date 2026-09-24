FROM python:3.13-slim
WORKDIR /srv
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client \
  && rm -rf /var/lib/apt/lists/*
COPY infra/restore.py infra/restore.py
USER 65532:65532
ENTRYPOINT ["python", "infra/restore.py"]
