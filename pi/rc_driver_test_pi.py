import socket
import serial
import time


#From computer to pi.
host = "192.168.43.122"
port = 8051

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((host,port))
server_socket.listen(0)
conn,addr = server_socket.accept()
print("Established Connection !")

#From Pi to arduino
port_ard = "/dev/ttyACM0"
rate = 115200
ser = serial.Serial(port_ard,rate) 
ser.flushInput()#Clearing input buffer.
time.sleep(5) #Waiting for arduino to reset.


while True:
    data = conn.recv(1024)
    if data == chr(6).encode():
        print("Forward Right")
        ser.write(b"6")
    elif data == chr(7).encode():
        print("Forward Left")
        ser.write(b"7")
    elif data == chr(8).encode():
        print("Reverse Right")
        ser.write(b"8")
    elif data == chr(9).encode():
        print("Reverse Left")
        ser.write(b"9")
    elif data == chr(1).encode():
        print("Forward")
        ser.write(b"1")
    elif data == chr(2).encode():
        print("Reverse")
        ser.write(b"2")
    elif data == chr(3).encode():
        print("Right")
        ser.write(b"3")
    elif data == chr(4).encode():
        print("Left")
        ser.write(b"4")
    elif data == chr(0).encode():
        ser.write(b"0")
    elif data == "Terminating":
        conn.close()
        print("Exit !")
        break
print("Completed Testing")