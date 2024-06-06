#!/usr/bin/env bash
# Script to set up web static environment

# Update and upgrade system packages
sudo apt-get -y update
sudo apt-get -y upgrade

# Install nginx if not already installed
sudo apt-get -y install nginx

# Create necessary directories with correct permissions
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a test HTML file in the test directory
echo "Hello, this is a test HTML file." | sudo tee /data/web_static/releases/test/index.html

# Remove existing symbolic link if it exists
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi

# Create a new symbolic link to the test directory
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership of the /data/ directory to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update nginx configuration if not already updated
if ! grep -q "location /hbnb_static" /etc/nginx/sites-available/default; then
    sudo sed -i '44i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
fi

# Restart nginx to apply the changes
sudo service nginx restart

# Output success message
echo "Nginx configuration updated and localhost/hbnb_static available"
