# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy everything to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Set default port env var for Streamlit
ENV PORT=8080

# Start Streamlit app using correct port/address
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
