import numpy as np
from PIL import Image
import cv2

import mss
import mss.tools

import pyautogui
import time, random
import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F

time.sleep(2)

def forward():
    pyautogui.keyDown("right")
    time.sleep(0.25)
    pyautogui.keyUp("right")
    time.sleep(0.2)

def backward():
    pyautogui.keyDown("left")
    time.sleep(0.15)
    pyautogui.keyUp("left")
    time.sleep(0.2)

# define the CNN architecture
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # convolutional layer (sees 32x32x3 image tensor)
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        # convolutional layer (sees 16x16x16 tensor)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        # convolutional layer (sees 8x8x32 tensor)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        # max pooling layer
        self.pool = nn.MaxPool2d(2, 2)
        # linear layer (64 * 4 * 4 -> 500)
        self.fc1 = nn.Linear(64*4*4, 500)
        # linear layer (500 -> 2)
        self.fc2 = nn.Linear(500, 2)
        # dropout layer (p=0.25)
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        # add sequence of convolutional and max pooling layers
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        # flatten image input
#         print(x.shape)
        x = x.view(-1, 64*4*4)
        # add dropout layer
        x = self.dropout(x)
        # add 1st hidden layer, with relu activation function
        x = F.relu(self.fc1(x))
        # add dropout layer
        x = self.dropout(x)
        # add 2nd hidden layer, with relu activation function
        x = self.fc2(x)
        return x

# monitor = {"top": 30, "left": 50, "width": 650, "height": 550}
monitor = {"top": 145, "left": 200, "width": 450, "height": 600}

# create a complete CNN
model = Net()
model.load_state_dict(torch.load('model_cifar.pt'))
print("Loaded model from disk")

transform = transforms.Compose([
    transforms.Resize((32,32)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])



img_rows, img_cols = 32, 32




i=0
print("Starting to play...")
while True:
	with mss.mss() as sct:
		sct_img = sct.grab(monitor)
		img = np.array(sct_img)
		img = img[270:650, 0:] # crop

		input = transform(img)

		input = input.view(1, 3, 32,32)

		output = model(input)
		prediction = int(torch.max(output.data, 1)[1].numpy())
		print(prediction)
		if prediction == 0:
			# pyautogui.press('a')
			# straight()
			print("Backward")
			backward()
		elif prediction == 1:
			# pyautogui.press(['a', 'left'])
			# forward_left()
			print("Forward")
			forward()
		i+=1
