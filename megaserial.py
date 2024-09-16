import serial
import time
import serialFonk as sf
import struct

# unoi port ayarları
#uno = serial.Serial('/dev/serial/by-path/platform-xhci-hcd.1-usb-0:2:1.0-port0', 115200)  # COM1 yerine kullanılan portu belirtin
#mega = serial.Serial('/dev/serial/by-path/platform-xhci-hcd.0-usb-0:2:1.0-port0', 9600)
def read_float():
    # 4 bayt oku (bir float 4 bayttır)
    bytes = sf.mega.read(4)

    # Baytları bir float'a dönüştür
    float_val = struct.unpack('f', bytes)[0]

    return float_val

    

def main():
    i = 0
    data_to_send = "2,0,0,0,0,0\n"
    sf.serialSend("mega",data_to_send)
    """if(i!=1):
        time.sleep(2)
        i=1"""
    time.sleep(2)
    if i in range(100):
        print(read_float())
    """data_to_send = "1,0,0,255,1,1\n"
    mega.write(data_to_send.encode('ASCII'))
    time.sleep(2)"""
    """data_to_send = "1,20,20,100,1,1\n"
    mega.write(data_to_send.encode('ASCII'))
    time.sleep(2)
    data_to_send = "1,-20,20,100,1,-1\n"
    mega.write(data_to_send.encode('ASCII'))
    time.sleep(2)"""
    """data_to_send = "1,0,0,0,0,0\n"
    mega.write(data_to_send.encode('ASCII'))
    time.sleep(1)"""
   
    
    

if __name__ == '__main__':
    while True:
        main()
    
    