import connection
import hardware
import video_feed
import threading

hardware.initialize()
hardware.set_status(color='green')

video_feed.initialize() # threading.Thread(target=).start()

connection.establish(
  video_handler=video_feed,
  hardware_handler=hardware
)