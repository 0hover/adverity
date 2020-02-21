# adverity

## Question1
Assuming that each server has config in ~/.ssh/config like below

```bash
Host bastion1
  HostName <bastion1 ip>
  User ubuntu

Host server1
  HostName <server1 ip>
  ProxyJump bastion1
  User ubuntu
```
command to run will be

`ssh server1`

Without config in `~/.ssh/config`

`ssh -J ubuntu@<bastion1:port> <ubuntu@server1:port>`  

Based on ssh man page

```
-J [user@]host[:port]
             Connect to the target host by first making a ssh connection to the jump host and then establishing a TCP forwarding to the ultimate destination from there
```


## Question 2
It is still ambiguous. If these would be random servers in random moments and random commands there is not much to ease the process. You can only write simple script in BASH, Python or any language of choice which will take command and server name as an arguments and execute it remotely using configuration explained above.
If this is would be one command in specified time periods then I'll add cron to this solution.
It is also possible to use Ansible CLI or pssh tool to run commands on several machines in parallel but for this inventory file needs to be altered.

---

Update on 21.02.2020  
I prepared infrasctructure on GCP for this excercise so it is possible to present this solution on real machines.
1) there are three servers: 'local' based on Ubuntu, bastion and target server based on CentOS 6
2) there are seperate, distinct keys for each machine stored in /home/gcp/.ssh folder on local server named bastion_key and target_key respectively
3) user for both bastion and target server is gcp
4) inventory file must exist on local machine in the same folder as the script
5) in order to execute script it has been modified to allow execution : `chmod +x`
6) to run script user has to provide argumens in following manner `$ ./script.py <server name> <command to execute on target>` ie. ./script.py server1 'ls -lah'

This is obviously PoC without any comments, error handling etc. intended to show possible solution for problem from question 2.
![GCP inventory](gcp_servers.png?raw=true "Title")
