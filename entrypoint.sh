#!/bin/bash

# Start Xvfb
Xvfb :99 -screen 0 1024x768x16 &

# Start fluxbox (a lightweight window manager)
fluxbox &

# Start x11vnc
x11vnc -display :99 -forever -usepw -create &

# Execute the main command (e.g., start your Selenium script)
exec "$@"
