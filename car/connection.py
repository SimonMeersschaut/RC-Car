import socket
import struct
import time
import json

def establish(video_handler=None, hardware_handler=None):
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  host_name = socket.gethostname()
  host_ip = socket.gethostbyname(host_name)
  port = 8888
  socket_address = ('0.0.0.0', port)
  server_socket.bind(socket_address)
  server_socket.listen(5)
  print("LISTENING AT:", socket_address)
  while True:
    client_socket, addr = server_socket.accept()
    print('Connection from ', addr)
    # success!
    video_handler.initialize()
    hardware_handler.initialize()
    while True:
      # get video frame
      if video_handler.is_ready():
        frame_data = video_handler.get_frame()
      else:
        frame_data = 'not ready'.encode('utf-8') # camera is being initialized?
      frame_data_size = struct.pack("Q", len(frame_data))
      
      hardware_data = hardware_handler.get_data()
      hardware_data_size = struct.pack("Q", len(hardware_data))
      try:
        client_socket.sendall(hardware_data_size + hardware_data + frame_data + frame_data_size)
      except ConnectionResetError:
        pass # connection closed

    video_handler.close()
    hardware_handler.close()

    client_socket.close()