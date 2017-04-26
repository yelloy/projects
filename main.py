from Controlmain import *
import time

M = Motor()
M.Connect("192.168.42.232",13133)
M.Online = True
time.sleep(0.2)
M.Initialize(0x200, 1)
#time.sleep(0.5)
M.Set_Motor_Speed(10, 20)
print("Hm?")
time.sleep(2)
M.Set_Motor_Speed(11, -20)
time.sleep(3)
print("Oi!")
M.Initialize(0x200, 0)
M.Disconnect()
print("AAAAAAAAPCHHI")
