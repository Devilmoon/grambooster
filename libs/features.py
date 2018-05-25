import json

def like_picture(api, media_id):
    res = api.post_like(media_id, 'photo_view')
    return res

def process_data(api, data):
    data = json.loads(data)
    pics = data.get("pics", "")
    if not pics:
        print("no pics received:", data)
        return
    print("i'm going to like this pic:", pics[0])
    res = like_picture(api, pics[0])
    print("result:", res)

seenMine=['']
def get_my_feed(api, username):
    own = api.self_feed()
    for i in range(len(own["items"])):
        id_pic = own["items"][i]["id"].split("_")[0]
        print("last pic:", id_pic)
        if id_pic != seenMine[0]:
            seenMine[0] = id_pic
            message = json.dumps({'who': username, 'pics': [seenMine[0]]})
            return message
        break