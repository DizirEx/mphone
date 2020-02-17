import string
import random

def randomString(strLen):
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(strLen))

def splash():
    return '''                                                                       │
  │'''+randomString(73)+'''│
  │'''+randomString(73)+'''│
  │'''+randomString(27)+''' ▙▗▌▛▀▖▌           '''+randomString(27)+'''│
  │'''+randomString(27)+''' ▌▘▌▙▄▘▛▀▖▞▀▖▛▀▖▞▀▖'''+randomString(27)+'''│
  │'''+randomString(27)+''' ▌ ▌▌  ▌ ▌▌ ▌▌ ▌▛▀ '''+randomString(27)+'''│
  │'''+randomString(27)+''' ▘ ▘▘  ▘ ▘▝▀ ▘ ▘▝▀▘'''+randomString(27)+'''│
  │'''+randomString(73)+'''│
  │'''+randomString(73)+'''│
  │                                                                       '''
