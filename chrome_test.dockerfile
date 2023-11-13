# Use the official Python base image
FROM python:3.9

# Setting up system packages and dependencies
RUN apt-get update && apt-get install -y \
    wget \
 && rm -rf /var/lib/apt/lists/*

# Add Google Chrome repository
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Update package list
RUN apt-get update

#Invalidate cache and write available versions of Google Chrome to a file
RUN echo "Invalidating cache" && apt-cache policy google-chrome-stable > /chrome_versions.txt
