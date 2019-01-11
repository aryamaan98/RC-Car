import socket
import pygame
from pygame.locals import *
import cv2
import sys

host = "127.0.0.1"
port = 9050



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created")
client_socket.bind((host,port))
conn = client_socket.accept()
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
                conn.send(chr(6).encode())

            elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                print("Forward Left")
                conn.send(chr(7).encode())

            elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                print("Reverse Right")
                conn.send(chr(8).encode())

            elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                print("Reverse Left")
                conn.send(chr(9).encode())

            elif key_input[pygame.K_UP]:
                print("Forward")
                conn.send(chr(1).encode())

            elif key_input[pygame.K_DOWN]:
                print("Reverse")
                conn.send(chr(2).encode())

            elif key_input[pygame.K_RIGHT]:
                print("Right")
                conn.send(chr(3).encode())

            elif key_input[pygame.K_LEFT]:
                print("Left")
                conn.send(chr(4).encode())

            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                print("Exit")
                continue_driving = False
                conn.send(chr(0).encode())
                conn.send("Terminating")
                conn.close()
                break
        elif event.type == pygame.KEYUP:
            conn.send(chr(0).encode())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        conn.close()
        server_socket.close()
        break
        

    