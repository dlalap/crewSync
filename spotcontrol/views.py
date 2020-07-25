from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.auth.models import AnonymousUser
from .models import SpotifyUser
import requests
import os
import uuid
import json
import datetime as dt
import pytz
import base64

def index(request):
    return render(request, 'spotcontrol/index.html', {})


def room(request, room_name):
    return render(request, 'spotcontrol/room.html', {
      'room_name': room_name
    })


def connect_spotify(request):
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
    req = ( 
        f'{base}?client_id={client_id}'
        f'&response_type={response_type}'
        f'&redirect_uri={redirect_uri}'
        f'&scope={scope}'
        f'&state={state}'
    )
    return redirect(req)

def auth_spotify(request):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)

    endpoint = 'https://accounts.spotify.com/api/token'
    grant_type = 'authorization_code'
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    contentType = "application/x-www-form-urlencoded"

    ids = encodeIdAndSecret(client_id, client_secret)


    data = (
        # f'client_id={client_id}'
        # f'&client_secret={client_secret}'
        f'&grant_type={grant_type}'
        f'&code={code}'
        f'&redirect_uri={redirect_uri}'
    )

    headers = {
        'content-type': contentType,
        'Authorization': f'Basic {ids}'
    }

    print(data)

    response = requests.post(endpoint, data=data, headers=headers)

    r_result = populateSpotifyAuthParams(request, response)

    if r_result != 200:
        return redirect('spot_auth_result', authresult='fail')
    else:
        return redirect('spot_auth_result', authresult='success')

def refresh_spotify(request):
    endpoint = 'https://accounts.spotify.com/api/token'
    grant_type = 'refresh_token'
    refresh_token = SpotifyUser.objects.get(username=request.user).refresh_token
    print(f'REFRESH: {refresh_token}')
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    # ids = client_id + ':' + client_secret
    # ids = ids.encode()
    # ids = base64.b64encode(ids).decode('ascii')
    ids = encodeIdAndSecret(client_id, client_secret)
    contentType = "application/x-www-form-urlencoded"

    data = {
        'grant_type': grant_type,
        'refresh_token': refresh_token,
    }

    headers = {
        'content-type': contentType,
        'Authorization': f'Basic {ids}'
    }

    response = requests.post(endpoint, data=data, headers=headers)

    response_json = json.loads(response.text)
    access_token = response_json.get('access_token')
    
    # print('access_token: ' + access_token)
    spotifyUser = SpotifyUser.objects.get(username=request.user)
    spotifyUser.access_token = access_token
    print('new access token: ' + access_token)
    spotifyUser.save()

    return HttpResponse(response.text)

def encodeIdAndSecret(client_id, client_secret):
    ids = client_id + ':' + client_secret
    ids = ids.encode()
    ids = base64.b64encode(ids).decode('ascii')
    return ids

def populateSpotifyAuthParams(request, postResponse, timezone='America/Los_Angeles'):
    response_json = json.loads(postResponse.text)
    if 'error' in response_json:
        return 400

    access_token = response_json.get('access_token', None)
    token_type = response_json.get('token_type', None)
    expires_in = response_json.get('expires_in', None)
    refresh_token = response_json.get('refresh_token', None)

    current_user = request.user
    curr_tz = pytz.timezone(timezone)

    spotifyUserKwargs = {
        'username': current_user,
        'auth_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': dt.datetime.now(tz=curr_tz) + dt.timedelta(seconds=3600)
    }

    spotifyUserExists = SpotifyUser.objects.filter(username=current_user)
    if len(spotifyUserExists) == 0:
        print('spotify user does not exist')
        SpotifyUser.objects.create(
            **spotifyUserKwargs
        )
    else:
        print('spotify user exists')
        newTime = dt.datetime.now(tz=curr_tz) + dt.timedelta(seconds=3600)
        selectedObject = spotifyUserExists[0]
        selectedObject.__dict__.update(spotifyUserKwargs)
        selectedObject.save()
    return 200

class MainPage(TemplateView):
    template_name = "index.html"

    # spotData = getSpotifyData(self.request)
    def get_context_data(self, **args):
        context = super().get_context_data(**args)
        context['token'] = getSpotifyData(self.request)
        print(f'context: {context}')
        return context


def getSpotifyData(request):
    if request.user.is_authenticated:
        spotifyExists = SpotifyUser.objects.filter(username=request.user)
        if len(spotifyExists) == 0:
            return "0"
        else:
            auth_token = spotifyExists[0].auth_token
        return auth_token
    else:
        return "-1"


class AuthResult(TemplateView):
    template_name = 'auth/auth_success_or_fail.html'

    def get_context_data(self, **args):
        context = super().get_context_data(**args)
        return context
