from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from .models import SpotifyUser, RecentCrews
import requests
import os
import uuid
import json
import datetime as dt
import pytz
import base64

# def index(request):
#     return render(request, 'spotcontrol/index.html', {})


class Index(TemplateView):
    template_name = 'spotcontrol/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def room(request, crew_id=None):
    print(
        f'crew_id = {crew_id}'
    )
    # currentUser = SpotifyUser.objects.get(id=request.user.id)
    # crewExistsInHistory = crew_id in [x.crew_id for x in currentUser.most_recent_crews.all()]

    # if crewExistsInHistory:
    #     crew = currentUser.most_recent_crews.get(crew_id=crew_id)
    #     crew.last_active_date = dt.datetime.now()
    # else:
    #     if crew_id is None:
    #         crew_id = uuid.uuid4()
    #     crew = RecentCrews(crew_id=crew_id)
    # crew.save()

    # currentUser.most_recent_crews.add(crew)
    # currentUser.save()

    return render(request, 'spotcontrol/room.html', {
      'room_name': crew_id,
    })


def connect_spotify(request):
    base = 'https://accounts.spotify.com/authorize'
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    response_type = 'code'
    # redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
    redirect_uri = f'https://{settings.CURRENT_NGROK}/redir_uri/'
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

def check_if_auth_expired(request, timezone='America/Los_Angeles'):
    expires_in = SpotifyUser.objects.get(username=request.user).expires_in
    curr_tz = pytz.timezone(timezone)
    curr_date = dt.datetime.now(tz=curr_tz)
    return curr_date > expires_in

def auth_spotify(request):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)

    endpoint = 'https://accounts.spotify.com/api/token'
    grant_type = 'authorization_code'
    # redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
    redirect_uri = f'https://{settings.CURRENT_NGROK}/redir_uri/'
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

    print(f'r_result: {r_result}')

    if r_result != 200:
        return redirect('spot_auth_result', authresult='fail')
    else:
        return redirect('spot_auth_result', authresult='success')

def refresh_spotify(request):
    if request.method != 'POST':
        print("Request FORBIDDEN.")
        return HttpResponseForbidden()

    endpoint = 'https://accounts.spotify.com/api/token'
    grant_type = 'refresh_token'
    refresh_token = SpotifyUser.objects.get(username=request.user).refresh_token
    print(f'REFRESH: {refresh_token}')
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
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
    expires_in = response_json.get('expires_in')
    
    spotifyUser = SpotifyUser.objects.get(username=request.user)
    spotifyUser.auth_token = access_token
    spotifyUser.expires_in = dt.datetime.now() + dt.timedelta(seconds=expires_in)
    print(f'new access token: {access_token}')
    spotifyUser.save()

    if response.status_code != 200:
        return HttpResponse('FAIL')
    else:
        return HttpResponse('SUCCESS')

    return HttpResponse(response.text)


@login_required
def get_auth_token(request):
    if check_if_auth_expired(request):
        refresh_spotify(request)

    spotifyUser = SpotifyUser.objects.get(username=request.user)
    payload = {
        'Data': {
            'token': spotifyUser.auth_token
        }
    }
    return HttpResponse(json.dumps(payload))


def log_playback_device(request):
    if request.method != 'POST':
        return HttpResponseForbidden()

    if check_if_auth_expired(request):
        refresh_spotify(request)

    endpoint = 'https://api.spotify.com/v1/me/player/devices'
    spotifyUser = SpotifyUser.objects.get(username=request.user)
    auth_token = spotifyUser.auth_token
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = requests.get(endpoint, headers=headers)
    response = json.loads(response.text)
    print(response)
    device_id = None
    numDevices = len(response['devices'])
    if numDevices > 1:
        for res in response['devices']:
            if res['is_active']:
                device_id = res['id']
    elif numDevices == 1:
        device_id = response['devices'][0]['id']

    if device_id is not None:
        spotifyUser.most_recent_device = device_id
        spotifyUser.save()
    
    # device_id = device_id.get('devices', None)[0]['id']
    print(f'MOST RECENT DEVICE: {device_id}')
    return HttpResponse(device_id)

def encodeIdAndSecret(client_id, client_secret):
    ids = client_id + ':' + client_secret
    ids = ids.encode()
    ids = base64.b64encode(ids).decode('ascii')
    return ids

def populateSpotifyAuthParams(request, postResponse, timezone='America/Los_Angeles'):
    response_json = json.loads(postResponse.text)
    print(f'response_json: {response_json}')
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
        # print(f'context: {context}')
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

def test(request):
    user = request.user
    spotExists = SpotifyUser.objects.filter(username=user)
    if len(spotExists) > 0:
        auth_token = spotExists[0].auth_token

        print(
            f'RUNNING TEST ENDPOINT.\n'
            f'USER: {request.user}\n'
            f'AUTH_TOKEN: {auth_token}'
            )
    return HttpResponse(200)