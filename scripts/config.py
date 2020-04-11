'''
Import this file for current serial port settings
'''

#TODO: allow env variables to override these so no code changes needed

OPEN_WEATHER_MAP_API_KEY='72be76e2d922e36ab8e1537afa9fead8'

PORT = '/dev/ttyACM0'
#PORT = '/dev/ttyUSB0'
#port = '/dev/ttyVIRTUAL'

BAUD_RATE = 19200

# motion detection DBUS interface
MOTION_DETECT_INTERFACE_NAME = 'com.MotionDetectService'
MOTION_DETECT_OBJECT_PATH = '/com/motiondetect/object'

MOTION_DETECT_SIGN_ON_TIME_MINUTES = 20
MOTION_DETECT_SIGN_ON_TIME_SECONDS = MOTION_DETECT_SIGN_ON_TIME_MINUTES * 60
MOTION_DETECT_SIGN_ON_TIME_MILLISECONDS = MOTION_DETECT_SIGN_ON_TIME_SECONDS * 1000

# after the sign turns on, how long do we wait before motion detection can turn it on again?
SIGN_ENABLE_ON_TIMEOUT_HOURS = 2
SIGN_ENABLE_ON_TIMEOUT_MIN = SIGN_ENABLE_ON_TIMEOUT_HOURS * 60
SIGN_ENABLE_ON_TIMEOUT_SEC = SIGN_ENABLE_ON_TIMEOUT_MIN * 60
SIGN_ENABLE_ON_TIMEOUT_MS = SIGN_ENABLE_ON_TIMEOUT_SEC * 1000