import re
import urllib.request
import simplejson
from collections import namedtuple
from operator import itemgetter

# v0.01

# API STUFF
# TOKEN GOES HERE
# REQUEST ONE AT SPOTIFY WEB API
# https://developer.spotify.com/web-api/console/get-several-albums/
TOKEN = ""
OAUTH_TOKEN = "Bearer " + TOKEN


class Playlist(object):
    def __init__(self, account_name, playlist):
        self._playlist_name = playlist
        self._playlist_id = ""
        self._account_name = account_name
        self._song_list = []


    def create_playlist(self, playlist_name):
        url = "https://api.spotify.com/v1/users/%s/playlists" % (self._account_name)
        data = "{\"name\":\"%s\",\"public\":false}" % (playlist_name)
        bytes = data.encode('UTF-8')
        req = urllib.request.Request(url, bytes)
        req.add_header("Accept", "application/json")
        req.add_header("Authorization", OAUTH_TOKEN)
        req.add_header("Content-Type", "application/json")
        urllib.request.urlopen(req)


    def get_playlist_id(self):
        url = "https://api.spotify.com/v1/users/%s/playlists" % (self._account_name)
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("Authorization", OAUTH_TOKEN)
        r = urllib.request.urlopen(req)
        data = simplejson.load(r)
        for i in range(0, len(data['items'])):
            if data['items'][i]['name'] == self._playlist_name:
                self._playlist_id = data['items'][i]['id']
                self._playlist_name = data['items'][i]['name']


    def export_playlist(self):
        SongData = namedtuple('SongData', 'name artist uri')
        url = "https://api.spotify.com/v1/users/%s/playlists/%s/tracks" % (self._account_name, self._playlist_id)
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("Authorization", OAUTH_TOKEN)
        r = urllib.request.urlopen(req)
        data = simplejson.load(r)
        for i in range(0, len(data['items'])):
            track = data['items'][0]['track']['name']
            artist = data['items'][0]['track']['artists'][0]['name']
            uri = data['items'][0]['track']['uri']
            self._song_list.append(SongData(track, artist, uri))
        with open(self._playlist_id+"_export.csv", 'w') as f:
            a = csv.writer(f, delimiter = ',')
            f.write("song, artist, spotify uri")
            for i in range(0, len(self._song_list)):
                track = self._song_list[i].track
                artist = self._song_list[i].artist
                uri = self._song_list[i].uri
                csv.writerow([track, artist, uri])


    def add_tracks(self, spotify_ids):
        url = "https://api.spotify.com/v1/users/%s/playlists/%s/tracks?uris=%s" % (self._account_name, self._playlist_id, spotify_ids)
        req = urllib.request.Request(url)
        # req = urllib.request.Request(url, "".encode('UTF-8'))
        req.add_header("Accept", "application/json")
        req.add_header("Authorization", OAUTH_TOKEN)
        req.get_method = lambda: 'POST'
        urllib.request.urlopen(req)


class Song(object):
    def __init__(self):
        self._artist = ""
        self._track = ""
        self._spotify_id = ""
        self._pattern = re.compile('(.*)[-](.*)|(.*) by (.*)')


    @property
    def artist(self):
        return self._artist


    @artist.setter
    def artist(self, s):
        self._artist = s


    @property
    def track(self):
        return self._track


    @track.setter
    def track(self,s):
        self._track = s


    @property
    def spotify_id(self):
        return self._spotify_id


    @spotify_id.setter
    def spotify_id(self, s):
        self._spotify_id = s


    def run(self, s):
        result = re.search(self._pattern,s)
        result = result.string
        if '-' in result:
            result = result.split('-')
        elif ' by ' in result:
            result = result.split(' by ')
        self._track = result[0].lstrip().rstrip().replace(' ','+')
        self._artist = result[1].rstrip().lstrip().lower()


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



def main():
    # playlist goes here
    account = 'foo'
    playlist_name = 'bar'
    p = Playlist(account, playlist_name)
    s = Song()
    tracks = []
    open ('songs.txt', "r") as f:
        for line in f:
            s.run(line)
            s.get_spotify_id()
            tracks.append(s._spotify_id)
    tracks = ','.join(tracks)
    p.add_tracks(tracks)


if '__name__' == '__main__':
    main()
