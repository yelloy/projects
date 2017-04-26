import socket
import time
import struct
import threading
import ParamList



###### Устройства ######

### Шаблон устройства ###
        
class Base_Device():

    def __init__(self):
        self.Online = False

    ###### Создаем сокет ######
        self.s = socket.socket()       # Создание сокета s
        self.s_lock = threading.Lock() # Создаем s_lock - замок для сокета s

    ###### Подключение (Отключение) к устройству ######
        self.connected = False

    def Connect(self, IP, Port):
        if not self.connected:
            try:
                self.s.connect((IP, Port))
                self.Send_Online()
            except OSError as msg:
                print("Не могу связаться с сокет-сервером: %s\n " % msg)
            else:
                print(IP + " connected")
                self.connected = True

    def Disconnect(self):
        self.s.close()
        self.connected = False

    ###### Отправка сообщения на подключенное устройство ######
    def Send_Msg(self, data):
        self.s_lock.acquire(True)     # Ожидает доступа к сокету, и если сокет доступен - захватывает его.
        try:
            self.s.send(data)   
            time.sleep(0.1)
            self.s_lock.release()
        except OSError: #self.s.error: # здесь нужно указать ошибку сокета(изучить их)
            print ("Socket error\n")

    ### Отправка онлайна ### 
    def Send_Online_msg(self):
        can_msg_online = struct.Struct('I 4B')
        can_msg_online_data = can_msg_online.pack(0x600, 0, 0, 0, 0)
        self.Send_Msg(can_msg_online_data)            # Отправка переменной can_a с сокета s 
 
        
    def Set_ShortInt_Param(self, can_addr, PrmN, Prm):
        can_msg_shortint_param = struct.Struct('=I 6B h')
        сan_msg_shortint_param_data = can_msg_shortint_param.pack(can_addr, 4, 0, 0, 0, PrmN, 2, Prm)
        self.Send_Msg(сan_msg_shortint_param_data)   

    def Cycle(self):
        while True:
            if self.Online:    # Тут вместо False должен быть STOP работающий по ивентам. Когда некая ф-я вызывается возникает ивент меняющий значение STOP
                self.Send_Online_msg()
                time.sleep(1)

    
    def Send_Online(self):
        t = threading.Thread( target = self.Cycle)
        t.start()
    
### Мотор ###
        
class Motor(Base_Device):

    def __init__(self):
        Base_Device.__init__(self) # Наследуем Base_Device

    def Set_Motor_Speed(self, MotorNumber, speed):
        self.Set_ShortInt_Param(self.can_addr, MotorNumber, speed)

    def Initialize(self, can_addr, work_mode):      # 1 - рабочий режим
        self.can_addr = can_addr   # 0x200 
        can_msg_init = struct.Struct('=I 6B')
        can_msg_init_data = can_msg_init.pack(can_addr, 2, 0, 0, 0, 200, work_mode)
        self.Send_Msg(can_msg_init_data)

        

### Шаговый двигатель ###
       
class Stepper(Base_Device):        

    def __init__(self):
        Base_Device.__init__(self) # Наследуем Base_Device

    def Set_Stepper_Pos(self, stepperN, steps):
        can_msg_stepper_pos = struct.Struct('=I 6B H')
        can_msg_stepper_pos_data = can_msg_stepper_pos.pack(self.can_addr, 4, 0, 0, 0, 0xCE, stepperN, steps)
        self.Send_Msg(can_msg_stepper_pos_data)

    def Set_Steppers_Pos(self, steps1, steps2, steps3):
        can_msg_steppers_pos = struct.Struct('=I 5B 3H')
        can_msg_steppers_pos_data = can_msg_steppers_pos.pack(self.can_addr, 7, 0, 0, 0, 0xD0, steps1, steps2, steps3)
        self.Send_Msg(can_msg_steppers_pos_data)
        
    def Initialize(self, can_addr, stepperN, work_mode):    # 2 - рабочий режим
        self.can_addr = can_addr   # 0x230
        can_msg_init = struct.Struct('=I 7B')
        can_msg_init_data = can_msg_init.pack(self.can_addr, 3, 0, 0, 0, 0xC8, stepperN, work_mode)
        self.Send_Msg(can_msg_init_data)

    def Calib_Axes(self, stepperN):
        can_msg_calib_axes = struct.Struct('=I 6B H')
        can_msg_calib_axes_data = can_msg_calib_axes.pack(self.can_addr, 4, 0, 0, 0, 0xCF, stepperN, 0x3C)
        self.Send_Msg(can_msg_calib_axes_data)

    def Print_APCHHI(self):
        print("APPCHHI")

###### ПРИМЕР ######
if __name__ == "__main__":      # Для того чтобы программа не запускалась при её импортирование
    
### Добавляем мнимые моторы ###
    Motor_Controller = []
    Motor1 = Motor()
    Motor_Controller.append(Motor1)
    Motor2 = Motor()
    Motor_Controller.append(Motor2)

### Добавляем мнимые шаговики ###
    Stepper_Controller = []
    Stepper1 = Stepper()
    Stepper_Controller.append(Stepper1)
    Stepper2 = Stepper()
    Stepper_Controller.append(Stepper2)

    Device_List = []
    Device_List.append(Motor_Controller) 
    Device_List.append(Stepper_Controller) 


    Device_List[1][0].Print_APCHHI()


