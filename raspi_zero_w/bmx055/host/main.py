import paramiko

def connect_raspi():
    hostname = "raspberrypi"
    username = "pi"
    port = 22
    key_file = "../../ssh_keys/raspi_zero"
    key = paramiko.Ed25519Key.from_private_key_file(key_file)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=port, username=username, pkey=key)
    command = "cd attitude_estimation/raspi_zero_w/bmx055;python3 bmx055.py"
    stdin, stdout, stderr = client.exec_command(command)

    for o in stdout:
        print(o, end="")
    for e in stderr:
        print(e, end="")

    client.close()

def main():
    connect_raspi()

if __name__ == "__main__":
    main()
