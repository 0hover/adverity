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
