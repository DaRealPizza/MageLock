import socket, pickle

ip = "0.0.0.0"
port = 40183

# connect to server
con = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
con.bind((ip, port))

room = {}

# define player sent packet
class Packet:
    def __init__(self, x, y, cls, address, animationstate):
        self.x = x
        self.y = y
        self.cls = cls
        self.address = address
        self.animationstate = animationstate

# main loop
while True:
    # receive data from players
    data, addr = con.recvfrom(1024)
    data = pickle.loads(data)

    # check if the data is a header
    if isinstance(data, str):
        if data.startswith("HEADER:"):
            header = data[7:]
            print(f"{addr} sends header {header}")

            if header == "JOIN": # join header
                print(f"{addr} joined room")
            elif header == "LEAVE": # leave header
                del room[addr]
                print(f"{addr} left room")
            elif header == "FETCHROOM": # fetchroom header
                con.sendto(pickle.dumps(room), addr)
            elif header == "CRASH": # crash header
                del room[addr]
                print(f"{addr} crashed")
            else: # invalid header
                print(f"{addr} sends invalid header: {header}")
    # check if the data is a player packet
    if isinstance(data, Packet):
        # updates room based on player packet
        room[addr] = data

        # responds with enemy data
        enemies = list(room.values())
        con.sendto(pickle.dumps(enemies), addr)
    