import os
import json

from insta_auth import get_api

username = 'calogero.mandracchia'
password = 'forzalazio'

media_id = '1776226418134789884'

settings_file_path = "saved_auth.json"

api = get_api(username, password, settings_file_path)
print("api acquired!")

def like_picture(api, media_id):
    res = api.post_like(media_id, 'photo_view')
    return res

like_picture(api, media_id)