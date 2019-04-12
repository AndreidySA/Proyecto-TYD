import random
import socket
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


def Juego(conn):
    control = 0  # Se usará para que si es la primera vez no pregunte por la carta del oponente
    Cartaop = []
    Respuesta=" "
    Mazo=sum(list(map( lambda tipo: ['♠'+str(tipo),'♣'+str(tipo),'♥'+str(tipo),'♦'+str(tipo)], ['A','K','Q','J',2,3,4,5,6,7,8,9,10])),[])

    # Map genera una lista de listas
    # sum agrega las listas del segundo nivel en una sola, usando la sobrecarga de + para listas
    cartastotales=[]
    posicionescartas=[]
    CartasP1=[]
    CartasP2=[]
    contador=0 #Para intercambiar turnos
    for i in range(10):
        a=random.randint(0,51)

        while a in posicionescartas: #Para que no se repitan posiciones
            a = random.randint(0, 51)

        if a not in posicionescartas:
            posicionescartas.append(a)
            cartastotales.append(Mazo[a])

    for i in cartastotales: #Sacar las cartas que ya van para los jugadores
        Mazo.remove(i)


    for i in range(5):
        CartasP1.append(cartastotales[i])

    for i in range(5,10):

       CartasP2.append(cartastotales[i])


    CartasJ2=" ".join(str(x) for x in CartasP2)

    conn.send(str.encode(CartasJ2))
    print("Sus cartas son:")
    print(CartasP1)

    while True:

        if(contador%2==0):
            if(control!=0):
                print("Ingrese 'a'para tomar la carta del mazo, ingrese 'b' si desea tomar la carta del oponente")
                Respuesta=input()
            if(control==0 or Respuesta=='a'):
                print("La carta del mazo que le ha tocado es: ")
                esc=random.randint(0,41)
                print(Mazo[esc])
                print("Desea tomar la carta?")
                TomarDM= input()
                if(TomarDM=='si'):

                    print("Cual carta desea cambiar?\nSus cartas están organizadas en posiciones de 1 a 5, favor ingrese la posición")
                    posicionCarta=input()
                    posicionCarta=int(posicionCarta)
                    CartasP1.append(Mazo[esc])
                    Mazo.append(CartasP1[posicionCarta]) #Enviar carta al mazo
                    Mazo.pop(esc)

                #Enviar mazo al cliente

                    MazoJ2 = " ".join(str(x) for x in Mazo)
                    conn.send(str.encode(MazoJ2)) #Enviándole el mazo
                    Enviar = CartasP1[posicionCarta - 1]
                    CartasP1.pop(posicionCarta - 1)

                    m = Ganar(CartasP1)
                    if (m == "G"):
                        conn.send(str.encode("J1G"))  # Enviándole al oponente
                        EnviarCorreo()
                        win = open("Juego.txt", "w+")
                        win.write("El jugador 2 es un buen jugador")
                        win.close()
                        with pysftp.Connection('192.168.77.42', username='root', password='20150270') as sftp:
                            with sftp.cd('TresDos'):
                                print(sftp.listdir())
                                print(sftp.pwd)
                                sftp.put(R"C:\Users\COMPAQ\PycharmProjects\untitled\Juego.txt")  # cargar archivo
                                sftp.get('Juego.txt', R"C:\Users\COMPAQ\PycharmProjects\untitled\Juego.txt")

                    break

                    conn.send(str.encode(Enviar))  # Enviar carta al oponente
                    contador = contador + 1

                if(TomarDM=="no"):
                    MazoJ2 = " ".join(str(x) for x in Mazo)
                    conn.send(str.encode(MazoJ2))  # Enviándole el mazo
                    conn.send(str.encode(Mazo[esc]))  # Enviar carta al oponente
                    contador = contador + 1

            if(Respuesta=="b"):

                print( "Cual carta desea cambiar?\nSus cartas están organizadas en posiciones de 1 a 5, favor ingrese la posición")
                posicionCarta = input()
                posicionCarta = int(posicionCarta)

                CartasP1.append(Cartaop[0])
                Enviar=CartasP1[posicionCarta-1]
                CartasP1.pop(posicionCarta - 1)
                m = Ganar(CartasP1)
                if (m == "G"):
                    conn.send(str.encode("J1G"))  # Enviándole al oponente si se ganó
                    EnviarCorreo()
                    win = open("Juego.txt", "w+")
                    win.write("El jugador 2 es un buen jugador")
                    win.close()
                    with pysftp.Connection('192.168.77.42', username='root', password='20150270') as sftp:
                        with sftp.cd('TresDos'):
                            print(sftp.listdir())
                            print(sftp.pwd)
                            sftp.put(R"C:\Users\COMPAQ\PycharmProjects\untitled\Juego.txt")  # cargar archivo
                            sftp.get('Juego.txt', R"C:\Users\COMPAQ\PycharmProjects\untitled\Juego.txt")

                break
                conn.send(str.encode(Enviar))  # Enviar carta al oponente
                contador=contador+1

            print("Sus cartas son: ")
            print(CartasP1)
            print("Turno del jugador 2...")


        if(contador%2!=0):
            data = conn.recv(1024)
            recibido = data[:].decode("utf-8")
            Oponente=recibido.split()
            if (recibido == "J2G"):
                print("El jugador 2 ha ganado. Mejor suerte para la próxima")
                break

            if(len(Oponente)==1):
                print("La carta que ha arrojado el oponente es:")
                print(Oponente[0])
                Cartaop=Oponente
                contador=contador+1
                control=control+1

            if(len(Oponente)>5):
                Mazo=Oponente





def accepta_socket():
    conn, address = s.accept()
    print("Empieza el juego")
    envia_juego(conn)
    conn.close()

def crea_socket():
    try:
        global host
        global puerto
        global s
        host = ""
        puerto = 2222
        s = socket.socket()

    except socket.error as msg:
        print("Error creando el socket: " + str(msg))


# Enlaza el socket y escucha por conexiones
def enlaza_socket():
    try:
        global host
        global puerto
        global s

        s.bind((host, puerto))
        s.listen(5)

    except socket.error as msg:
        print("Error enlazando el socket: " + str(msg) + "\n" + "Retrying...")
        enlaza_socket()


# Establece conexión con un cliente (socket debe de estar escuchando)


# Envía el juego
def envia_juego(conn):
    conn.send(str.encode("Empieza el juego"))
    Juego(conn)


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
    if len(unicos)==2:
        x = unicos.pop()
        c = valor.count(x)
        if c == 2 or c==3:
            print("Usted ha ganado")
            return 'G' # gano


def main():
    crea_socket()
    enlaza_socket()
    accepta_socket()


main()
