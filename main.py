### Замки стоит поменять на очередь, чтобы не возникало тупиков 
from Gromozeka import *
import time

D = Robot()
D.add_Motor_Controller(0)
M = D.Motors_Contr_List[0]
D.Connect("192.168.42.232",13133)
D.Send_Online()
D.Listen()
time.sleep(0.2)
M.Initialize(ISREADY)
#print("Hm?")
M.MotorA(20)
M.MotorB(-20)
time.sleep(3)
#print("Oi!")
M.Initialize(NOTREADY)
D.Disconnect()
print("AAAAAAAAPCHHI")


#### КАК ЗАМУТИТЬ ПАРАМЛИСТ. Инструкция для чайников ##########################
## 1. По 6-му элементу сообщения определяем кто оно по жизни                 ##
## 2. Из уже определенного сообщения вытягиваем инфу и раскидываем куда надо ##
## 3. Смотрим следующий элемент.                                             ##
###############################################################################


