# import playlist
# import songs
import praw
from collections import namedtuple
import re
import urllib.request
import simplejson as json
from operator import itemgetter
from fuzzywuzzy import fuzz
import time
# import codecs

# v0.01

# API STUFF
# TOKEN GOES HERE
# REQUEST ONE AT SPOTIFY WEB API
# https://developer.spotify.com/web-api/console/get-several-albums/


# if want to go fuzzy string match database route
# def set_database(path):
#     f = codecs.open(path, 'r', 'utf-8')
#     choices = f.readlines()
#     return choices
#

results = []

def regex_match(i):
    global results
    SongTuple = namedtuple('SongTuple', 'artist title')
    for x in i.splitlines():
        try:
            x = re.sub(r'(\(http.*\))', '', str(x))
            x = re.sub(r'(?!-|\s|,)\W','', str(x))
            result = re.match(r'(?!\[|\])(.*)?\s*-\s*((?:\b\w*\s?)+)',str(x)).groups()
            artist = result[0].rstrip().lstrip().lower().replace(' ','+')
            title = result[1].lstrip().rstrip().lower().replace(' ','+')
            try:
                results.append(get_spotify_id(SongTuple(artist,title)))
            except ValueError:
                try:
                    artist = result[1].rstrip().lstrip().lower().replace(' ','+')
                    title = result[0].lstrip().rstrip().lower().replace(' ','+')
                    results.append(get_spotify_id(SongTuple(artist,title)))
                except ValueError:
                    pass
        except:
            pass


def thread_parser(uid):
    r = praw.Reddit('user-agent')
    if len(uid) < 10:
        submission = r.get_submission(submission_id=uid)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        already_done = set()
        for comment in flat_comments:
            if comment.id not in already_done:
                try:
                    regex_match(str(comment.body))
                except:
                    pass
                already_done.add(comment.id)
    return results



def file_parser(path):
    results = []
    SongTuple = namedtuple('SongTuple', 'artist title')
    with open(path, "r") as f:
        for line in f:
            try:
                result = re.match('(.*)-(.*)',str(comment)).groups()
                artist = result[0].rstrip().lstrip().lower()
                title = result[1].lstrip().rstrip().replace(' ','+')
                results.append(SongTuple(artist,title))
            except:
                pass
    return results


def get_spotify_id(t):
    artist = t[0]
    track = t[1]
    url ="https://api.spotify.com/v1/search?q=%s+artist:%s&type=track&market=US&" % (track, artist)
    r = urllib.request.urlopen(url)
    data = json.load(r)
    PopId = namedtuple('PopId', 'pop spotify_id')
    popid_list = []
    for i in range(0, len(data["tracks"]["items"])):
        if fuzz.ratio(artist, data["tracks"]["items"][i]["artists"][0]["name"].lower()) > 60:
            if fuzz.ratio(track, data["tracks"]["items"][i]["name"].lower()) >= 60:
                s_id = data["tracks"]["items"][i]["id"]
                return s_id
    raise ValueError('track not found')

def print_playlist(a):
    Song = namedtuple('Song', 'artist title')
    songlist = []
    for i in a:
        try:
            url ="https://api.spotify.com/v1/tracks/%s" % (i)
            r = urllib.request.urlopen(url)
            data = json.load(r)
            print(Song(data["artists"][0]["name"], data["name"]))
        except:
            pass

def other_test():
    r = praw.Reddit('user-agent')
    submission = r.get_submission(url='https://www.reddit.com/r/indieheads/comments/4nuqcn/my_best_friend_was_murdered_in_the_orlando/d47eray')
    s = submission.comments[0]
    result = regex_match(s.body)



def test():
    songlist = []
    thread_parser('4nuqcn')
    print_playlist(results)

# def main():
#     # playlist goes here
#     scopes = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'
#     account = 'foo'
#     playlist_name = 'bar'
#     token = "Bearer " + OAUTH_TOKEN
#     p = Playlist(account, playlist_name, token)
#     tracks = []
#     tracks = ','.join(tracks)
#     p.add_tracks(tracks)


if __name__ == '__main__':
    # other_test()
    test()
    # regex_test()
    # main()
