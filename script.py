#!/usr/bin/python3
  
import re, sys, subprocess

server = sys.argv[1] #get server name from command line
p_server = "({0})".format(sys.argv[1]) #regexp pattern of server name
p_ip = "(ip:)(.+)" #target server pattern
p_bastion = "(bastion:)(.+)" #bastion server pattern

with open("inventory", "r") as file: #open inventory and go line by line looking for target server name matching the one from command 
    for line in file:
        match = re.search(p_server,line)
        if match: #if server found in inventory
            print("Server found:", match.group(1)) #print target server name
            ip_line = re.search(p_ip, file.readline()) #search for target server IP
            target = ip_line.group(2).strip()
            print("Target IP:", target)
            
            bastion_line = re.search(p_bastion, file.readline()) #search for bastion server IP
            bastion = bastion_line.group(2).strip() 
            print("Bastion IP:", bastion)
            
            command = sys.argv[2] #command to run on target server
            
            #finally, execute command on target server using bastion as jump host
            execute = 'ssh -o ProxyCommand="ssh -i /home/gcp/.ssh/bastion_key -W %h:%p gcp@{0}" -i /home/gcp/.ssh/target_key gcp@{1} "{2}"'.format(bastion, target, command)
            p = subprocess.Popen(execute, stdout=subprocess.PIPE, shell = True, universal_newlines=True)
            output, err = p.communicate()
            print("Command result:")
            print(output)
            print("Return code:",err)
