import playlist
import user
import praw
import re
import requests
import simplejson as json
from fuzzywuzzy import fuzz
from functools import partial
import sys
import multiprocessing
import math


def get_spotify_id(t):
    artist = t[0]
    track = t[1]
    url = "https://api.spotify.com/v1/search?q=%s+artist:%s&type=track&market=US&" % (track, artist)
    r = requests.get(url)
    data = json.loads(r.text)
    if 'tracks' in data:
        for i in range(0, len(data["tracks"]["items"])):
            if fuzz.ratio(artist, data["tracks"]["items"][i]["artists"][0]["name"].lower()) > 60:
                if fuzz.ratio(track, data["tracks"]["items"][i]["name"].lower()) >= 60:
                    s_id = data["tracks"]["items"][i]["uri"]
                    return s_id
    raise ValueError('track not found')
    

def fetch_comments(uid, client_id, client_secret):
    res = []
    r = praw.Reddit(user_agent = 'portify by /u/doveward',
                    client_id = client_id,
                    client_secret = client_secret)
    r.read_only = True
    submission = r.submission(id=uid)
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        matches = regex_match(comment.body.splitlines())
        for match in matches:
            res.append(match.groups())
    return res


def regex_match(lis):
    res = [re.sub(r'(\(http.*\))', '', str(x)) for x in lis]
    res = [re.sub(r'(?!-|\s|,)\W','', str(x)) for x in res]
    res = [re.match(r'(?!\[|\])(.*)?\s*(?:-|by)\s*((?:\b\w*\s?)+)', str(x)) for x in res]
    res = filter(None, res)
    return res


def string_strip(s):
    return s.rstrip().lstrip().lower().replace(' ','+')


def song_helper(artist, song, q):
    a = string_strip(artist)
    s = string_strip(song)
    try:
        uri = get_spotify_id((a, s))
        q.put(uri)
    except ValueError:
        try:
            uri = get_spotify_id((s, a))
            q.put(uri)
        except:
            pass
    

def parse(q, lis):
    for res in lis:
        if len(res[0]) > 40 or len(res[1]) > 40:
            together = ''.join(res).split('-')
            j = regex_match(together)
            for k in j:
                n = k.groups()
                song_helper(n[0], n[1], q)
        song_helper(res[0], res[1], q)


def counter(i):
    yield i+1


def chunker(a, j):
    i = len(a)
    high = math.ceil(i/j)
    res = [a[x:x+high] for x in range(0, i, high)]
    return res


def mt(thread_id, playlist_name):
    POOL_SIZE = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=POOL_SIZE)
    manager = multiprocessing.Manager()
    q = manager.Queue()
    u = user.User()
    p = playlist.Playlist(u.username, playlist_name, u.token)
    a = fetch_comments(thread_id, u.client_id , u.client_secret)
    mapfunc = partial(parse, q)
    chunks = chunker(a, POOL_SIZE)
    pool.map(mapfunc, [x for x in chunks])
    q.put('STOP')
    c = 0
    d = dict()
    for i in iter(q.get, 'STOP'):
        if i in d:
            pass
        else:
            d[i] = c
            c = next(counter(c))

    pool.close()
    pool.terminate()
    pool.join()
    upload(list(d.keys()), p)


def upload(tracks, p):
    tracks = chunker(tracks, math.ceil(len(tracks)/100))
    for track in tracks:
       res = {} 
       res['uris'] = track
       res = json.dumps(res)
       p.add_tracks(res)


def main():
    x = sys.argv[1]
    if sys.argv[2]:
        pl = sys.argv[2]
    else:
        pl = x
    mt(x, pl)

if __name__ == "__main__":
    main()
