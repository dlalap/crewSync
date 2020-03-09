import requests
import os
import uuid

base = 'https://accounts.spotify.com/authorize'
client_id = os.getenv('SPOTIPY_CLIENT_ID')
response_type = 'code'
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
state = uuid.uuid4()
scope = '''\
    user-modify-playback-state \
    user-read-playback-state \
    user-read-currently-playing \
    user-library-read \
    playlist-read-private \
    playlist-modify-public \
    playlist-modify-private \
    playlist-read-collaborative \
    app-remote-control \
    streaming \
    '''

# scope = 'streaming'

req = ( 
    f'{base}?client_id={client_id}'
    f'&response_type={response_type}'
    f'&redirect_uri={redirect_uri}'
    f'&scope={scope}'
    f'&state={state}'
)

res = requests.get(
    req
)

print(res)