import cv2
import socket
import struct
import json
import pickle
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8888))  # Replace 'server_ip_address' with the actual server IP

OUTPUT_RESOLUTION = (1280, 720)
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K buffer size
        if not packet:
            break
        data += packet
    if not data:
        break

    packed_metadata_size = data[:payload_size]
    data = data[payload_size:]
    metadata_size = struct.unpack("Q", packed_metadata_size)[0]

    while len(data) < metadata_size:
        data += client_socket.recv(4 * 1024)  # 4K buffer size
    metadata = data[:metadata_size]
    data = data[metadata_size:]
    metadata = json.loads(metadata.decode('utf-8'))
    # print(f"Delay: {time.time() - metadata['timestamp']}") # TODO: not every frame

    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)  # 4K buffer size
        if not packet:
            break
        data += packet
    if not data:
        break

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)  # 4K buffer size
    frame_data = data[:msg_size]
    print(frame_data)
    data = data[msg_size:]

    frame = pickle.loads(frame_data)
    frame = cv2.resize(frame, OUTPUT_RESOLUTION, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    cv2.imshow('Client', frame)
    if cv2.waitKey(1) == 13:
        break

cv2.destroyAllWindows()
client_socket.close()