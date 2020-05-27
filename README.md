Team members (Team 13)::
`Yuansan Liu, 1037351`
`Karun Varghese Mathew, 1007247`
`Junlin Chen, 1065399`
`Jingyi Shao, 1049816`
`Han Jiang, 1066425`


[Front end demo](http://172.26.131.162:8080/)

# Deployment Guide
## System requirement
* Ansible 2.9

## Deployment Process
1. Make sure to use Unimelb VPN connection even though you’re using campus network. Ansible may hangs if being run from unimelb network without proxy.
2. Clone the repo from https://github.com/Lysarthas/CCCa2 and go to `nectar` folder.
3. To deploy, here is three cases:
  3.1 create instances and setup remote instance and start the service. For the first case, run
  ```
  source ./openrc.sh
  ansible-playbook master.yaml --extra-var db_action=backup
  ```
  3.2 remote instance is all set and only setup/restart service (docker swarm, concul, couchdb, web app, etc). In this case, data from cluster will be backup to backup db in semi-realtime(couples of mins) in incremental manner. For the second case, run
  ```
  source ./openrc.sh
ansible-playbook remote.yaml --extra-var db_action=backup
  ```
  3.3 restart couchdb and store the data from `backupdb` to `cluster` when the cluster failed. This is a rare case. For the third case, run
  ```
  source ./openrc.sh
ansible-playbook remote.yaml --extra-var db_action=restore
  ```