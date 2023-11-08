# Use the official Python base image
FROM python:3.9

# Setting up system packages and dependencies for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libx11-6 \
 && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update \
 && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P ~/ \
 && unzip ~/chromedriver_linux64.zip -d ~/ \
 && mv -f ~/chromedriver /usr/local/bin/chromedriver \
 && chmod +x /usr/local/bin/chromedriver \
 && rm ~/chromedriver_linux64.zip

# Set the working directory
WORKDIR /app

# Copy the Python requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies from requirements file
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python scripts and JSON identifiers into the Docker image
COPY main.py /app/
COPY applier.py /app/
COPY identifiers.json /app/

# Set the command to run your main.py when the container starts. Last command keeps container running.
CMD ["python", "main.py"]
CMD ["tail", "-f", "/dev/null"] 