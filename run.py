# import playlist
# import songs
import praw
from collections import namedtuple
import re
import urllib.request
import simplejson as json
from operator import itemgetter
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

def regex_match(s):
    result = re.match(r'(.*)-(.*)',str(s)).groups()
    artist = result[0].rstrip().lstrip().lower()
    title = result[1].lstrip().rstrip().replace(' ','+')
    return artist, title


def thread_parser(uid):
    results = []
    SongTuple = namedtuple('SongTuple', 'artist title')
    if len(uid) < 10:
        uid = "'%s'"%uid
        utype = 'submission_id='
    else:
        utype=''
    r = praw.Reddit('user-agent')
    submission = r.get_submission(utype+uid)
    if utype == '':
        comment = submission.comments[0]
        try:
            artist, title = regex_match(str(comment))
            results.append(SongTuple(artist,title))
        except:
            pass
    else:
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        already_done = set()
        for comment in flat_comments:
            if comment.id not in already_done:
                try:
                    artist,title = regex_match(str(comment))
                    results.append(SongTuple(artist,title))
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
    url ="https://api.spotify.com/v1/search?q=%s&type=track&market=US" % (track)
    r = urllib.request.urlopen(url)
    data = json.load(r)
    PopId = namedtuple('PopId', 'pop spotify_id')
    popid_list = []
    for i in range(0, len(data["tracks"]["items"])):
        if data["tracks"]["items"][i]["artists"][0]['name'].lower() == artist:
            popid_list.append(PopId(data["tracks"]["items"][i]["popularity"], data["tracks"]["items"][i]["uri"]))
    return max(popid_list,key=itemgetter(0))[1]


def test():
    songlist = []
    # results = thread_parser('https://www.reddit.com/r/indieheads/comments/4nuqcn/my_best_friend_was_murdered_in_the_orlando/d4736ss')
    results = thread_parser('4nuqcn')
    for result in results:
         songlist.append(get_spotify_id(result))
    print(songlist)

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
    test()
    # main()
