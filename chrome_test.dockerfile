# Use the official Python base image
FROM python:3.9

# Setting up system packages and dependencies
RUN apt-get update && apt-get install -y \
    wget \
 && rm -rf /var/lib/apt/lists/*

# Add Google Chrome repository
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY webdriver_test_requirements.txt /app/
RUN pip install --no-cache-dir -r webdriver_test_requirements.txt

# Copy the webdriver test script into the container
COPY webdriver_test_script.py /app/

# Run the webdriver test script when the container starts and redirect output to a file
CMD python webdriver_test_script.py > /app/script_output.txt

RUN google-chrome --version > /chrome_version.txt

