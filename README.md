# portify

## installation:
python3 setup.py install  

## configuration:
### username  
open up "config":  
username = "spotify username goes here"  
### token
https://developer.spotify.com/web-api/console/post-playlists/  
fill out your username and click "get oauth token"  
check playlist-modify-public and playlist-modify-private  
token = 
### client_id and client_secret
https://www.reddit.com/prefs/apps
click create an app
name it portify or whatever  
check script  
redirect_url use https://localhost:8080  
client_id =  
client_secret = 
## run:
python3 run.py "reddit thread id" "your name for playlist"
