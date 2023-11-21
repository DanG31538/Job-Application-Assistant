# Start from the official Selenium Chrome standalone image
FROM selenium/standalone-chrome

# Switch to root to install Python
USER root

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy all the required files into the container
COPY applier.py /app/
COPY entrypoint.sh /app/
COPY identifiers.json /app/
COPY main.py /app/
COPY openai_query.py /app/
COPY requirements.txt /app/
COPY resume_parser.py /app/

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh


# Install Python dependencies
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Try installing 2captcha-python separately
RUN pip3 install 2captcha-python==1.1.0

# Use your entrypoint script to initialize the container
ENTRYPOINT ["/app/entrypoint.sh"]
