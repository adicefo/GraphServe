# Use official Python image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies directly
RUN pip install --no-cache-dir fastapi uvicorn[standard] neo4j neomodel pydantic[email] passlib py-automapper


COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
