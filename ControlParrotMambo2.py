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



#DEFINICION DE VARIABLES

#offsets

offset_z=5
offset_y=5


#angulos relativos

oldz = 0
oldy = 0
oldx = 0


#contador para lectura de la bateria

counter=0

#zonas muertas y maximos para filtrado de angulos

zonamuerta_z = 0.5
zonamuerta_y = 0.5
zonamuerta_x = 0.8
maximo_z = 5
maximo_y = 5
maximo_x = 3
factorx= 5



def conectar():

    print("intentando conectar")
    success = mambo.connect(num_retries=3)
    print("conectado: %s" % success)

    if (success):

        
        print("sleeping")
        mambo.smart_sleep(1)
        mambo.ask_for_state_update()         # Se coge la información del estado del dron(importante para mostrar el nivel de la bateria)
        mambo.smart_sleep(1)
        
    ventana.update()                # se actualiza la ventana(si no se congelaria en el boton)

                                
def despegar():

    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)

    print("despegando!")
    mambo.safe_takeoff(5)
    ventana.update()


def aterrizar():

    print("aterrizando")
    mambo.safe_land(10)
    mambo.smart_sleep(5)
    ventana.update()


def derecha(speed):

    mambo.fly_direct(roll=speed, pitch=0, yaw=0, vertical_movement=0, duration=0.5)
    ventana.update()


def abajo(speed):

    mambo.fly_direct(roll=0, pitch=-speed, yaw=0, vertical_movement=0, duration=0.5)
    ventana.update()


def izquierda(speed):

    mambo.fly_direct(roll=-speed, pitch=0, yaw=0, vertical_movement=0, duration=0.5)
    ventana.update()


def arriba(speed):

    mambo.fly_direct(roll=0, pitch=speed, yaw=0, vertical_movement=0, duration=0.5)
    ventana.update()


def subir(speed):

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=speed, duration=0.5)
    ventana.update()
    

def bajar(speed):

    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-speed, duration=0.5)
    ventana.update()


def rotar_izquierda(speed):

    mambo.fly_direct(roll=0, pitch=0, yaw=speed, vertical_movement=0, duration=0.5)
    ventana.update()


def rotar_derecha(speed):

    mambo.fly_direct(roll=0, pitch=0, yaw=-speed, vertical_movement=0, duration=0.5)
    ventana.update()


def desconectar():

    print("desconectando")
    mambo.disconnect()
    print("desconectado")
    ventana.update()


def emergencia():

    print("EMERGENCIA!!!!!")


    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=2)

    print("aterrizando")
    mambo.safe_land(10)
    mambo.smart_sleep(5)
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


def correccion_offset(valor,offset):


    if valor<offset and valor>-offset:

        valor=0
    
    else:

        valor=valor
    
    return valor


def calibrar():


    jsonResult=arduino.readline()
                

    try:
                        

        jsonObject=simplejson.loads(jsonResult)
        sys,gyro,accel,mag= jsonObject["sys"],jsonObject["gyro"],jsonObject["accel"],jsonObject["mag"]
        nivel_sys.set(sys)   
        nivel_gyro.set(gyro)
        nivel_accel.set(accel)
        nivel_mag.set(mag)         

    except Exception as Error:

        print(repr(Error))

        pass
        




####DISEÑO TKINTER#####


#características ventana tkinter

ventana = Tk()
ventana.title("control parrot Mambo")
ventana.geometry("800x700")
ventana.configure(background="white")


#configuración velocidad

velocidad=Scale(ventana,from_ =0, to=200, orient=HORIZONTAL,length=220, label= "               VELOCIDAD (%) " ,bg="white", tickinterval=100)
velocidad.set(20)                            #Se inicializa como velocidad 20
velocidad.place(x=530,y=250)



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

imagen_drone_posi = Label (ventana,image=imagen_drone). place(x=230,y=20)
imagen_bateria_posi = Label (ventana, image=imagen_bateria). place(x=660,y= 20)

#Declaracion de los botones

boton3 = Button(ventana, text = "EMERGENCIA", width = 10 , height = 1,font= ("Italic" , 15, "bold"), fg="white",bg="red",   command = emergencia )
boton4 = Button(ventana, text = "DESPEGAR", width = 10 , height = 1, font= ("Italic" , 10, "bold"), fg="white",bg="grey50", command = despegar )
boton5 = Button(ventana, text = "ATERRIZAR", width = 10 , height = 1, font= ("Italic" , 10, "bold"), fg="white",bg="grey50", command = aterrizar )
boton6 = Button(ventana, text = "CONECTAR", width = 8 , height = 1, font= ("Italic" , 10, "bold"), fg="white",bg="green", command = conectar )
boton7 = Button(ventana, image=imagen_boton7, width = 50 , height = 50, command=lambda:derecha(velocidad.get()) )
boton8 = Button(ventana, image=imagen_boton8, width = 50 , height = 50, command =lambda: abajo(velocidad.get()))
boton9 = Button(ventana, image=imagen_boton9, width = 50 , height = 50, command =lambda: izquierda(velocidad.get()) )
boton10 = Button(ventana, image=imagen_boton10, width = 50 , height = 50, command =lambda: arriba(velocidad.get()) )
boton11 = Button(ventana, image=imagen_boton11, width = 50 , height = 50, command =lambda: bajar(velocidad.get()) )
boton12 = Button(ventana, image=imagen_boton12, width = 50 , height = 50, command =lambda: subir(velocidad.get()) )
boton13 = Button(ventana, image=imagen_boton13, width = 50 , height = 50, command =lambda: rotar_derecha(velocidad.get()) )
boton14 = Button(ventana, image=imagen_boton14, width = 50 , height = 50, command =lambda: rotar_izquierda(velocidad.get())  )
boton15 = Button(ventana, text = "DESCONECTAR", width = 10 , height = 1, font= ("Italic" , 10, "bold"), fg="white",bg="blue2", command = desconectar )

#Posicionamiento de los botones

boton3.place(x=600,y=630)
boton4.place(x=345,y=345)
boton5.place(x=345,y=540)
boton6.place(x=355,y=235)
boton7.place(x=230,y=430)
boton8.place(x=175,y=485)
boton9.place(x=120,y=430)
boton10.place(x=175,y=375)
boton11.place(x=575,y=485)
boton12.place(x=575,y=375)
boton13.place(x=630,y=430)
boton14.place(x=520,y=430)
boton15.place(x=30,y=640)

#Boton de control

man_auto = BooleanVar() 
boton_control = Checkbutton(ventana, text='BLOQUEAR IMU',variable=man_auto,onvalue=True, offvalue=False)
man_auto.set(True)
boton_control.place(x=60,y=230)

#Etiqueta bateria

Lbl_porcentage_bat = Label(text="%", font = ("Italic", 10, "bold"), bg="white").place (x=710, y= 120)

nivelbateria = StringVar()

Lbl_bat= Label(ventana, textvariable= nivelbateria).place(x=670,y=120)

#Etiqueta calibraciones

Lbl_cal = Label(text="CALIBRACION IMU", font = ("Italic", 10, "bold"), bg="white").place (x=45, y= 40)
Lbl_sys = Label(text="SYS:", font = ("Italic", 10), bg="white").place (x=60, y= 80)
Lbl_gyro = Label(text="GYRO:", font = ("Italic", 10), bg="white").place (x=60, y= 100)
Lbl_accel = Label(text="ACCEL:", font = ("Italic", 10), bg="white").place (x=60, y= 120)
Lbl_mag = Label(text="MAG", font = ("Italic", 10), bg="white").place (x=60, y= 140)

nivel_sys=StringVar()
nivel_gyro=StringVar()
nivel_accel=StringVar()
nivel_mag=StringVar()

Lbl_valor_sys= Label(ventana, textvariable= nivel_sys).place(x=140,y=80)
Lbl_valor_gyro= Label(ventana, textvariable= nivel_gyro).place(x=140,y=100)
Lbl_valor_accel= Label(ventana, textvariable= nivel_accel).place(x=140,y=120)
Lbl_valor_mag= Label(ventana, textvariable= nivel_mag).place(x=140,y=140)




def main():

    global oldz
    global oldy
    global oldx
    global offset_z
    global offset_y
    global factorx
    global counter
    


    while 1:

        ventana.update_idletasks()
        ventana.update()
    

        if counter==10:

            cargabateria()
            calibrar()
            couter=0
        
        else:

            counter+=1
        
        if man_auto.get()==False:
    
            jsonResult=arduino.readline()
            
            try:
                    

                jsonObject=simplejson.loads(jsonResult)
                x,y,z= jsonObject["x"], jsonObject["y"], jsonObject["z"]

                Z=float(z)*100/180
                Y=(float(y)*100/90)*(-1)     #se multiplica por menos 1 ya que los valores de la IMU decrecen en sentido horario
                X=(((float(x)-0)*(100-(-100)))/(360-0))+(-100)

                Z=correccion_offset(Z,offset_z)
                Y=correccion_offset(Y,offset_y)

                restaz = Z - oldz
                restay = Y - oldy
                restax = X - oldx

                restax*=factorx

                print(Z," ", Y," ", restax)

                oldz = Z
                oldy = Y
                oldx = X

                
                mambo.fly_direct(roll=Y, pitch=Z, yaw=restax, vertical_movement=0, duration=0.005)

                
            except Exception as Error:

                print(repr(Error))

                pass
        
        else:

            ventana.update()        


if (__name__ == '__main__'):
	main()