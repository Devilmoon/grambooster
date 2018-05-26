import json

def like_picture(api, media_id):
    """Like a picture given its id

    Args:
        api: an Instagram API instance
        media_id: a picture's ID, taken from Instagram's backend
    
    Returns:
        Instagram's reply to our action
    """
    res = api.post_like(media_id, 'photo_view')
    return res

def process_data(api, data, username, cache):
    """process a message received by a peer

    This function processes a message received by a peer.
    It will either decide to like the picture referenced
    in said message or skip the action since the picture 
    had already been cached or is his own.

    Args:
        api: an Instagram API instance
        data: the message in JSON format
        username: your own username
        cache: the path to a cache file
    
    Returns:
        Nothing
    """
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
    """Check your own user feed for new pics

    This function checks if you have a new picture
    uploaded on Instagram, and if so broadcasts
    the ID to all peers in order to get it liked
    by the network.

    Args:
        api: an Instagram API instance
        username: your Instagram username
        cache: path to a cache file
    
    Returns:
        Message formatted and serialised in JSON
        ready to be sent to peers if we have uploaded
        a new pic since last check, nothing otherwise
    """
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
    """deserialize and return cache

    This function will load our JSON-like
    cache a return it as a Python dictionary

    Args:
        cache: the path to a cache file
    
    Returns:
        deserialized cache as Python dictionary

    Raises:
        Exception: if the file doesn't exist or
            is empty we write a fresh cache in it
            and call the function again.
    """
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
    """update cache

    This function will update our cache 
    if the picture inside the message received 
    had never been seen before.
    If there is any problem with the cache file 
    it will just overwrite it with a fresh cache.

    Args:
        cache: the path to a cache file
        message: a serialized message containing
            a pic to like
    
    Returns:
        Nothing
    """
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
    """check if a picture is in cache

    This function checks wether or not a
    given picture is in our cache or not.

    TODO: implement in update_history

    Args:
        cache: the path to a cache file
        message: a serialised message containing
            a pic
    
    Returns:
        True or False 
    """
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

