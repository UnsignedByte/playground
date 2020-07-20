# -*- coding: utf-8 -*-
# @Author: UnsignedByte
# @Date:   01:38:51, 20-Jul-2020
# @Last Modified by:   UnsignedByte
# @Last Modified time: 01:44:57, 20-Jul-2020

# for crafting things

from pynput import keyboard, mouse;

mc = mouse.Controller();

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()