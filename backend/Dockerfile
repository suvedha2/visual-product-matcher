FROM python:3.9-slim

WORKDIR /app

# Copy all necessary files from the backend folder into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# The command to start the FastAPI server
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]