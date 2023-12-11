#!/bin/bash

# Print a message to indicate the script has started
echo "Starting the Docker container..."

# Start Xvfb
echo "Starting Xvfb..."
Xvfb :99 -screen 0 1024x768x16 &
XVFB_PID=$!
echo "Xvfb started, PID: $XVFB_PID"
sleep 2 # give it some time to start

# Start fluxbox (a lightweight window manager)
echo "Starting fluxbox..."
fluxbox &
FLUXBOX_PID=$!
echo "fluxbox started, PID: $FLUXBOX_PID"
sleep 2 # give it some time to start

# Start x11vnc without a password
echo "Starting x11vnc without a password..."
x11vnc -display :99 -forever -nopw -create &
X11VNC_PID=$!
echo "x11vnc started, PID: $X11VNC_PID"
sleep 2 # give it some time to start

# Check if Xvfb, fluxbox, and x11vnc are still running
if ! kill -0 $XVFB_PID > /dev/null 2>&1; then
    echo "Xvfb did not start correctly."
    exit 1
fi

if ! kill -0 $FLUXBOX_PID > /dev/null 2>&1; then
    echo "fluxbox did not start correctly."
    exit 1
fi

if ! kill -0 $X11VNC_PID > /dev/null 2>&1; then
    echo "x11vnc did not start correctly."
    exit 1
fi

# Echo a message indicating that all processes have been started
echo "All processes started. Container is now running."

# Keep the script running
echo "Entering infinite loop to keep the container alive. Press Ctrl+C to exit."
while true; do
    sleep 3600
done
