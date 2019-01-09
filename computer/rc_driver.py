import socket
import serial
import pygame
from pygame.locals import *
def connect(host,port,serial_port,input_size):
    server_socket = socket.socket()
    server_socket.bind((host,port))
    server_socket.listen(0)

    connection = server_socket.accept()[0].makefile('rb')
    ser = serial.Serial(serial_port,115200,timeout=1)
    send_inst = True
    
pygame.init()
pygame.display.set_mode((250,250))

events = pygame.event.get()
for event in events:
    if event.type == KEYDOWN:
        key_input = pygame.key.get_pressed()

    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
        print("Forward Right")
        X = np.vstack((X, temp_array))
        y = np.vstack((y, self.k[1]))
        saved_frame += 1
        self.ser.write(chr(6).encode())

    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
        print("Forward Left")
        X = np.vstack((X, temp_array))
        y = np.vstack((y, self.k[0]))
        saved_frame += 1
        self.ser.write(chr(7).encode())

    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
        print("Reverse Right")
        self.ser.write(chr(8).encode())

    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
        print("Reverse Left")
        self.ser.write(chr(9).encode())

            
    elif key_input[pygame.K_UP]:
        print("Forward")
        saved_frame += 1
        X = np.vstack((X, temp_array))
        y = np.vstack((y, self.k[2]))
        self.ser.write(chr(1).encode())

    elif key_input[pygame.K_DOWN]:
        print("Reverse")
        self.ser.write(chr(2).encode())

    elif key_input[pygame.K_RIGHT]:
        print("Right")
        X = np.vstack((X, temp_array))
        y = np.vstack((y, self.k[1]))
        saved_frame += 1
        self.ser.write(chr(3).encode())

    elif key_input[pygame.K_LEFT]:
        print("Left")
        X = np.vstack((X, temp_array))
        y = np.vstack((y, self.k[0]))
        saved_frame += 1
        self.ser.write(chr(4).encode())

    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
        print("exit")
        self.send_inst = False
        self.ser.write(chr(0).encode())
        self.ser.close()
        break

    elif event.type == pygame.KEYUP:
        self.ser.write(chr(0).encode())

if cv2.waitKey(1) & 0xFF == ord('q'):
    break

    