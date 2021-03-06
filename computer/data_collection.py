import cv2
import pygame
from pygame.locals import *
import socket
import numpy as np 
import time 
import os
import sys

host = "192.168.1.100"
port = 8000
input_size = 120*320

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((host,port))
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('rb')
print("Established Connection !")

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Socket Created")
# server_socket.connect((host,port))
# print("Established connection !")
# connection = server_socket.accept()[0].makefile('rb')

send_inst = True

k = np.zeros((4,4), 'float')
for i in range(4):
    k[i,i] = 1

pygame.init()
pygame.display.set_mode((250,250))

#Collection
saved_frame = 0
total_frame = 0

# collect images for training
print("Start collecting images...")
print("Press 'q' or 'x' to finish...")
start = cv2.getTickCount()

X = np.empty((0, input_size))
y = np.empty((0, 4))

# stream video frames one by one
try:
    stream_bytes = b' '
    frame = 1
    while send_inst:
        stream_bytes += connection.read(1024)
        first = stream_bytes.find(b'\xff\xd8')
        last = stream_bytes.find(b'\xff\xd9')

        if first != -1 and last != -1:
            jpg = stream_bytes[first:last + 2]
            stream_bytes = stream_bytes[last + 2:]
            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    
            # select lower half of the image
            height, width = image.shape
            roi = image[int(height/2):height, :]

            cv2.imshow('image', image)

            # reshape the roi image into a vector
            temp_array = roi.reshape(1, int(height/2) * width).astype(np.float32)
                    
            frame += 1
            total_frame += 1

            # get input from human driver
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    # complex orders
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print("Forward Right")
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, k[1]))
                        saved_frame += 1
                        connection.send(chr(6).encode())

                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print("Forward Left")
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, k[0]))
                        saved_frame += 1
                        connection.send(chr(7).encode())

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                        print("Reverse Right")
                        connection.send(chr(8).encode())

                    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                        print("Reverse Left")
                        connection.send(chr(9).encode())

                    # simple orders
                    elif key_input[pygame.K_UP]:
                        print("Forward")
                        saved_frame += 1
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, k[2]))
                        connection.send(chr(1).encode())

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        connection.send(chr(2).encode())

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, k[1]))
                        saved_frame += 1
                        connection.send(chr(3).encode())

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        X = np.vstack((X, temp_array))
                        y = np.vstack((y, k[0]))
                        saved_frame += 1
                        connection.send(chr(4).encode())

                    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                        print("Exit")
                        send_inst = False
                        connection.send(b"Terminating")
                        server_scoket.close()
                        break

                elif event.type == pygame.KEYUP:
                    connection.send(chr(0).encode())

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    # save data as a numpy file
    file_name = str(int(time.time()))
    directory = "training_data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=y)
    except IOError as e:
        print(e)

    end = cv2.getTickCount()
    # calculate streaming duration
    print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))

    print(X.shape)
    print(y.shape)
    print("Total frame: ", total_frame)
    print("Saved frame: ", saved_frame)
    print("Dropped frame: ", total_frame - saved_frame)

finally:
    connection.close()
    server_socket.close()
