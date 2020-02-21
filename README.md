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
6) to run script user has to provide argumens in following manner `$ ./script.py <server name> <command to execute on target>` ie. `./script.py server1 'ls -lah'`

This is obviously PoC without any comments, error handling etc. intended to show possible solution for problem from question 2.  
Current setup on GCP
![GCP inventory](gcp_servers.png?raw=true "Title")
  
Example run. Compare internal IP from above with command result below. You will notice that command returns IP of target server.

```bash
gcp@instance:~/adverity$ ls -lah
total 16K
drwxrwxr-x 2 gcp gcp 4.0K Feb 21 19:41 .
drwxr-xr-x 8 gcp gcp 4.0K Feb 21 19:41 ..
-rw-rw-r-- 1 gcp gcp   96 Feb 21 19:41 inventory
-rwxr-xr-x 1 gcp gcp 1.1K Feb 21 19:41 script.py
gcp@instance:~/adverity$ ./script.py server1 'sudo ifconfig'
Server found: server1
Target IP: 35.222.15.186
Bastion IP: 35.202.96.42
Command result:
eth0      Link encap:Ethernet  HWaddr 42:01:0A:80:00:0B  
          inet addr:10.128.0.11  Bcast:10.128.0.11  Mask:255.255.255.255
          inet6 addr: fe80::4001:aff:fe80:b/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1460  Metric:1
          RX packets:28723 errors:0 dropped:0 overruns:0 frame:0
          TX packets:27554 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:28280796 (26.9 MiB)  TX bytes:3294995 (3.1 MiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)


Return code: None
gcp@instance:~/adverity$ cat inventory 
server1:
  ip: 35.222.15.186 
  bastion: 35.202.96.42
server2:
  ip: 0.0.0.0
  bastion: 1.1.1.1
gcp@instance:~/adverity$
```
