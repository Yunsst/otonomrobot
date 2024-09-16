
import serial
import time
while True:
    # Arduino'nun bağlı olduğu portu belirtin
    arduino_port = "/dev/ttyUSB0"  # Linux için
    # arduino_port = "COM3"  # Windows için

    # Seri bağlantıyı başlat
    ser = serial.Serial(arduino_port, 9600)

    # Arduino'nun başlaması için biraz zaman ver
    time.sleep(2)

    # Gönderilecek veri
    data = "2,0,0,0,0,0\n"

    # Veriyi Arduino'ya gönder
    ser.write(data.encode('ASCII'))

    # Gelen veriyi oku ve bir değişkende sakla
    received_data = ser.readline().decode('ASCII').strip()

    # Gelen veriyi yazdır
    print("Aldığım veri: ", received_data)

    # Seri bağlantıyı kapat
    
ser.close()
