import socket
from time import sleep
import random as r

interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
allips = [ip[-1][0] for ip in interfaces]

# msg = b'hello world'

virtualPlanks = []
for i in range(20):
    virtualPlanks.append(f"NCI0{r.randint(0, 99999)}")


while True:

    msg = str({"msgDeviceEUI": f"{r.choice(virtualPlanks)}", "msgRSSI": "-43", "msgUpCount": "0", "msgSensorCount": "40",
     "msgSensorReadings": [340, 333, 336, 342, 343, 348, 340, 345, 338, 344, 343, 340, 339, 341, 346, 352, 338, 346,
                           339, 338, 341, 341, 333, 342, 344, 344, 342, 335, 339, 344, 342, 346, 340, 331, 342, 338,
                           345, 345, 327, 332]})

    for ip in allips:
        print(f'sending {msg}\non {ip}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((ip, 0))
        sock.sendto(msg.replace("'", '"').encode("utf-8"), ("255.255.255.255", 2311))
        sock.close()

    sleep(2)
