import firstfonks
import serial
import time
import math
"""import DepthAnythingV2.getLength as bettercallsaul"""
# unoi port ayarları

mega = serial.Serial('/dev/serial/by-path/platform-xhci-hcd.0-usb-0:2:1.0-port0', 31250,timeout=0.1)




mega.bytesize = 8 #Bu, veri bitlerinin sayısını belirtir. Genellikle 8’dir.
mega.parity = 'N' #Bu, parity bitini belirtir. Genellikle ‘N’ (Yok) olarak ayarlanır.
mega.stopbits = 1 #Bu, durdurma bitlerinin sayısını belirtir. Genellikle 1’dir.ü


yaw=0

def set_globyaw(yw):
    global yaw    # Needed to modify global copy of globvar
    yaw = round(yw,1)



def yawRead():
    global yaw  # yaw'ın global olduğunu belirtiyoruz

    try:
        if mega.in_waiting > 0:
            yaw2 = mega.readline().decode('ASCII').rstrip("\n")
            yaw = float(yaw2)  # yaw2'yi float'a dönüştürmeyi deniyoruz
            set_globyaw(-1*(yaw-180))

    except (ValueError, TypeError):
        print(TypeError)  # Eğer dönüştürme başarısız olursa (None veya geçersiz bir değer nedeniyle)
        pass  # Hata oluşursa, bir şey yapmayız ve yaw'ın bir önceki değerini koruruz.

    except KeyboardInterrupt:
        print("Kullanıcı tarafından kesildi.")
    
    return yaw  # Her durumda, yaw'ı döndürürüz

yawRead()

def sendMove(data):
    try:
        #data = "1,14.64,20,150,1,2\n"
        mega.write(data.encode('ASCII')) 
        
            
    except KeyboardInterrupt:
        print("Kullanıcı tarafından kesildi.")



def calculate_infos(cx,cy,cyaw,gx,gy,gyaw):
    mp=[]
    infos = firstfonks.pathplanner(cx,cy,cyaw,gx,gy,gyaw)
    print(infos)
    for miniinfo in infos:
        
        first_yaw = miniinfo[0]
        last_yaw = miniinfo[1]
        
        radius = miniinfo[2]
        rotation = miniinfo[3]
        c_x= miniinfo[4]
        c_y= miniinfo[5]
        if radius<=0.1:
            radius=1

        theta = 0
        if (rotation !=0):
            theta = ((math.atan((16)/radius)) * 180) / math.pi
            theta = round(theta,2)
            alpha = (math.atan(16/(radius+12.25))* 180) / math.pi
            alpha2 = (math.atan(16/(radius-12.25))* 180) / math.pi
        match rotation:
            case 0:#düz
                moveParams = "1,0,0,128,1,2\n"  
            case -1: #sağ
                moveParams = "1,"+ str(theta)+ ","+str(alpha)+",128,1,1\n"
            case 1:#sol
                moveParams = "1,"+ str(theta)+","+str(alpha)+",128,1,-1\n"
            case _:
                moveParams = "1,0,0,0,0,0\n"
            
        mp.append([moveParams,first_yaw,last_yaw,radius,rotation,c_x,c_y])
    return mp


        

# Yaw değerini kontrol etmek için PID kontrolcüsünü oluştur


# Hedeflenen yaw değerini belirle


# Gerçek yaw değerini güncelle ve PID kontrolcüsünün çıktısını al
# Bu çıktı, servo motorları kontrol etmek için kullanılabilir
def main():
    counter =1
    adim= 7
    cmd_s=50.0
    moveParams = "1,0,0,0,0,0\n"
    sendMove(moveParams)
    time.sleep(5)
    yawRead()    
    print(yaw)
    print("1")
    
    time.sleep(2)
    print("2")

    yawRead()
    print(yaw)
    print("lastread:",yaw)
    mp=calculate_infos(40,40,90,40,350,90)
    print(mp)
    time.sleep(2)
    for inf in mp:
        if((inf[4])==0):
            print(inf[0])
            moveParams=inf[0]
            sendMove(moveParams)
            yawRead()
            Kp=0.3
            ref = yaw
            error=0
            t1=time.time()
            t_s=float(inf[3]/cmd_s)
            while True:
                yawRead()
                error= round(ref - yaw,1)
                kontrol_signal= Kp*error
                t2=time.time()
                if (bettercallsaul.obje_yes_no()>0):
                    moveParams="1,0,0,0,1,2\n"      
                    sendMove(moveParams)
                    gecensure=t2-t1
                    kalansure=t_s-gecensure
                    kalanyol = (inf[3]*kalansure)/t_s
                    gidilenyol = (inf[3]*gecensure)/t_s
                    cx=inf[5]
                    cx=inf[6]
                    #Açıya göre

                    break
                print("error:",error)
                if error<-1 or error>1:
                    servoangle=(-1*kontrol_signal)
                    print("servoangle:",servoangle)
                    if servoangle>0:  
                        moveParams= "1,"+str(round(error,1))+","+str(abs(round(servoangle)))+",128,2,-1\n"
                        print(moveParams)
                        
                    elif servoangle<0:
                        moveParams= "1,"+str(round(error,1))+","+str(abs(round(servoangle)))+",128,2,1\n"
                        print(moveParams)

                    sendMove(moveParams)
                if ((t2-t1)>t_s):
                    moveParams="1,0,0,0,1,2\n"
                    #sendMove(moveParams)
                    break
                    
                    
                

                """if(counter<adim):
                    counter=float(inf[3]%adim)
                    time.sleep(counter*0.1) #toplam süre/(toplamyol/1sefedegidilecek)
                    counter=counter+adim
                    yawRead()
                elif(float(inf[3]))>counter:
                    time.sleep(adim*0.1)
                    counter=counter+adim
                    yawRead()
                else:
                    moveParams="1,0,0,0,1,2\n" 
                    print("elsde")     
                    sendMove(moveParams)
                    break"""
                """moveParams="1,0,0,0,1,2\n"      
                sendMove(moveParams)
                time.sleep(1)"""#kamera yaz buraya <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        elif((inf[4])==-1 or (inf[4])==1):
            yawRead()
            inf[2] =round((inf[4]*inf[2]),1)
            moveParams=inf[0]
            sendMove(moveParams)
            while inf[2]!=round(yaw,1):
                print("yawfirst:",yaw)
                print("inffirst:",round(inf[2],1))
                yawRead()
                """moveParams="1,0,0,0,1,2\n"      
                sendMove(moveParams)
                time.sleep(1)"""#kamera yaz buraya <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        

        
    moveParams="1,0,0,0,1,2\n"      
    sendMove(moveParams)          
                
                        
    """while True:
        
        if j == 0:
            moveParams = "1,0,0,70,2,2\n"
            print(moveParams)
            sendMove(moveParams)
            print(moveParams)
            t1=time.time()
            time.sleep(5)
            new_global()
            mypid = pid.PID()
            mypid.SetPoint = float(yawRead())
            
        t2=time.time()
        
        yaw_n = float(yawRead())  # Gerçek yaw değerini almak için kendi fonksiyonunuzu kullanın
        
        mypid.update(yaw_n)
        output = mypid.output
        
        if output<-1 or output>1:
            
            servoangle=(-1*output*0.1)
            if servoangle>0:  
                moveParams= "1,"+str(round(-output))+","+str(round(servoangle))+",70,2,-1\n"
                print(moveParams)
            elif servoangle>0:
                moveParams= "1,"+str(round(output))+","+str(round(-servoangle))+",70,2,1\n"
                print(moveParams)
            sendMove(moveParams)
            print(t2-t1)
        if ((t2-t1)>10):
            moveParams = "1,0,0,0,0,0\n"
            print(moveParams)
            sendMove(moveParams)
            print("kırdım")
            break"""


if __name__ == '__main__':
    main()
    