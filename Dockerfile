FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m src.database.init_database

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "src.app:app", "run", "--host", "0.0.0.0"]
