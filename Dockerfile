FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 3020

CMD ["gunicorn", "-b", "0.0.0.0:3020", "app:app"]