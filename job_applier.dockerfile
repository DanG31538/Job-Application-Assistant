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

# Add Google Chrome repository
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Debugging: Check the content of the Google Chrome list
RUN cat /etc/apt/sources.list.d/google-chrome.list

# Update package list
RUN apt-get update

# Debugging: Check available versions of Google Chrome
RUN apt-cache policy google-chrome-stable

# Install a specific version of Google Chrome
#RUN apt-get install -y google-chrome-stable=114.0.5735.90-1

# Debug: Print installed Chrome version
#RUN echo "Installed Chrome version:" && google-chrome --version

# Install a specific version of ChromeDriver
RUN CHROMEDRIVER_VERSION=114.0.5735.90 \
 && wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P ~/ \
 && unzip ~/chromedriver_linux64.zip -d ~/ \
 && mv -f ~/chromedriver /usr/local/bin/chromedriver \
 && chmod +x /usr/local/bin/chromedriver \
 && rm ~/chromedriver_linux64.zip


# Set the working directory
WORKDIR /app

# Copy requirements.txt into the image
#COPY requirements.txt /app/requirements.txt


# Install Python dependencies from requirements file
#RUN pip install --upgrade pip
#RUN pip install requests
#RUN pip install --no-cache-dir -r requirements.txt

# Use the entrypoint script to initialize the container
#ENTRYPOINT ["/app/entrypoint.sh"]