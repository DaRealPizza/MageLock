import socket, pickle

ip = "0.0.0.0"
port = 40183

con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
con.bind((ip, port))

room = {}

class Packet:
    def __init__(self, x, y, cls, address):
        self.x = x
        self.y = y
        self.cls = cls
        self.address = address

while True:
    data, addr = con.recvfrom(1024)
    data = pickle.loads(data)
    if isinstance(data, str):
        if data.startswith("HEADER:"):
            header = data[7:]
            print(f"{addr} sends header {header}")

            if header == "JOIN":
                print(f"{addr} joined room")
            elif header == "LEAVE":
                del room[addr]
                print(f"{addr} left room")
            elif header == "FETCHROOM":
                con.sendto(pickle.dumps(room), addr)
            else:
                print(f"{addr} sends invalid header: {header}")
    if isinstance(data, Packet):
        room[addr] = data
        
        enemies = list(room.values())
        con.sendto(pickle.dumps(enemies), addr)
        
    