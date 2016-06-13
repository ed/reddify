import re
import urllib.request
import simplejson
from collections import namedtuple
from operator import itemgetter


class Song(object):
    def __init__(self):
        self._artist = ""
        self._track = ""
        self._spotify_id = ""
        self._pattern = re.compile('(.*)-(.*)')

    def run(self, s):
        result = re.search(self._pattern,s)
        result = result.string
        if '-' in result:
            result = result.split('-')
        try:
            self._artist = result[0].rstrip().lstrip().lower()
            self._track = result[1].lstrip().rstrip().replace(' ','+')
        except:
            pass


    def get_spotify_id(self):
        url ="https://api.spotify.com/v1/search?q=%s&type=track&market=US" % (self.track)
        r = urllib.request.urlopen(url)
        data = simplejson.load(r)
        PopId = namedtuple('PopId', 'pop spotify_id')
        popid_list = []
        for i in range(0, len(data["tracks"])):
            if data["tracks"]["items"][i]["artists"][0]['name'].lower() == self.artist:
                popid_list.append(PopId(data["tracks"]["items"][i]["popularity"], data["tracks"]["items"][i]["uri"]))
        self._spotify_id = max(popid_list,key=itemgetter(0))[1]

