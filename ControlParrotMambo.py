from tkinter import *
from pyparrot.Minidrone import Mambo
import serial
import time
import simplejson


####PROGRAMACIÓN DRONE####




MACmambo = "e0:14:d0:63:3d:d0"   #dirección MAC bluetooth del parrot mambo

mambo = Mambo(MACmambo, use_wifi=False)   #declaración variable del drone




def conectar():

    success = mambo.connect(num_retries=3)

def despegar():

    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)

    mambo.safe_takeoff(5)


def aterrizar():

    mambo.safe_land(10)

def derecha():

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=1)

def abajo():

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=1)

def izquierda():

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=1)

def arriba():

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=1)

def subir():

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=5, duration=1)

def bajar():

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-5, duration=1)

def rotar_izquierda():

    mambo.turn_degrees(5)


def rotar_derecha():

    mambo.turn_degrees(-5)

####DISEÑO TKINTER#####


#características ventana tkinter

ventana = Tk()
ventana.title("control parrot Mambo")
ventana.geometry("800x700")
ventana.configure(background="white")


#imagenes

imagen_drone = PhotoImage(file="parrotmambo.png")
imagen_bateria = PhotoImage(file="bateria.png")
imagen_boton7 = PhotoImage(file= "botderecha.png")
imagen_boton8 = PhotoImage(file= "botderecha2.png")
imagen_boton9 = PhotoImage(file= "botderecha23.png")
imagen_boton10 = PhotoImage(file= "botderecha234.png")
imagen_boton11 = PhotoImage(file= "botbajar.png")
imagen_boton12 = PhotoImage(file= "botbajar2.png")
imagen_boton13 = PhotoImage(file= "botrotar.png")
imagen_boton14 = PhotoImage(file= "botrotar2.png")

#Posición de las imagenes

imagen_drone_posi = Label (ventana,image=imagen_drone). place(x=224,y=20)
imagen_bateria_posi = Label (ventana, image=imagen_bateria). place(x=660,y= 20)

#Declaracion de los botones

boton1 = Button(ventana, text = "MODO AUTOMÁTICO", width = 15 , height = 2, font= ("Italic" , 10, "bold"), fg="black",bg="beige", command = lambda: click_boton(1) )
boton2 = Button(ventana, text = "MODO MANUAL", width = 15 , height = 2, font= ("Italic" , 10, "bold"), fg="black",bg="beige", command = lambda: click_boton(2) )
boton3 = Button(ventana, text = "EMERGENCIA", width = 10 , height = 1,font= ("Italic" , 15, "bold"), fg="white",bg="red",   command = lambda: click_boton(3) )
boton4 = Button(ventana, text = "DESPEGAR", width = 10 , height = 1, font= ("Italic" , 10, "bold"), fg="white",bg="grey50", command = despegar )
boton5 = Button(ventana, text = "ATERRIZAR", width = 10 , height = 1, font= ("Italic" , 10, "bold"), fg="white",bg="grey50", command = aterrizar )
boton6 = Button(ventana, text = "CONECTAR", width = 8 , height = 1, font= ("Italic" , 10, "bold"), fg="white",bg="green", command = conectar )
boton7 = Button(ventana, image=imagen_boton7, width = 50 , height = 50, command= derecha )
boton8 = Button(ventana, image=imagen_boton8, width = 50 , height = 50, command = abajo )
boton9 = Button(ventana, image=imagen_boton9, width = 50 , height = 50, command = izquierda )
boton10 = Button(ventana, image=imagen_boton10, width = 50 , height = 50, command = arriba )
boton11 = Button(ventana, image=imagen_boton11, width = 50 , height = 50, command = bajar )
boton12 = Button(ventana, image=imagen_boton12, width = 50 , height = 50, command = subir )
boton13 = Button(ventana, image=imagen_boton13, width = 50 , height = 50, command = rotar_derecha )
boton14 = Button(ventana, image=imagen_boton14, width = 50 , height = 50, command = rotar_izquierda  )

#Posicionamiento de los botones

boton1.place(x=30,y=60)   
boton2.place(x=30,y=130)
boton3.place(x=600,y=630)
boton4.place(x=345,y=345)
boton5.place(x=345,y=540)
boton6.place(x=353,y=235)
boton7.place(x=230,y=430)
boton8.place(x=175,y=485)
boton9.place(x=120,y=430)
boton10.place(x=175,y=375)
boton11.place(x=575,y=485)
boton12.place(x=575,y=375)
boton13.place(x=630,y=430)
boton14.place(x=520,y=430)


ventana.mainloop()




