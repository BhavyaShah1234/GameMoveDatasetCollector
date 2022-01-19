import cv2 as cv
import pandas as pd
import numpy as np
import keyboard as kb
import win32gui
import win32ui
import win32.lib.win32con as win32con
import os


def capture_window(window, a, b, w, h):
    hwnd = win32gui.FindWindow(None, window)
    # hwnd = None
    wdc = win32gui.GetWindowDC(hwnd)
    dc_obj = win32ui.CreateDCFromHandle(wdc)
    cdc = dc_obj.CreateCompatibleDC()
    data_bitmap = win32ui.CreateBitmap()
    data_bitmap.CreateCompatibleBitmap(dc_obj, w, h)
    cdc.SelectObject(data_bitmap)
    cdc.BitBlt((0, 0), (w, h), dc_obj, (a, b), win32con.SRCCOPY)
    signed_int_array = data_bitmap.GetBitmapBits(True)
    image = np.frombuffer(signed_int_array, dtype='uint8')
    image.shape = (h, w, 4)
    image = image[..., :3]
    image = np.ascontiguousarray(image)
    dc_obj.DeleteDC()
    cdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, wdc)
    win32gui.DeleteObject(data_bitmap.GetHandle())
    return image


# THESE VALUES ARE FOR DINO GAME(CHROME) ON https://chromedino.com/. TEST WITH DIFFERENT VALUES FOR DIFFERENT GAMES
x, y = 350, 200
width, height = 900, 200
window_name = 'T-Rex Dinosaur Game - Chrome Dino Runner Online - Google Chrome'

frame_key_dict = {'frame': [], 'move': []}
counter = 0
key = None
os.mkdir('images')
while True:
    frame = capture_window(window_name, x, y, width, height)
    filename = f'images/img_{counter}.jpg'
    cv.imwrite(filename, frame)
    key = kb.read_key()
    if kb.is_pressed(key):
        kb.on_release_key(key, lambda _: _)
        if key == 'esc':
            break
    else:
        key = None
    frame_key_dict['frame'].append(filename)
    frame_key_dict['move'].append(key)
    counter = counter + 1
    # UNCOMMENT THESE 2 LINES BELOW TO VIEW WINDOW AND TEST VALUES OF x, y, width, height AND window_name
    # cv.imshow('FRAME', frame)
    # cv.waitKey(1)

df = pd.DataFrame(frame_key_dict)
df.to_csv('images/dataframe.csv')
