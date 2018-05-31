import asyncio
import argparse

from urllib.request import urlopen

from libs.client import TCPclient

def get_seed():
    github_repo = "https://raw.githubusercontent.com/Devilmoon/grambooster/master/seed"
    with urlopen(github_repo) as response:
        seed = response.read().decode('utf-8')
        print("seed is:", seed)
        seed = "151.30.68.43"
        return seed

def start(username, password):
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: TCPclient(loop, username, password), get_seed(), 3338)
    _, proto = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing connection')
    loop.close()



#if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Test instagram_private_api.py')
    #parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    #parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    #args = parser.parse_args()

    #loop = asyncio.get_event_loop()
    #coro = loop.create_connection(lambda: TCPclient(loop, args.username, args.password), get_seed(), 3338)
    #_, proto = loop.run_until_complete(coro)

    #try:
    #    loop.run_forever()
    #except KeyboardInterrupt:
    #    print('Closing connection')
    #loop.close()