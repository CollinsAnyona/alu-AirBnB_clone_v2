#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers"""
from fabric.api import *
import os
import re
from datetime import datetime

env.user = 'ubuntu'
env.hosts = ['54.167.92.252', '54.224.23.19']


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    local("mkdir -p versions")
    archive_name = "versions/web_static_{}.tgz".format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
    result = local("tar -cvzf {} web_static".format(archive_name), capture=True)
    if result.failed:
        return None
    return archive_name


def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    if not os.path.isfile(archive_path):
        return False

    filename_regex = re.compile(r'[^/]+(?=\.tgz$)')
    match = filename_regex.search(archive_path)
    if not match:
        return False

    archive_filename = match.group(0)
    remote_tmp_path = "/tmp/{}.tgz".format(archive_filename)
    remote_release_path = "/data/web_static/releases/{}".format(archive_filename)

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, remote_tmp_path)

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        run("mkdir -p {}".format(remote_release_path))
        run("tar -xzf {} -C {}".format(remote_tmp_path, remote_release_path))

        # Remove the archive from the web server
        run("rm {}".format(remote_tmp_path))

        # Move the contents from the web_static to the parent directory
        run("mv {0}/web_static/* {0}/".format(remote_release_path))
        run("rm -rf {}/web_static".format(remote_release_path))

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(remote_release_path))

        # Create a 0-index.html file inside the release folder for testing
        run("echo '<html><head></head><body>Holberton School</body></html>' > {}/0-index.html".format(remote_release_path))

        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

