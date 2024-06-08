#!/usr/bin/python3
from fabric.api import env, run, put
from os.path import exists
import time

env.hosts = ['54.167.92.252', '54.224.23.19']  # Replace with your server's IP address

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    time_str = time.strftime("%Y%m%d%H%M%S")
    file_name = "web_static_{}.tgz".format(time_str)
    local("mkdir -p versions")
    local("tar -cvzf versions/{} web_static".format(file_name))
    return "versions/{}".format(file_name)

def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not exists(archive_path):
        return False
    
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]
    
    if put(archive_path, "/tmp/{}".format(file)).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed:
        return False
    if run("rm /tmp/{}".format(file)).failed:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False
    if run("touch /data/web_static/releases/{}/my_index.html".format(name)).failed:
        return False
    
    return True

def deploy():
    """Creates and distributes an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)

