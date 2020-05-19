from tkinter import *
from pyparrot.Minidrone import Mambo
import serial
import time
import simplejson
import math


####PROGRAMACIÓN DRONE####




MACmambo = "D0:3A:89:B3:E6:5A"              #dirección MAC bluetooth del parrot mambo

mambo = Mambo(MACmambo, use_wifi=False)     #declaración variable del drone

arduino = serial.Serial('/dev/ttyUSB0', 115200)

dead_zone= 4



oldz = 0
oldy = 0
oldx = 0
restaz=0
restay=0
restax=0
counter=0


def conectar():

    print("intentando conectar")
    success = mambo.connect(num_retries=3)
    print("conectado: %s" % success)

    if (success):

        mambo.set_max_tilt(velocidad.get)
        
        print("sleeping")
        mambo.smart_sleep(1)
        mambo.ask_for_state_update()         # Se coge la información del estado del dron(importante para mostrar el nivel de la bateria)
        mambo.smart_sleep(1)
        
    ventana.update()                         # se actualiza la ventana(si no se congelaria en el boton)

def despegar():

    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)

    print("despegando")
    mambo.safe_takeoff(5)
    ventana.update()


def aterrizar():

    print("aterrizando")
    mambo.safe_land(10)
    ventana.update()

def derecha():

    mambo.fly_direct(roll=20, pitch=0, yaw=0, vertical_movement=0, duration=0.5)
    ventana.update()

def abajo():

    mambo.fly_direct(roll=0, pitch=-20, yaw=0, vertical_movement=0, duration=0.5)
    ventana.update()

def izquierda():

    mambo.fly_direct(roll=-20, pitch=0, yaw=0, vertical_movement=0, duration=0.5)
    ventana.update()

def arriba():

    mambo.fly_direct(roll=0, pitch=20, yaw=0, vertical_movement=0, duration=0.5)
    ventana.update()

def subir():

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=20, duration=0.5)
    ventana.update()


def bajar():

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-20, duration=0.5)
    ventana.update()

def rotar_izquierda():

    mambo.turn_degrees(10)
    ventana.update()


def rotar_derecha():

    mambo.turn_degrees(-10)
    ventana.update()

def desconectar():

    print("desconectando")
    mambo.disconnect()
    print("desconectado")
    ventana.update()

def cargabateria():

    
    nivelbateria.set(mambo.sensors.battery)
    ventana.update()

def correcion_angulos(angulo, zona_muerta, maximo ):

    signo=math.copysign(1, angulo)      #se coge el signo del ángulo
    valor = abs(angulo)                 #se trabaja con valores absolutos(al final se dará signo)

    if (valor < zona_muerta):           #Los cambios de posicion inferiores a la zona muerto no són cogidos

        angulo = 0
        return angulo

    else:
        
            
        valor = float(min(valor, maximo))  #se coge el mínimo entre el valor entrado y el maximo definido
            
        valor -= zona_muerta
           

    angulo = float(signo*valor)
    return angulo




####DISEÑO TKINTER#####


#características ventana tkinter

ventana = Tk()
ventana.title("control parrot Mambo")
ventana.geometry("800x700")
ventana.configure(background="white")


#configuración velocidad

velocidad=Scale(ventana,from_ =0, to=200, orient=HORIZONTAL,length=220, label= "Máxima inclinación (velocidad) " ,bg="white", tickinterval=100)
velocidad.set(20)                            #Se inicializa como velocidad 20
velocidad.place(x=20,y=180)



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

imagen_drone_posi = Label (ventana,image=imagen_drone). place(x=264,y=20)
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
boton15 = Button(ventana, text = "DESCONECTAR", width = 10 , height = 1, font= ("Italic" , 10, "bold"), fg="white",bg="blue2", command = desconectar )

#Posicionamiento de los botones

boton1.place(x=50,y=40)   
boton2.place(x=50,y=110)
boton3.place(x=600,y=630)
boton4.place(x=345,y=345)
boton5.place(x=345,y=540)
boton6.place(x=393,y=235)
boton7.place(x=230,y=430)
boton8.place(x=175,y=485)
boton9.place(x=120,y=430)
boton10.place(x=175,y=375)
boton11.place(x=575,y=485)
boton12.place(x=575,y=375)
boton13.place(x=630,y=430)
boton14.place(x=520,y=430)
boton15.place(x=30,y=640)

#Etiquetas

Lbl_porcentage_bat = Label(text="%", font = ("Italic", 10, "bold"), bg="white").place (x=710, y= 120)

nivelbateria = StringVar()

Lbl_bat= Label(ventana, textvariable= nivelbateria).place(x=670,y=120)



def main():

    global oldz
    global oldy
    global oldx
    global counter


      
    while 1:


        ventana.update_idletasks()
        ventana.update()

        

        if counter==10:

            cargabateria()
            couter=0
        
        else:

            counter+=1
    
            

        jsonResult=arduino.readline()
        

        try:
                

            jsonObject=simplejson.loads(jsonResult)
            x,y,z,sys,gyro,accel,mag= jsonObject["x"], jsonObject["y"], jsonObject["z"],jsonObject["sys"],jsonObject["gyro"],jsonObject["accel"],jsonObject["mag"]

            Z=float(z)*100/180
            Y=float(y)*100/90
            X=(((float(x)-0)*(180-(-180)))/(360-0))+(-180)

            restaz = Z - oldz
            restay = Y - oldy
            restax = X - oldx


            print(int(Z)," ",int(oldz)," ",restaz)

            """if Z>10:

                mambo.fly_direct(roll=0, pitch=20, yaw=0, vertical_movement=0, duration=0.05)
            
            elif Z<-10 :

                mambo.fly_direct(roll=0, pitch=-20, yaw=0, vertical_movement=0, duration=0.05)

            else:

                mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=0)"""

            oldz = Z
            oldy = Y
            oldx = X



        
        except Exception as Error:

            print(repr(Error))

            pass


if (__name__ == '__main__'):
	main()




