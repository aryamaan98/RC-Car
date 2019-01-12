import socket
import serial
import time
import io
import picamera

#From computer to pi.
host = "192.168.43.122"
port = 8051

#Video Streaming to computer
class SplitFrames(object):
    def __init__(self, connection):
        self.connection = connection
        self.stream = io.BytesIO()
        self.count = 0
    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((host, port)) #bind
connection = client_socket.makefile('wb')
print("Connection Accepted")

#From Pi to arduino
port_ard = "/dev/ttyACM0"
rate = 115200
ser = serial.Serial(port_ard,rate) 
ser.flushInput()#Clearing input buffer.
time.sleep(5) #Waiting for arduino to reset.



try:
    output = SplitFrames(connection)
    with picamera.PiCamera(resolution='640x480', framerate=60) as camera:   
        camera.start_preview()
        time.sleep(2)

        start = time.time()
        camera.start_recording(output, format='mjpeg')
        camera.wait_recording(30)
        camera.stop_recording()

        connection.write(struct.pack('<L', 0))


        # After sending the frames receiving the controls to be sent to auduino.
        data = client_socket.recv(1024)
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
            connection.close()
            client_socket.close()
            print("Exit !")
            break
finally:
    finish = time.time()
    print('Sent %d images in %d seconds at %.2ffps' % (output.count, finish-start, output.count / (finish-start)))

