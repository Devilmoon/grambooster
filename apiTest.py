from instagram_private_api import Client

user_name = '######'
password = '#####'

api = Client(user_name, password)

#Get first 10 pics from global feed
seen = []
results = api.feed_timeline()
for i in range(len(results["feed_items"])):
    try:
        print(results["feed_items"][i]["media_or_ad"]["id"])
        seen.append(results["feed_items"][i]["media_or_ad"]["id"].split("_")[0])
    except:
        pass



print(seen)
#like first pic seen
"""
try:
    api.post_like(seen[0], "feed_timeline")
except e:
    print(e)
"""

#get latest 10 pics from authenticated user
seenMine=[]
own = api.self_feed()
for i in range(len(own["items"])):
    try:
        print(own["items"][i]["id"])
        seenMine.append(own["items"][i]["id"].split("_")[0])
    except:
        pass


#like latest pic
try:
    api.post_like(seenMine[0], "feed_timeline")
except e:
    print(e)
