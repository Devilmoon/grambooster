import os
import json
import codecs

from instagram_private_api import Client


def get_api(username, password, settings_file_path="saved_auth.json"):
    api = None
    cached_auth = load_auth(settings_file_path)
    if cached_auth:
        print("found cached auth..")
        api = login_with_cache(username, password, cached_auth)
    else:
        print("fresh login..")
        api = fresh_login(username, password)
        store_auth(api.settings)
    print("api acquired!")
    return api

def load_auth(cached_file):
    if cached_file and os.path.isfile(cached_file):
        with open(cached_file) as file_data:
            cached_auth = json.load(file_data, object_hook=from_json)
            return cached_auth
    else:
        return None

def fresh_login(username, password):
    try:
        api = Client(username, password, auto_patch=True)
        return api
    except ClientLoginError:
        print('Login Error. Please check your username and password.')
        sys.exit(99)

def login_with_cache(username, password, cached_auth):
    try:
        api = Client(username, password, auto_patch=True, settings=cached_auth)
        return api
    except ClientCookieExpiredError:
        print('Cookie Expired. Please discard cached auth and login again.')
        sys.exit(99)

def store_auth(cached_auth, settings_file_path="saved_auth.json"):
    # this auth cache can be re-used for up to 90 days
    with open(settings_file_path, 'w') as outfile:
        json.dump(cached_auth, outfile, default=to_json)

def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object