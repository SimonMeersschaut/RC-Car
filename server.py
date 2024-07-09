import cv2
import socket
import pickle
import struct
import json
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 8888
socket_address = ('0.0.0.0', port)

server_socket.bind(socket_address)
server_socket.listen(5)
print("LISTENING AT:", socket_address)

while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        while vid.isOpened():
            ret, frame = vid.read()
            if not ret:
                break
            data = pickle.dumps(frame)
            metadata = json.dumps({"timestamp": time.time()}).encode('utf-8')
            metadata_size = struct.pack("Q", len(metadata))
            message_size = struct.pack("Q", len(data))
            client_socket.sendall(metadata_size + metadata + message_size + data)
        vid.release()
        client_socket.close()
