#!/usr/bin/env bash
# This script sets up your web servers for the deployment of web_static

# Exit on error
set -e

# Install Nginx if it is not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get update
    sudo apt-get -y install nginx
    sudo ufw allow 'Nginx HTTP'
fi

# Create the necessary directories with appropriate permissions
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file to test the Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create (or recreate) the symbolic link
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
nginx_config="/etc/nginx/sites-available/default"

if ! grep -q "location /hbnb_static/" "$nginx_config"; then
    sudo sed -i "/^\s*server_name _;/a \\\n    location /hbnb_static/ {\n        alias /data/web_static/current/;\n        autoindex off;\n    }\n" "$nginx_config"
fi

# Restart Nginx to apply the changes
sudo service nginx restart

# Ensure the script exits successfully
exit 0

