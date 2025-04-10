FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit needs this
ENV PYTHONUNBUFFERED=1
ENV PORT 8080

# Expose Streamlit port
EXPOSE 8080

# Start Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
