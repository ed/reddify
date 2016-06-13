import re
import urllib.request
import simplejson
from collections import namedtuple

class Playlist(object):
    def __init__(self, account_name, playlist, token):
        self._playlist_name = playlist
        self._playlist_id = ""
        self._account_name = account_name
        self._token = token
        self._song_list = []


    def create_playlist(self, playlist_name):
        url = "https://api.spotify.com/v1/users/%s/playlists" % (self._account_name)
        data = "{\"name\":\"%s\",\"public\":false}" % (playlist_name)
        bytes = data.encode('UTF-8')
        req = urllib.request.Request(url, bytes)
        req.add_header("Accept", "application/json")
        req.add_header("Authorization", self._token)
        req.add_header("Content-Type", "application/json")
        urllib.request.urlopen(req)


    def get_playlist_id(self):
        url = "https://api.spotify.com/v1/users/%s/playlists" % (self._account_name)
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("Authorization", self._token)
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
        req.add_header("Authorization", self._token)
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
        req.add_header("Authorization", self._token)
        req.get_method = lambda: 'POST'
        urllib.request.urlopen(req)

