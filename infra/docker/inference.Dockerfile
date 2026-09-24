FROM python:3.13-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/inference services/inference
COPY ml ml
USER 65532:65532
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--app-dir", "services/inference", "--host", "0.0.0.0", "--port", "8000"]
