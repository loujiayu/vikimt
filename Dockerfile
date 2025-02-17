FROM gcr.io/google-appengine/python

# Install system dependencies
RUN apt-get update && apt-get install -y libodbc2 unixodbc && rm -rf /var/lib/apt/lists/*

# Set up the application
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", ":$PORT", "main:app"]
