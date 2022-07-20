# Pakupi

## Quickstart

> Please note that this project is an active work in progress, documentation and features are subject to frequent changes.

Roles:
- Host: the machine used to configure the cluster
- Master: the main node for providing cluster services and interracting with the cluster
- Worker(s): any node whose processsing power is made available to cluster

- Install OS on master (Ubuntu Server 22.04):
	- Fixed IP
	- Open SSH
	- Keep user/password
- Prepare master for Ansible:
	- Deploy ssh key
- Install Ansible on host
	- Install required packages on host: `ansible-galaxy install -r requirements-galaxy.yml`
- Update inventory to include master IP
- Run DHCP setup playbook (01)
- TODO: How to add new worker/client to the inventory/dhcp lease list?
- Install OS on worker (Ubuntu Server 22.04):
	- Keep user/password
	- Setup worker for SSH access 
	- Setup DHCP on Worker (`/boot/firmware/network-config`)
- Run NIS setup playbook (02)
- Run slurm setup playbook (03)
- Run NFS setup playbook (04)
- Run worker configuration playbook (05)
- Run grafana setup playbook (06)
	- Log into grafana `http://<master>:3000` (`admin:admin`)
	- Add slurm dashboard (https://grafana.com/grafana/dashboards/4323)
