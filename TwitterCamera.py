from twython import TwythonStreamer
from twython import Twython
from picamera import PiCamera
from time import sleep

consumer_key        = '' #These must be added for code to work
consumer_secret     = ''
access_token        = ''
access_token_secret = ''


twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

camera = PiCamera()
camera.zoom = (0.2, 0.1, 0.6, 0.75)

class myStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            sleep(2)
            camera.capture('/home/pi/LoopTrackSelfie/selfie.jpg')
            photo = open('/home/pi/LoopTrackSelfie/selfie.jpg', 'rb')
            response = twitter.upload_media(media=photo)
            message = '@' + data['user']['screen_name']
            twitter.update_status(status=message, media_ids=[response['media_id']])

    def on_error(self, status_code, data):
        print(status_code)

def startTwitterStream():
    stream = myStreamer(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )
    stream.statuses.filter(track='loop track selfie, #looptrackselfie')

startTwitterStream()
