import subprocess
import paramiko

def ssh(username, ip_address):
    ssh_command = f"ssh {username}@{ip_address}"
    try:
        subprocess.run(["cmd", "/c", ssh_command])
    except Exception:
        print(f"Failed to connect to {ip_address}")

#restarts device type shit
def reboot(ip_address_name, username_name, password_name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    router_ip = ip_address_name
    router_username = username_name
    router_password = password_name

    ssh.connect(router_ip, username=router_username, password=router_password)
    stdin, stdout, stderr = ssh.exec_command("sudo shutdown -r now")
    output = stdout.readlines()

    for line in output:
        print(line.strip())

#shuts down device
def shutdown(ip_address_name, username_name, password_name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    router_ip = ip_address_name
    router_username = username_name
    router_password = password_name

    ssh.connect(router_ip, username=router_username, password=router_password)
    stdin, stdout, stderr = ssh.exec_command("sudo shutdown now")
    output = stdout.readlines()

    for line in output:
        print(line.strip())
              
#add buttons for shutdown and reboot
