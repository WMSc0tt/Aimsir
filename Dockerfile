#Base files
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the applikation source code into this container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

#entry point for the container
CMD ["python", "aimsir.py"]