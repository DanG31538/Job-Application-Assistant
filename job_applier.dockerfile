FROM python:3.9



# Setting up system packages and dependencies for Chrome
RUN set -e \
    && apt-get update -q \
    && apt-get install -yq \
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
RUN wget https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin && \
    rm chromedriver_linux64.zip

# Set ChromeDriver as an executable
RUN chmod +x /usr/local/bin/chromedriver

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install requests==2.26.0
RUN pip install --no-cache-dir -r requirements.txt