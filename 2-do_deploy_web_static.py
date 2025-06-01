#!/usr/bin/python3
"""Deploy web static to different servers"""
import re
from fabric.context_managers import cd
from fabric.api import env, put, run, sudo
from os.path import join, exists, splitext


env.user = "ubuntu"
env.hosts = ["3.80.145.4", "18.212.49.58"]
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Deploy a compressed archive to a remote server.
    Args:
        archive_path (str): The path to the compressed archive.
    Returns:
        bool: True if the deployment is successful, False otherwise.
    """

    if not exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        file_name = re.search(r'[^/]+$', archive_path).group(0)
        deploy_path = join("/data/web_static/releases/",
                           splitext(file_name)[0])
        sudo("mkdir -p {}".format(deploy_path))

        sudo("tar -xzf /tmp/{} -C {}".format(file_name, deploy_path))

        with cd(deploy_path):
            sudo("mv web_static/* .")
            sudo("rm -rf web_static")

        sudo("rm /tmp/{}".format(file_name))
        sudo("rm -rf /data/web_static/current")

        sudo('ln -sf {} /data/web_static/current'.format(deploy_path))
    except Exception as err:
        return False

    return True

