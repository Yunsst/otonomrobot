import serial
import time

# Arduino'nun bağlı olduğu portu belirleyin (örneğin: '/dev/ttyACM0' veya 'COM3')


"""data_to_send = "1"
uno.write(data_to_send.encode('ASCII'))
time.sleep(1)"""

def serialSend(slave,data):

    # double turn(double targetAngle, int servoAngle,int V,int direction,int rotation)
    # Gönderilecek veriler
    uno = serial.Serial('/dev/serial/by-path/platform-xhci-hcd.1-usb-0:2:1.0-port0', 115200)  # COM1 yerine kullanılan portu belirtin
    mega = serial.Serial('/dev/serial/by-path/platform-xhci-hcd.0-usb-0:2:1.0-port0', 9600)
    if slave == "mega":
        data_to_send = data
        mega.write(data_to_send.encode('ASCII'))

         
    elif slave == "uno":
        data_to_send = data
        uno.write(data_to_send.encode('ASCII'))
        time.sleep(2)
    
    
        
        # Seriyi kapatıyoruz
        #ser.close()



def serialRead(slave):
    uno = serial.Serial('/dev/serial/by-path/platform-xhci-hcd.1-usb-0:2:1.0-port0', 115200)  # COM1 yerine kullanılan portu belirtin
    mega = serial.Serial('/dev/serial/by-path/platform-xhci-hcd.0-usb-0:2:1.0-port0', 9600)
    #r = None  # r'yi başlangıçta None olarak ayarlayın
    if slave == "mega":
        if mega.in_waiting > 0:
            received_data = mega.readline().decode('ASCII').strip()
            if received_data:
                r = received_data
            time.sleep(0.05)
            return r
    elif slave == "uno":
        if uno.in_waiting > 0:
            received_data = uno.readline().decode('ASCII').strip()
            if received_data:
                r = received_data
            time.sleep(0.05)            
            return r



def main():
    data_to_send = "2,0,0,0,0,0\n"
    serialSend("mega",data_to_send)
    time.sleep(5)
    while True:
        print(serialRead("mega"))


if __name__ == '__main__':
    main()




            

