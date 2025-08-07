FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p app/uploads

EXPOSE 5000

# default environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_NAME=evaluation_system
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres123

COPY init_db_docker.py .

CMD ["sh", "-c", "python init_db_docker.py && python run.py"]
