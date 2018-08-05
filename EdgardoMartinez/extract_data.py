import retro
import pygame
from pygame.locals import *
import numpy
import threading
import csv
import cv2
import imutils
import datetime

def save_in_file(row):
    with open('action.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row.tolist())


def sonic_action():
    #["B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"]
    action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    keys=pygame.key.get_pressed()
    if keys[K_LEFT]:
        action[6] = 1
    if keys[K_UP]:
        action[0] = 1
    if keys[K_RIGHT]:
        action[7] = 1
    if keys[K_DOWN]:
        action[5] = 1
    return action

action_to_learn = False
env = retro.make(game='SonicTheHedgehog-Genesis', state='GreenHillZone.Act1')
_obs = env.reset()
act = 0
threads = []
firstFrame = None
video_size = 800, 600
while True:
    text = "Not Found"
    #GYM RENDER AS IMAGE
    img = env.render(mode='rgb_array')
    # ROTATE THE IMAGE THE MATRIX IS 90 grates and mirrores
    img = numpy.flipud(numpy.rot90(img))
    # GRAY SCALE
    frame = imutils.resize(img, width=500)
    # Movement detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    gray = cv2.bitwise_not(gray)
    if firstFrame is None:
        firstFrame = gray
        continue
    # # compute the absolute difference between the current frame and
    # # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # # loop over the contours
    for c in cnts:
    #     # if the contour is too small, ignore it
        if cv2.contourArea(c) < 70 or cv2.contourArea(c) > 2000:
            continue
    #     # compute the bounding box for the contour, draw it on the frame,
    #     # and update the text
        action_to_learn =  True
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
    #     text = "Found"
    # # draw the text and timestamp on the frame
    # cv2.putText(frame, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    # # end Movement Detection
    surf = pygame.surfarray.make_surface(frame)
    screen = pygame.display.set_mode(video_size)
    firstFrame = gray
    screen.blit(surf, (0, 0))
    pygame.display.update()
    action = sonic_action()
    # The observation array is now 215040
    # data_x = data[:,:215039]
    # data_y = data[:,[215040,215041,215042,215043,215044,215045,215046,215047,215048,215049,215050,215051]]
    img = img.transpose(2,0,1).reshape(-1,img.shape[1])
    o_matrix = img.flatten()
    if not numpy.array_equal(action, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) or action_to_learn:
        act +=1
        numpy.append(o_matrix, action)
        t = threading.Thread(target=save_in_file, args=(o_matrix,))
        threads.append(t)
        action_to_learn = False
        t.start()
    _obs, rew, done, info = env.step(action)
    print(info['screen_x'], act)
    if done:
        break
