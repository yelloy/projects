import pygame, time, threading, math

class Joystick_Handler():    # Функция отвечающая за обработку сигналов с Джойстика

    def __init__(self):
        self.R = 0
        self.L = 0
        


    def go(self):

####### Используемые переменные ######
        ext = False
        

    
        pygame.init()                            # Инициализирует библиотеку пугейма
        try:
            joystick = pygame.joystick.Joystick(0)   # Присваиваем первому подключенному джойстику(0) имя "joystick" 
            joystick.init()                          # Инициализируем джойстик "joystick"
            print("Joystick initialized")
        except:
            print("Problem with joystick")

        joystick_count = pygame.joystick.get_count() # Считаем кол-во подключенных джойстиков
        
        while not ext:
            pygame.event.get()                       # Узнаем о событиях связанных с джойстиком

            if joystick_count != 0:                  # Если хотя бы 1 джойстик подключен, то  


###### Обработчик сигналов с кнопок ######
        
                buttons = joystick.get_numbuttons()
                for button_number in range(buttons):  # Проверяем в цикле состояние каждой кнопки
                    button_pressed = joystick.get_button(button_number) # Кнопка нажата? да - button_pressed = 1, нет - button_pressed = 0
                if button_pressed:              # Если кнопка нажата
                    ext=1
                    continue
                    pass

###### Обработчик осей стиков ######
        
                h_axs = int(100*joystick.get_axis(3))  # Содержит значение горизонтальной оси правого стика (варируется от -100 до 100)
                v_axs = int(100*joystick.get_axis(1))  # Содержит значение вертикальной оси левого стика

                h_axs = ((h_axs+2)//20)*20                # Преобразуем шаг изменения значения горизонтальной оси с 1 на 20 
                v_axs = ((v_axs+2)//20)*20                # То же с вертикальной осью. Таким образом 200 возможных значений скорости мотора преобразуются в 11

                h_axs = int(h_axs//2)                     # Уменьшаем значение горизонтальной оси в 2 раза, для уменьшения скорости поворота в дальнейшем
    
                if h_axs<=0:
                    speedR = (-v_axs)
                else:
                    speedR = (-v_axs) + h_axs
                if h_axs < 0:
                    speedL = (v_axs) + h_axs
                else:
                    speedL = (v_axs)

###### Значения скоростей моторов для отправки ######

                time.sleep(0.1)             # Задержка, ограничивающая частоту отправления команд до 10 раз в секунду

                self.R = speedR
                self.L = speedL
                

            else:
                print("Joystick not founded")
        pygame.quit()   # Закрываем пугейм

    def return_speed(self):
        return(self.R, self.L)
    
class Joystick_thread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.Joy = Joystick_Handler()

    def run(self):
        self.Joy.go()


    def get_Speed(self):
        return self.Joy.return_speed()
 

