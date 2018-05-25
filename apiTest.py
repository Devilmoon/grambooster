from instagram_private_api import Client

user_name = '#########'
password = '##########'

api = Client(user_name, password)
seen = []
results = api.feed_timeline()
for i in range(len(results["feed_items"])):
    try:
        print(results["feed_items"][i]["media_or_ad"]["id"])
        seen.append(results["feed_items"][i]["media_or_ad"]["id"].split("_")[0])
    except:
        pass



print(seen)
try:
    api.post_like(seen[0], "feed_timeline")
except e:
    print(e)