#!/usr/bin/python3
  
import re, sys, subprocess

server = sys.argv[1]
p_server = "({0})".format(sys.argv[1])
p_ip = "(ip:)(.+)"
p_bastion = "(bastion:)(.+)"
with open("inventory", "r") as file:
    match = re.search(p_server,file.readline())
    if match:
        print("Server found:", match.group(1))
        ip_line = re.search(p_ip, file.readline())
        target = ip_line.group(2).strip()
        print("Target IP:", target)
        bastion_line = re.search(p_bastion, file.readline())
        bastion = bastion_line.group(2).strip()
        print("Bastion IP:", bastion)
        command = sys.argv[2]
        execute = 'ssh -o ProxyCommand="ssh -i /home/gcp/.ssh/bastion_key -W %h:%p gcp@{0}" -i /home/gcp/.ssh/target_key gcp@{1} "{2}"'.format(bastion, target, command)
        p = subprocess.Popen(execute, stdout=subprocess.PIPE, shell = True, universal_newlines=True)
        output, err = p.communicate()
        print("Command result:", output, end='')
        print("Return code:",err)
