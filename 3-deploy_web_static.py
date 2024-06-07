#!/usr/bin/python3
# Creates and distributes an archive to a web server.
import os
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['54.167.92.252', '54.224.23.19']


def do_pack():
    """Creates gzipped archive of the directory web_static"""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed:
        return None
    return file


def do_deploy(archive_path):
    """
    Function to distribute archive to a web server
    Args:
        archive_path (str): Path to the archive to distribute
    """
    if not os.path.isfile(archive_path):
        return False

    # Extracting the file name without the extension
    filename = os.path.basename(archive_path)
    name = filename.split(".")[0]

    # Defining the remote paths
    remote_tmp_path = "/tmp/{}".format(filename)
    remote_release_path = "/data/web_static/releases/{}".format(name)

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, remote_tmp_path)

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        run("mkdir -p {}".format(remote_release_path))
        run("tar -xzf {} -C {}".format(remote_tmp_path, remote_release_path))

        # Delete the archive from the web server
        run("rm {}".format(remote_tmp_path))

        # Move the contents from the web_static to the parent directory
        run("mv {0}/web_static/* {0}/".format(remote_release_path))
        run("rm -rf {}/web_static".format(remote_release_path))

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(remote_release_path))

        # Create a my_index.html file inside the release folder for testing
        run("echo 'Hello, world!' > /data/web_static/releases/{}/my_index.html".format(name))

        return True
    except:
        return False


def deploy():
    """
    Creates and distributes an archive to a web server
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

