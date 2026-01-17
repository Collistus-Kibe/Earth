# 1. Use Official Python Base Image
FROM python:3.11-slim

# 2. Set Working Directory
WORKDIR /app

# 3. Copy Requirements first (for caching speed)
COPY requirements.txt .

# 4. Install Dependencies
# We install 'gunicorn' for production stability
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# 5. Copy the rest of the app code
COPY . .

# 6. Expose the Port
EXPOSE 8080

# 7. The Command to Run the App
# We use Gunicorn (Production) -> Uvicorn (Worker)
CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]