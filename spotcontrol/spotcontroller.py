import requests
import datetime as dt


def sendSpotControl(control, auth):

    control = control.lower()

    zero = 'https://api.spotify.com/v1/me/player/seek?position_ms=0'
    base = 'https://api.spotify.com/v1/me/player/'
    ## switcher = {
    ##     'play': ('PUT', 'play'),
    ##     'pause': ('PUT', 'pause'),
    ##     'prev': ('POST', 'previous'),
    ##     'next': ('POST', 'next')
    ## }
    print({
            'base': base + control,
            'auth': auth,
        })

    header = {
        'Authorization': 'Bearer ' + auth
    }

    if control in ['play', 'pause']:
        print(f'Pressed {control}')
        if control == 'play':
            requests.put(zero, headers=header)
        return requests.put(base + control, headers=header)

    elif control in ['previous', 'next', 'seek']:
        print(f'Pressed {control}')
        return requests.post(base + control, headers=header)