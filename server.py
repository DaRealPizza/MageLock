import socket, pickle

ip = "0.0.0.0"
port = 40183

con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
con.bind((ip, port))

room = []

while True:
    data, addr = con.recvfrom(1024)
    if data.decode().startswith("HEADER:"):
        header = data[7:].decode()
        print(f"{addr} sends header {header}")

        if header == "JOIN":
            room.append(addr)
            print(f"{addr} joined room")
        elif header == "LEAVE":
            room.remove(addr)
            print(f"{addr} left room")
        elif header == "FETCHROOM":
            con.sendto(pickle.dumps(room), addr)
        else:
            print(f"{addr} sends invalid header: {header}")
    else:
        print(f"{addr} sends invalid data: {data.decode()}")