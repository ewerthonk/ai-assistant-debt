# Base image
FROM python:3.12-slim

# Set environment variable to avoid buffering in Python
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the /app directory inside the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Setting the port to expose
EXPOSE 8080

# Specify the command to run your application
CMD ["streamlit", "run", "app/Chatbot.py", "--server.port=8080", "--server.address=0.0.0.0"]