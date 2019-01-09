import socket
import pygame
from pygame.locals import *
import cv2
import sys

host = 192.168.1.100
port = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created")
client_socket.connect(host,port)
print("Established Connection !")

    
pygame.init()
pygame.display.set_mode((250,250))

continue_driving = True

while continue_driving:
    events = pygame.event.get()
    for event in events:
        if event.type == KEYDOWN:
            key_input = pygame.key.get_pressed()
        
            if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                print("Forward Right")
                client_socket.send(chr(6).encode())

            elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                print("Forward Left")
                client_socket.send(chr(7).encode())

            #elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
               #print("Reverse Right")
                #client_socket.send(chr(8).encode())

            #elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                #print("Reverse Left")
                #client_socket.send(chr(9).encode())

            elif key_input[pygame.K_UP]:
                print("Forward")
                client_socket.send(chr(1).encode())

            #elif key_input[pygame.K_DOWN]:
                #print("Reverse")
                #client_socket.send(chr(2).encode())

            elif key_input[pygame.K_RIGHT]:
                print("Right")
                client_socket.send(chr(3).encode())

            elif key_input[pygame.K_LEFT]:
                print("Left")
                client_socket.send(chr(4).encode())

            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                print("Exit")
                continue_driving = False
                client_socket.send(chr(0).encode())
                client_socket.send("Terminating")
                client_socket.close()
                break
        elif event.type == pygame.KEYUP:
            client_socket.send(chr(0).encode())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

    