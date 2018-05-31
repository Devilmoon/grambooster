import toga
import subprocess
import main

import threading


import asyncio
import argparse

from urllib.request import urlopen

from libs.client import TCPclient

THREAD = None
loop = asyncio.get_event_loop()


def get_seed():
    github_repo = "https://raw.githubusercontent.com/Devilmoon/grambooster/master/seed"
    with urlopen(github_repo) as response:
        seed = response.read().decode('utf-8')
        print("seed is:", seed)
        seed = "151.30.68.43"
        return seed

def start(username, password):
    coro = loop.create_connection(lambda: TCPclient(loop, username, password), get_seed(), 3338)
    _, proto = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing connection')
    loop.close()

def build(app):
    c_box = toga.Box()
    f_box = toga.Box()
    box = toga.Box()

    c_input = toga.TextInput()
    f_input = toga.TextInput()

    c_label = toga.Label('Password', alignment=toga.RIGHT_ALIGNED)
    f_label = toga.Label('Username', alignment=toga.RIGHT_ALIGNED)

    def login(widget):
        t = threading.Thread(target = start, args = (f_input.value, c_input.value))
        t.daemon=True
        t.start()
        THREAD = t
        

    button = toga.Button('Start gaining likes!', on_press=login)

    f_box.add(f_input)
    f_box.add(f_label)

    c_box.add(c_input)
    c_box.add(c_label)

    box.add(f_box)
    box.add(c_box)
    box.add(button)

    box.style.set(flex_direction='column', padding_top=10)
    f_box.style.set(flex_direction='row', margin=5)
    c_box.style.set(flex_direction='row', margin=5)

    c_input.style.set(flex=1, margin_left=160)
    f_input.style.set(flex=1, margin_left=160)
    c_label.style.set(width=100, margin_left=10)
    f_label.style.set(width=100, margin_left=10)

    button.style.set(margin=15)

    return box

def main():
    return toga.App('GramBooster', 'com.grambooster', startup=build)

if __name__ == '__main__':
    main().main_loop()
    print("cal")