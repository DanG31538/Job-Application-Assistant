# Start from the official Selenium Chrome standalone image
FROM selenium/standalone-chrome

# Switch to root to install Python and other dependencies
USER root

# Install Python, pip, Xvfb, x11vnc, and fluxbox (a lightweight window manager)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    xvfb \
    x11vnc \
    fluxbox \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy all the required files into the container
COPY applier.py /app/
COPY identifiers.json /app/
COPY main.py /app/
COPY openai_query.py /app/
COPY requirements.txt /app/
COPY resume_parser.py /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Set up VNC server (replace 'yourpassword' with a password of your choice)
RUN x11vnc -storepasswd vnc123 /etc/x11vnc.pass

# Expose VNC port (5900 is the default VNC port)
EXPOSE 5900

# Copy the modified entrypoint script into the container
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint to your modified script
ENTRYPOINT ["/app/entrypoint.sh"]
