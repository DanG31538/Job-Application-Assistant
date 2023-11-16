# Use the official Python base image
FROM python:3.9

# Setting up system packages and dependencies
RUN apt-get update && apt-get install -y \
    wget \
 && rm -rf /var/lib/apt/lists/*

# Download and install a specific version of Chromium
RUN wget [URL_OF_SPECIFIC_CHROMIUM_BUILD] -O chromium.deb
RUN dpkg -i chromium.deb || apt-get install -fy

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY webdriver_test_requirements.txt /app/
RUN pip install --no-cache-dir -r webdriver_test_requirements.txt

# Copy the webdriver test script into the container
COPY webdriver_test_script.py /app/

# Run the webdriver test script when the container starts and redirect output to a file
CMD python webdriver_test_script.py > /app/script_output.txt

# Optionally, you can still keep the command to output the installed Chromium version
RUN which chromium-browser
RUN chromium-browser --version > /chrome_version.txt
