import re
import requests
import simplejson as json

class Playlist(object):
    def __init__(self, account_name, playlist, token):
        self._playlist_name = playlist
        self._playlist_id = ""
        self._account_name = account_name
        self._token = token
        self.create_playlist()


    def create_playlist(self):
        url = "https://api.spotify.com/v1/users/%s/playlists" % (self._account_name)
        headers = {'Accept' : 'application/json', 'Authorization' : self._token, 'Content-Type' : "application/json"}
        data = "{\"name\":\"%s\",\"public\":true}" % (self._playlist_name)
        data = data.encode('UTF-8')
        r = requests.post(url, headers=headers, data=data)
        self.get_playlist_id()


    def get_playlist_id(self):
        url = "https://api.spotify.com/v1/users/%s/playlists" % (self._account_name)
        headers = {'Accept' : 'application/json', 'Authorization' : self._token}
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)
        for i in range(0, len(data['items'])):
            if data['items'][i]['name'] == self._playlist_name:
                self._playlist_id = data['items'][i]['id']


    def add_tracks(self, spotify_ids):
        url = "https://api.spotify.com/v1/users/%s/playlists/%s/tracks?" % (self._account_name, self._playlist_id)
        headers = {'Accept' : 'application/json', 'Authorization' : self._token}
        r = requests.post(url, headers=headers, data=spotify_ids)
