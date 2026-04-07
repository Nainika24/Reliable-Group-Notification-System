# Reliable-Group-Notification-System
# Reliable UDP Group Notification System

## Overview

This project implements a **Reliable Group Notification System using UDP sockets in Python**. Since UDP does not guarantee packet delivery by default, reliability is achieved using **sequence numbers, acknowledgements (ACK), timeout handling, and retransmission logic** at the application layer.

The system allows multiple clients to subscribe to a server and receive broadcast notifications with delivery confirmation and performance monitoring.

---

## Objective

The objective of this project is to design and implement a **reliable UDP-based notification delivery system** that:

* Supports multiple subscribers
* Broadcasts messages to all clients simultaneously
* Detects packet loss
* Retransmits lost packets
* Tracks acknowledgement success rate
* Measures latency using timestamps
* Calculates packet-loss percentage

---

## Features

* UDP-based communication
* Multi-client group notification
* Subscriber join / leave support
* Custom packet structure
* Sequence number tracking
* Timestamp-based latency measurement
* ACK-based reliability mechanism
* Timeout detection
* Retransmission logic
* Packet-loss percentage calculation
* ACK success-rate monitoring
* Multi-threaded server architecture

---

## Technologies Used

Python built-in modules:

```
socket
threading
json
time
```

No external libraries required.

---

## Project Structure

```
Reliable-UDP-Notification-System
│
├── server.py
├── client.py
├── README.md
├── requirements.txt
└── results/
```

---

## System Architecture

### Server Responsibilities

* Maintains subscriber list
* Receives JOIN and LEAVE requests
* Broadcasts notification messages
* Tracks acknowledgements
* Retransmits lost packets
* Calculates performance metrics

### Client Responsibilities

* Sends JOIN request to server
* Receives notifications
* Calculates latency
* Sends acknowledgement packets back to server

Communication Flow:

Client → JOIN → Server
Server → Notification → Clients
Clients → ACK → Server

---

## Packet Format

Each notification packet contains:

| Field     | Description                             |
| --------- | --------------------------------------- |
| type      | Packet type (DATA / JOIN / LEAVE / ACK) |
| seq       | Sequence number                         |
| message   | Notification text                       |
| timestamp | Packet send time                        |

Example packet:

```
{
"type": "DATA",
"seq": 1,
"message": "Meeting at 2 PM",
"timestamp": 1710000000
}
```

---

## Reliability Mechanism

UDP normally provides **best-effort delivery only**.

Reliability is implemented using:

1. Sequence numbers
2. ACK packets
3. Timeout detection
4. Retransmission logic
5. Packet-loss monitoring

Workflow:

Send packet → Wait for ACK
If ACK missing → Retransmit
Repeat until delivery confirmed or retry limit reached

---

## Performance Metrics

The server calculates:

### ACK Success Rate

ACK Success Rate =
(Total ACK Received / Total Packets Sent) × 100

### Packet Loss Percentage

Packet Loss =
((Packets Sent − ACK Received) / Packets Sent) × 100

The client calculates:

### Latency

Latency = Receive Time − Send Timestamp

---

## How to Run the Project

### Step 1 — Run Server

```
python server.py
```

Expected output:

```
Server started successfully on port 6060
```

---

### Step 2 — Run Client(s)

Run on same machine or different laptops connected to the same network:

```
python client.py
```

Client automatically sends JOIN request to server.

---

### Step 3 — Send Notification

From server terminal:

```
Enter notification: Exam tomorrow at 9 AM
```

Server broadcasts message to all connected clients.

---

## Example Output

### Server Output

```
Subscriber joined: ('192.168.x.x', port)
ACK received from ('192.168.x.x', port)

Packets Sent: 3
ACK Received: 3
ACK Success Rate: 100 %
Packet Loss: 0 %
```

### Client Output

```
Message: Exam tomorrow at 9 AM
Sequence: 1
Latency: 0.02 seconds
```

---

## Performance Evaluation

System tested with multiple subscribers:

| Clients | Result                               |
| ------- | ------------------------------------ |
| 1       | Reliable delivery                    |
| 2       | Reliable delivery                    |
| 3+      | Reliable with retransmission support |

Observation:

Latency increases slightly as number of subscribers increases, but reliability remains high due to retransmission mechanism.

---

## Applications

* Campus announcement systems
* Emergency alert broadcasting
* Classroom notification systems
* Smart IoT alert systems
* Distributed messaging environments

---

## Conclusion

This project successfully converts unreliable UDP communication into a **reliable group notification system** using application-layer reliability techniques such as acknowledgements, sequence numbers, timeout detection, and retransmission. The system ensures accurate delivery while maintaining low communication overhead compared to TCP-based solutions.
