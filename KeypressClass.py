import cv2 as cv
import pandas as pd
import numpy as np
import keyboard as kb
import win32gui
import win32ui
import win32.lib.win32con as win32con
import os


class Capture:
    def __init__(self, window_name, x, y, window_width, window_height, folder, show):
        self.window_name = window_name
        self.x = x
        self.y = y
        self.window_width = window_width
        self.window_height = window_height
        self.folder = folder
        self.frame_key_dict = {'frame': [], 'move': []}
        self.counter = 0
        self.key = None
        self.show = show
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)

    def capture_window(self):
        hwnd = win32gui.FindWindow(None, self.window_name)
        # hwnd = None
        wdc = win32gui.GetWindowDC(hwnd)
        dc_obj = win32ui.CreateDCFromHandle(wdc)
        cdc = dc_obj.CreateCompatibleDC()
        data_bitmap = win32ui.CreateBitmap()
        data_bitmap.CreateCompatibleBitmap(dc_obj, self.window_width, self.window_height)
        cdc.SelectObject(data_bitmap)
        cdc.BitBlt((0, 0), (self.window_width, self.window_height), dc_obj, (self.x, self.y), win32con.SRCCOPY)
        signed_int_array = data_bitmap.GetBitmapBits(True)
        image = np.frombuffer(signed_int_array, dtype='uint8')
        image.shape = (self.window_height, self.window_width, 4)
        image = image[..., :3]
        image = np.ascontiguousarray(image)
        dc_obj.DeleteDC()
        cdc.DeleteDC()
        win32gui.ReleaseDC(hwnd, wdc)
        win32gui.DeleteObject(data_bitmap.GetHandle())
        return image

    def capture_screen_and_keyboard(self):
        frame = self.capture_window()
        filename = f'{self.folder}/img_{self.counter}.jpg'
        cv.imwrite(filename, frame)
        self.key = kb.read_key()
        if kb.is_pressed(self.key):
            kb.on_release_key(self.key, lambda _: _)
            if self.key == 'esc':
                df = pd.DataFrame(self.frame_key_dict)
                df.to_csv(f'{self.folder}/dataframe.csv')
                return False
        else:
            self.key = None
        self.frame_key_dict['frame'].append(filename)
        self.frame_key_dict['move'].append(self.key)
        self.counter = self.counter + 1
        if self.show:
            cv.imshow('FRAME', frame)
            cv.waitKey(1)
        self.capture_screen_and_keyboard()


if __name__ == '__main__':
    obj = Capture(window_name='T-Rex Dinosaur Game - Chrome Dino Runner Online - Google Chrome',
                  x=350,
                  y=200,
                  window_width=900,
                  window_height=200,
                  folder='images',
                  show=False)
    obj.capture_screen_and_keyboard()
