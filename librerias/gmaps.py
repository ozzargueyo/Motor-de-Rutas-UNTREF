import googlemaps
import config.googlemaps
class Gmaps(object):
    def __init__(self):
        self.client = googlemaps.Client(key=config.googlemaps.API_KEY)


gmaps = Gmaps()
