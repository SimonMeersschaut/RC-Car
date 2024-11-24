import random
import pickle

def initialize():
  print('Initializing hardware...')
  # TODO set lights etc.
  print('Hardware initialized.')

def set_status(color):
  # TODO set status light
  pass

def is_ready():
  return True

def get_data():
  # output = random.randint(0, 10)
  # output = output << 4 # space for status bits
  # # Set status bits
  # for index, value in enumerate([False, False, True, False]):
  #   if value:
  #     # set high
  #     output = output | (1 << index)
  #   else:
  #     # set low
  #     output = output & (0 << index)
  # return bin(output)
  return pickle.dumps({
    'data': [False, False, True, False]
  })

def close():
  pass