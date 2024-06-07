#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers.
"""

from fabric.api import env, run, put, local
from datetime import datetime
import os

env.hosts = ['54.167.92.252', '54.224.23.19']

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    Returns the archive path if successful, otherwise returns None.
    """
    try:
        if not os.path.exists("versions"):
            os.mkdir("versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("echo 'New version deployed!' > web_static/my_index.html")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to web servers.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        bool: True if all operations have been done correctly, otherwise False.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path = "/data/web_static/releases/"

        # Upload the archive to /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Create the release directory
        run

