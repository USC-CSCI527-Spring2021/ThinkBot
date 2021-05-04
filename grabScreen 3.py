import numpy as np
import cv2
import time
import mss
import mss.tools
from PIL import Image
import os, os.path
from pynput import keyboard

DIR = "/Users/rishabhgandhewar/Desktop/pics/train-2021-03-07/train_pics"
monitor = {"top": 145, "left": 200, "width": 450, "height": 600}

COMBINATION = { keyboard.KeyCode.from_char('a'),  
                keyboard.Key.left, keyboard.Key.right}
current = set()
i=0
up, left, right, onlyup = 0, 0, 0, 0

try:
    training_data = open("pics/train-2021-03-07/training_data.csv", 'r')
    val = training_data.read().split('\n')[-2]
    print(val)
    i = int(val.split(',')[0].split('.')[0].split('/')[1]) + 1
    print("i:", i)
except Exception as e:
    print(e)


def on_press(key):
    # try:
        # print('alphanumeric key {0} pressed'.format(key.char))
    if key == keyboard.Key.esc:
        listener.stop()

    global training_data, up, left, right, onlyup

    if key in COMBINATION:
        current.add(key)

    val = ''
    for k in current:
        if k == keyboard.KeyCode.from_char('a'):
            val += "UP "
            up += 1
        elif k == keyboard.Key.left:
            val += "LEFT "
            left += 1
        elif k == keyboard.Key.right:
            val += "RIGHT "
            right += 1

    if keyboard.KeyCode.from_char('a') in current and len(current)==1:
        onlyup += 1

    if val != '':
        img, path = get_image()
        training_data = open("pics/train-2021-03-07/training_data.csv", 'a')
        training_data.write(path + ", " + val + "\n")

    print("Written:", val, "ONLYUP:", onlyup, "UP:", up, "LEFT:", left, "RIGHT:", right)

    # if key == keyboard.Key.esc:
    #     training_data.close()
    # except AttributeError:
    #     print('special key {0} pressed'.format(key))

def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        training_data.close()
        return False
    try:
        current.remove(key)
    except KeyError:
        pass
    
def get_image():
    with mss.mss() as sct:
        num_pics = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        # img = img[270:650, 0:] # crop

        path = "pics/train-2021-03-07/train_pics/r"+str(num_pics)+".jpg"
        cv2.imwrite(path, img)
        # mss.tools.to_png(sct_img.rgb, sct_img.size, output=path)
        num_pics += 1
        return img, path

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()