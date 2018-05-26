import json

def like_picture(api, media_id):
    res = api.post_like(media_id, 'photo_view')
    return res

def process_data(api, data, username, cache):
    if pic_in_cache(cache, data):
        print("pic already in cache")
        return
    data = json.loads(data)
    pics = data.get("pics", "")
    if not pics:
        print("no pics received:", data)
        return
    who = data.get("who", "")
    if who!= username:
        print("i'm going to like this pic:", pics[0])
        res = like_picture(api, pics[0])
        print("result:", res)
        return
    else:
        print("That's my pic! Not liking it")
        return

seenMine=['']
def get_my_feed(api, username, cache):
    own = api.self_feed()
    for i in range(len(own["items"])):
        id_pic = own["items"][i]["id"].split("_")[0]
        print("last pic:", id_pic)
        if id_pic != seenMine[0]:
            seenMine[0] = id_pic
            message = json.dumps({'who': username, 'pics': [seenMine[0]]})
            update_history(cache, message)
            #get_history(cache)
            return message
        break

def get_history(cache):
    try:
        with open(cache, "r") as c:
            blob = c.read()
            if blob=="":
                raise Exception
            history = json.loads(blob)
            return history
    except Exception as e:
        with open(cache, "w+") as c:
            c.write('{"seen":[]}')
        return get_history(cache)

def update_history(cache, message):
    messageL = json.loads(message)
    history = get_history(cache)
    updated = False
    for i in range(len(history.get("seen"))):
        #if user is already cached
        if history.get("seen")[i].get("who") == messageL.get("who"):
            #if pic has never been seen
            if messageL.get("pics")[0] not in history["seen"][i]["pics"]:
                history["seen"][i]["pics"].append(messageL.get("pics")[0])
                print("new pic")
                updated = True
                break
            else:
                #pic has already been seen
                print("pic already seen")
                updated = True
                break
    #user never cached            
    if not updated:
        print("new user")
        history["seen"].append(messageL)
    try:
        with open(cache, "w+") as c:
            c.write(json.dumps(history))
        return
    except:
        with open(cache, "w+") as c:
            c.write("{'seen':[]}")
        return

def pic_in_cache(cache, message):
    history = get_history(cache)
    messageL = json.loads(message)
    for i in range(len(history.get("seen"))):
        #if user is already cached
        if history.get("seen")[i].get("who") == messageL.get("who"):
            #if pic has never been seen
            if messageL.get("pics")[0] not in history["seen"][i]["pics"]:
                return False
            else:
                #pic has already been seen
                return True
    return False

