import serial
import time
import serialFonk
# unoi port ayarları
uno = serial.Serial('/dev/serial/by-path/platform-xhci-hcd.1-usb-0:2:1.0-port0', 115200)  # COM1 yerine kullanılan portu belirtin
mega = serial.Serial('/dev/serial/by-path/platform-xhci-hcd.0-usb-0:2:1.0-port0', 9600)

dosya_adi = "veri.txt"

def unodinleme():
    try:
        with open("veri.txt", "w") as dosya:
            for i in range(6000):
                print(i)
                
                veri = mega.readline().decode('ASCII').strip()
                print(veri)
                if veri:
                    print(f"Okunan veri: {veri}")
                    #dosya.write(veri + "\n")
    except KeyboardInterrupt:
        print("Kullanıcı tarafından kesildi.")
    finally:
        # unoi port bağlantısını kapatın
       
        print("Veri veri.txt dosyasına 360 satırla kaydedildi.")


def main():
    print('main1')
    #uno.write('1'.encode('ASCII'))  # Veriyi bytelara dönüştürerek gönderin
    print('main2')
    time.sleep(2)
    #Targetangle servoangle speed direction rotation
    data_to_send = "1,14.64,20,150,1,2\n"
    mega.write(data_to_send.encode('ASCII'))
    
    time.sleep(1)
    """data_to_send = "1,0,,255,1,1\n"
    mega.write(data_to_send.encode('ASCII'))
    time.sleep(4)"""
    data_to_send = "2,0,0,0,0,0,0\n"
    mega.write(data_to_send.encode('ASCII'))
    for i in range(10):
        data = mega.readline().decode('ASCII').strip()
    print(data)
    """data_to_send = "1,20,20,100,1,1\n"
    mega.write(data_to_send.encode('ASCII'))
    time.sleep(2)
    data_to_send = "1,-20,20,100,1,-1\n"s
    mega.write(data_to_send.encode('ASCII'))
    time.sleep(2)
    data_to_send = "1,0,0,0,0,0\n"
    mega.write(data_to_send.encode('ASCII'))
    time.sleep(1)"""
    
    #uno.write('2'.encode('ASCII'))  # Veriyi bytelara dönüştürerek gönderin
    #unodinleme()
    data_to_send = "1,0,0,0,0,1\n"
    mega.write(data_to_send.encode('ASCII'))

    #uno.write('1'.encode('ASCII'))  # Veriyi bytelara dönüştürerek gönderin
    print('main5')
    time.sleep(2)
    
    
    

if __name__ == '__main__':
   
    main()
    uno.close()
    