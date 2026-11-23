FROM python:3.13-slim

WORKDIR /app

RUN useradd --create-home appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser app/ ./app/

USER appuser

EXPOSE 2222

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2222"]
