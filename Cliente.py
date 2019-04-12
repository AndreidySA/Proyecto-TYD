import socket
import random
import smtplib
import pysftp

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MI_CORREO= 'andreidysantanaa@gmail.com'
PASSWORD= 'GiveMeSomeFood.'
MTA_HOST= 'smtp.gmail.com'
MTA_PORT= 587


def EnviarCorreo():
    sesion=smtplib.SMTP(host=MTA_HOST, port=MTA_PORT)
    sesion.starttls()
    sesion.login(MI_CORREO,PASSWORD) #Se logea
    message= MIMEMultipart() #Crea el mensaje
    message['From']=MI_CORREO
    message['To']='20150270@ce.pucmm.edu.do'
    message['Subject']="Felicidades por su buen juego"
    message.attach(MIMEText("Usted ha ganado el último juego de Tres y Dos. ¡FELICIDADES!\nAtt: Equipo de 3 & 2", 'plain'))
    sesion.send_message(message)
    del message
    sesion.quit()



def Ganar(Mano):
    cont = 0
    valor = []
    contando = 0
    for i in Mano:  # Para ir pasando de string a string

        this = Mano[contando]
        contando = contando + 1
        for a in this:
            cont = cont + 1
            if (cont == 2):
                valor.append(a)
                cont = 0

    unicos = set()
    for i in valor:
        unicos.add(i)
    if len(unicos) == 2:
        x = unicos.pop()
        c = valor.count(x)
        if c == 2 or c == 3:
            print("Usted ha ganado")
            return 'G'  # gano


def Jugar(Carta2, Mazo, CartO):
    m=" "
    print("Para tomar la carta del mazo, ingrese 'a', para tomar la carta de su oponente, presione 'b'")
    Respuesta = input()
    if (Respuesta == "a"):
        escogida = random.randint(0, 41)
        print("La carta que le ha tocado es:")
        print(MazoP2[escogida])
        Cambio = input("¿Desea cambiar la carta? [si/no]\n")
        if (Cambio == 'si'):
            print(
                "Cual carta desea cambiar?\nSus cartas están organizadas en posiciones de 1 a 5, favor ingrese la posición")
            posicionCarta = input()
            posicionCarta = int(posicionCarta)
            Carta2.append(Mazo[escogida])
            Mazo.append(Carta2[posicionCarta])  # Enviar carta al mazo
            Mazo.pop(escogida)
            Enviar=Carta2[posicionCarta-1]
            Carta2.pop(posicionCarta - 1)
            m = Ganar(Carta2)
            if (m == 'G'):
                s.send(str.encode("J2G"))  # Enviándole al oponente
                EnviarCorreo()
                win=open("Juego.txt","w+")
                win.write("El jugador 2 es un buen jugador")
                win.close()
                with pysftp.Connection('192.168.77.42', username='root', password='20150270') as sftp:
                    with sftp.cd('TresDos'):
                        print(sftp.listdir())
                        print(sftp.pwd)
                        sftp.put(R"C:\Users\COMPAQ\PycharmProjects\untitled\Juego.txt")  # cargar archivo
                        sftp.get('Juego.txt', R"C:\Users\COMPAQ\PycharmProjects\untitled\Juego.txt")



            MazoJ1 = " ".join(str(x) for x in Mazo)
            s.send(str.encode(MazoJ1))  # Enviándole el mazo
            if(m!="G"):
                s.send(str.encode(Enviar))  # Enviar carta al oponente


        if(Cambio=='no'):
            MazoJ1 = " ".join(str(x) for x in Mazo)
            s.send(str.encode(MazoJ1))  # Enviándole el mazo
            s.send(str.encode(Mazo[escogida]))

    if (Respuesta == "b"):

        print( "Cual carta desea cambiar?\nSus cartas están organizadas en posiciones de 1 a 5, favor ingrese la posición")
        posicionCarta = input()
        posicionCarta = int(posicionCarta)
        Carta2.append(CartO[0])
        Enviar = Carta2[posicionCarta - 1]
        Carta2.pop(posicionCarta - 1)
        m = Ganar(Carta2)
        if (m == "G"):
            s.send(str.encode("J2G"))  # Enviándole al oponente si se ganó
            EnviarCorreo()
            win = open("Juego.txt", "w+")
            win.write("El jugador 2 es un buen jugador")
            win.close()
            with pysftp.Connection('192.168.77.42', username='root', password='20150270') as sftp:
                with sftp.cd('TresDos'):
                    print(sftp.listdir())
                    print(sftp.pwd)  # retorna directorio en el que se está trabajando actualmente
                    sftp.put(
                        R"C:\Users\COMPAQ\PycharmProjects\untitled\Juego.txt")  # cargar archivo
                    sftp.get('Juego.txt', R"C:\Users\COMPAQ\PycharmProjects\untitled\Juego.txt")

        if(m!="G"):
            s.send(str.encode(Enviar))  # Enviar carta al oponente

    if(m!="G"):
        print("Sus cartas son: ")
        print(Carta2)
        print("Turno del jugador 1...")


MazoP2 = []
CartasP2 = []
CartO = []
s = socket.socket()
host = '192.168.0.3'
puerto = 2222
contador = 0

s.connect((host, puerto))

while True:
    if (contador % 2 == 0):
        data = s.recv(1024)

        recibido = data[:].decode("utf-8")

        if (recibido == 'Empieza el juego'):
            print(recibido)
            print("Eres el jugador 2")
            print("Sus cartas son:")
            recibido = ""

        if (recibido == "J1G"):
            print("El jugador 1 ha ganado. Mejor suerte para la próxima")
            break


        else:
            Cartas = recibido.split()
            if (len(Cartas) == 5):
                CartasP2 = Cartas;
            if (len(Cartas) == 1):
                print("La carta que ha arrojado su oponente es:")
                CartO = Cartas
                contador = contador + 1
            # print(Cartas)
            if (len(Cartas) > 5):
                for m in Cartas:
                    MazoP2.append(m)
            else:
                if (len(Cartas) > 0):
                    print(Cartas)
        recibido = ""

    if (contador % 2 != 0):
        Jugar(CartasP2, MazoP2, CartO)
        contador = contador + 1
