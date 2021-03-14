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
    stdin, stdout, stderr = client.exec_command("ls -al")

    for o in stdout:
        print("[std]", o, end="")
    for e in stderr:
        print("[err]", e, end="")

    client.close()

def main():
    connect_raspi()

if __name__ == "__main__":
    main()
