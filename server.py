# ==========================================
# Reliable UDP Notification Server (FIXED)
# ==========================================

import socket
import threading
import json
import time

SERVER_IP = "0.0.0.0"
SERVER_PORT = 6060  # Changed port to avoid conflict

TIMEOUT = 2
MAX_RETRIES = 5

subscribers = set()
acknowledgements = {}
lock = threading.Lock()

seq_number = 0
total_sent = 0
total_ack = 0


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Important fix for Windows port reuse issue
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_IP, SERVER_PORT))

print("Server started successfully on port", SERVER_PORT)


def create_packet(message, seq):

    return json.dumps({
        "type": "DATA",
        "seq": seq,
        "message": message,
        "timestamp": time.time()
    }).encode()


def receive_handler():

    global total_ack

    while True:

        try:

            data, addr = server_socket.recvfrom(1024)

            packet = json.loads(data.decode())

            if packet["type"] == "JOIN":

                with lock:
                    subscribers.add(addr)

                print("Subscriber joined:", addr)


            elif packet["type"] == "LEAVE":

                with lock:

                    if addr in subscribers:
                        subscribers.remove(addr)

                print("Subscriber left:", addr)


            elif packet["type"] == "ACK":

                seq = packet["seq"]

                with lock:
                    acknowledgements[(addr, seq)] = True

                total_ack += 1

                print("ACK received from", addr)

        except:

            print("Invalid packet ignored")


def reliable_send(client, packet, seq):

    global total_sent

    retries = 0

    while retries < MAX_RETRIES:

        server_socket.sendto(packet, client)

        total_sent += 1

        time.sleep(TIMEOUT)

        with lock:

            if (client, seq) in acknowledgements:

                print("Delivered to", client)
                return

        retries += 1

        print("Retry", retries, "→", client)

    print("Delivery FAILED to", client)


def send_notification(message):

    global seq_number

    seq_number += 1

    packet = create_packet(message, seq_number)

    with lock:

        clients = list(subscribers)

    for client in clients:

        threading.Thread(
            target=reliable_send,
            args=(client, packet, seq_number)
        ).start()


def print_metrics():

    if total_sent == 0:
        return

    success_rate = (total_ack / total_sent) * 100
    loss_rate = ((total_sent - total_ack) / total_sent) * 100

    print("\n===== PERFORMANCE METRICS =====")

    print("Packets Sent:", total_sent)
    print("ACK Received:", total_ack)
    print("ACK Success Rate:", round(success_rate, 2), "%")
    print("Packet Loss:", round(loss_rate, 2), "%")

    print("===============================\n")


threading.Thread(
    target=receive_handler,
    daemon=True
).start()


while True:

    message = input("Enter notification: ")

    send_notification(message)

    time.sleep(1)

    print_metrics()