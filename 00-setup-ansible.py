"""
Setup ansible on selected hosts (by name or ip)
"""

import ansible.inventory.manager
import ansible.parsing.dataloader
import argparse
import fabric
import getpass
import os
import pathlib
import subprocess


ANSIBLE_SSHKEY = os.getenv("ANSIBLE_SSHKEY", str(pathlib.Path("~", ".ssh", "id_rsa")))
ANSIBLE_USER = os.getenv("ANSIBLE_USER", "user")
ANSIBLE_PASSWORD = "user"


@fabric.task
def setup_worker(c):
    print(c.client)
    # c.put("sources.list", "/tmp/sources.list")
    # c.sudo("mv /tmp/sources.list /etc/apt/sources.list")
    # c.put("raspi.list", "/tmp/raspi.list")
    # c.sudo("mv /tmp/raspi.list /etc/apt/sources.list.d/raspi.list")
    c.sudo("date --set '2031-12-31 20:45:00'")
    c.sudo("apt -y update")
    #c.sudo("apt -y upgrade")
    c.sudo("apt -y install ansible")
    #c.reboot()


def find_inventory_hosts(inventory):
    loader = ansible.parsing.dataloader.DataLoader()
    inventory_manager = ansible.inventory.manager.InventoryManager(loader=loader, sources=[inventory])
    return list(map(lambda i: i.get_vars()["ansible_host"], inventory_manager.list_hosts("all")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="Set the target host user for ssh commands", default=ANSIBLE_USER)
    parser.add_argument("-i", "--identity", help="Set the SSH identity to use for ssh commands", default=ANSIBLE_SSHKEY)
    parser.add_argument("--ssh-only", help="Only setup ssh identity, do not install packages", action="store_true")
    parser.add_argument("--inventory", help="Set the target hosts from inventory file (YAML)")
    parser.add_argument("host", nargs="*", help="Set the target hosts")
    arguments = parser.parse_args()
    # Get target user password
    arguments.password = getpass.getpass("Password for '{}' [default:{}]: ".format(arguments.user, ANSIBLE_PASSWORD))
    if not arguments.password:
        arguments.password = ANSIBLE_PASSWORD
    # Find host addresses
    hosts = list(arguments.host)
    if arguments.inventory:
        hosts += find_inventory_hosts(arguments.inventory)
    # Define SSH config for fabric
    config = fabric.Config(overrides={"user": arguments.user, "sudo": {"password": arguments.password}})
    # Copy ssh identity on workers
    for host in hosts:
        print("SSH-COPY_ID {}@{}".format(arguments.user, host))
        subprocess.run([ "ssh-copy-id", "-o", "StrictHostKeyChecking=no",  "-f",
                        "-i", arguments.identity, "{}@{}".format(arguments.user, host)])
    # Setup workers
    if not arguments.ssh_only:
        for connection in fabric.Group(*hosts, config=config, connect_kwargs={"password": arguments.password}):
            print(connection.host)
            setup_worker(connection)
