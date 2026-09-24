FROM python:3.13-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY workers/training workers/training
COPY ml ml
USER 65532:65532
ENTRYPOINT ["python", "-m", "workers.training.runner"]
