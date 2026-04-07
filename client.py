# ==========================================
# Reliable UDP Notification Client (FIXED)
# ==========================================

import socket
import json
import threading
import time


SERVER_IP = "127.0.0.1"
SERVER_PORT = 5055   # MUST match server port


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_join():

    packet = {"type": "JOIN"}

    client_socket.sendto(
        json.dumps(packet).encode(),
        (SERVER_IP, SERVER_PORT)
    )

    print("Connected to server")


def send_leave():

    packet = {"type": "LEAVE"}

    client_socket.sendto(
        json.dumps(packet).encode(),
        (SERVER_IP, SERVER_PORT)
    )

    print("Disconnected from server")


def send_ack(seq):

    packet = {
        "type": "ACK",
        "seq": seq
    }

    client_socket.sendto(
        json.dumps(packet).encode(),
        (SERVER_IP, SERVER_PORT)
    )


def receive_messages():

    while True:

        try:

            data, addr = client_socket.recvfrom(1024)

            packet = json.loads(data.decode())

            seq = packet["seq"]
            message = packet["message"]

            send_time = packet["timestamp"]
            latency = time.time() - send_time

            print("\nMessage:", message)
            print("Sequence:", seq)
            print("Latency:", round(latency, 4), "seconds")

            send_ack(seq)

        except:

            print("Invalid packet ignored")


send_join()

threading.Thread(
    target=receive_messages,
    daemon=True
).start()


try:

    while True:
        pass

except KeyboardInterrupt:

    send_leave()