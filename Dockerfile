FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev && rm -rf /var/lib/apt/lists/*

# Set up the application
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENV PORT=8080
CMD ["gunicorn", "-b", ":$PORT", "main:app"]
