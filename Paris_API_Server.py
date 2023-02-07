###apt-get install git




###apt install python3-pip
###apt-get install python3-opencv
#apt-get install zbar-tools


#usar sin permisos de administrador 


##pip install mysql-connector-python
###pip install python-snap7
###pip install Flask

#python3 -m pip install pyzbar
####pip install opencv-python      si es linux ###apt-get install python3-opencv

#pip install numpy
#pip install -U Flask




#pip install waitress
#pip install wheel 
#pip install gunicorn


#from crypt import methods

#from asyncio.windows_events import NULL
#from logging import exception
##from asyncio.windows_events import NULL

#from asyncio.windows_events import NULL
import random
#from tkinter import E
#from crypt import methods
from flask import Flask, render_template,jsonify, Response,request
import cv2
import numpy as np
import threading
import queue
#from PIL import Image

from CD_coneccion_BD import Coneccion_BD_CD
#from Servidor.CN_Seguridad_Acceso import Consulta_codigo

from CN_Seguridad_Acceso import Seguridad_Acceso_CN
import protocolo_captura_imagen

import pyzbar.pyzbar as pyzbar

import CN_Seguridad_Acceso
import time


app = Flask(__name__)

direccion_ip_PLC='0.0.0.0'
#######################################################################################################
#Captura de Imagen Camaras Ip y USB
########################################################################################################

url_direccion_Inter_C01_P01='rtsp://admin:Ronald11@192.168.12.4:554/cam/realmonitor?channel=1&subtype=1&unicast=true'
url_direccion_Inter_C01_P01_Lector_QR='rtsp://admin:Ronald11@192.168.12.4:554/cam/realmonitor?channel=1&subtype=0&unicast=true'
url_direccion_Cam_C01_P01='rtsp://admin:ECIOVL@192.168.70.62:554/Streaming/Channels/1'
url_direccion_Cam_C01_P01_Lector_QR='rtsp://admin:ECIOVL@192.168.70.62:554/subStreaming/Channels/2'
url_direccion_Cam_C01_P02='rtsp://admin:Hik12345@192.168.70.61:554/cam/realmonitor?channel=1&subtype=0&unicast=true'
url_direccion_Cam_C01_P03='rtsp://admin:Hik12345@192.168.50.32:554/Sreaming/Channels/201'
url_direccion_Cam_C01_P04='rtsp://admin:Hik12345@192.168.50.30:554/subStreaming/Channels/101'
url_direccion_Cam_C01_P05='rtsp://admin:Hik12345@192.168.50.31:554/Sreaming/Channels/201'
url_direccion_Cam_C01_P06='rtsp://admin:Hik12345@192.168.50.52:554/Sreaming/Channels/201'

Intercomunicador_C01_P01 = cv2.VideoCapture(url_direccion_Inter_C01_P01)
Cam_C01_P01 = cv2.VideoCapture(url_direccion_Cam_C01_P01)# Ubicado interior del pasadiso puertacalle
Cam_C01_P02 = cv2.VideoCapture(url_direccion_Cam_C01_P02)# ubicador en la calle puerta
Cam_C01_P03 = cv2.VideoCapture(url_direccion_Cam_C01_P03)# Ubicado al interior de la cochera
Cam_C01_P04 = cv2.VideoCapture(url_direccion_Cam_C01_P04)# Ubicado calle mirando a 8 de noviembre
Cam_C01_P05 = cv2.VideoCapture(url_direccion_Cam_C01_P05)# Ubicado calle mirando a tumbre
Cam_C01_P06 = cv2.VideoCapture(url_direccion_Cam_C01_P06)# Ubicado en el 4to piso


cola_Intercomunicador_C01_P01=queue.Queue()
cola_Cam_C01_P01=queue.Queue()
cola_Cam_C01_P02=queue.Queue()
cola_Cam_C01_P03=queue.Queue()
cola_Cam_C01_P04=queue.Queue()
cola_Cam_C01_P05=queue.Queue()
cola_Cam_C01_P06=queue.Queue()
#  for cctv Intercomunicador_C01_P01 use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of Intercomunicador_C01_P01
# for local webcam use cv2.VideoCapture(0)

# def Capturar_cola_Intercomunicador_C01_P01():
#     print("start Reveive")
#     #cap = Intercomunicador_C01_P01

#     ret, frame = Intercomunicador_C01_P01.read()

#     frame_respaldo=frame

#     #cola_Cam_C01_P03.put(frame)

#     while True:
#         ret, frame = Intercomunicador_C01_P01.read()
#         if(ret!=False):
#             ret, frame = Intercomunicador_C01_P01.read()
#             cola_Intercomunicador_C01_P01.put(frame)
#             if(cola_Intercomunicador_C01_P01.qsize()>3):
#                 while(cola_Intercomunicador_C01_P01.empty()!=True):
#                     cola_Intercomunicador_C01_P01.get()

#         else:
#             frame=frame_respaldo
#             #flag, buffer = cv2.imencode('.jpg', frame)
#             #frame = buffer.tobytes()
#             cola_Intercomunicador_C01_P01.put(frame)
#             if(cola_Intercomunicador_C01_P01.qsize()>1):
#                 while(cola_Intercomunicador_C01_P01.empty()!=True):
#                     cola_Intercomunicador_C01_P01.get()


def Capturar_cola_Intercomunicador_C01_P01():
    while True:
        try:
            Inter_C01_P01 = cv2.VideoCapture(url_direccion_Inter_C01_P01)# Ubicado interior del pasadiso puertacalle

            print("start Reveive Capturar_cola_Intercomunicador_C01_P01()")
            cap = Inter_C01_P01
            ret, frame = cap.read()
            cola_Intercomunicador_C01_P01.put(frame)
            while ret:
                ret, frame = cap.read()
                cola_Intercomunicador_C01_P01.put(frame)
                if(cola_Intercomunicador_C01_P01.qsize()>1):
                    while(cola_Intercomunicador_C01_P01.empty()!=True):
                        cola_Intercomunicador_C01_P01.get()
        except:
            print("error Capturar_cola_Intercomunicador_C01_P01()")




def Capturar_cola_Cam_C01_P01():
    while True:
        try:
            Cam_C01_P01 = cv2.VideoCapture(url_direccion_Cam_C01_P01)# Ubicado interior del pasadiso puertacalle

            print("start Reveive Capturar_cola_Cam_C01_P01()")
            cap = Cam_C01_P01
            ret, frame = cap.read()
            cola_Cam_C01_P01.put(frame)
            while ret:
                ret, frame = cap.read()
                cola_Cam_C01_P01.put(frame)
                if(cola_Cam_C01_P01.qsize()>1):
                    while(cola_Cam_C01_P01.empty()!=True):
                        cola_Cam_C01_P01.get()
        except:
            print("error Capturar_cola_Cam_C01_P01()")

def Capturar_cola_Cam_C01_P02():
        while True:
            try:
                Cam_C01_P02 = cv2.VideoCapture(url_direccion_Cam_C01_P02)# ubucador en la calle puertacalle
                print("start Reveive Capturar_cola_Cam_C01_P02()")
                cap = Cam_C01_P02
                ret, frame = cap.read()
                cola_Cam_C01_P02.put(frame)
                while ret:
                    ret, frame = cap.read()
                    cola_Cam_C01_P02.put(frame)
                    if(cola_Cam_C01_P02.qsize()>1):
                        while(cola_Cam_C01_P02.empty()!=True):
                            cola_Cam_C01_P02.get()
            except:
                print("error Capturar_cola_Cam_C01_P02()")


def Capturar_cola_Cam_C01_P03():
        while True:
            try:
                Cam_C01_P03 = cv2.VideoCapture(url_direccion_Cam_C01_P03)# Ubicado al interior de la cochera
                print("start Reveive Capturar_cola_Cam_C01_P03()")
                cap = Cam_C01_P03
                ret, frame = cap.read()
                cola_Cam_C01_P03.put(frame)
                while ret:
                    ret, frame = cap.read()
                    cola_Cam_C01_P03.put(frame)
                    if(cola_Cam_C01_P03.qsize()>1):
                        while(cola_Cam_C01_P03.empty()!=True):
                            cola_Cam_C01_P03.get()
            except:
                print("error Capturar_cola_Cam_C01_P03()")

def Capturar_cola_Cam_C01_P04():
        while True:
            try:
                Cam_C01_P04 = cv2.VideoCapture(url_direccion_Cam_C01_P04)# Ubicado calle mirando a 8 de noviembre
                print("start Reveive Capturar_cola_Cam_C01_P04()")
                cap = Cam_C01_P04
                ret, frame = cap.read()
                cola_Cam_C01_P04.put(frame)
                while ret:
                    ret, frame = cap.read()
                    cola_Cam_C01_P04.put(frame)
                    if(cola_Cam_C01_P04.qsize()>1):
                        while(cola_Cam_C01_P04.empty()!=True):
                            cola_Cam_C01_P04.get()
            except:
                print("error Capturar_cola_Cam_C01_P04()")

def Capturar_cola_Cam_C01_P05():
        while True:
            try:
                Cam_C01_P05 = cv2.VideoCapture(url_direccion_Cam_C01_P05)# Ubicado calle mirando a tumbre
                print("start Reveive Capturar_cola_Cam_C01_P05()")
                cap = Cam_C01_P05
                ret, frame = cap.read()
                cola_Cam_C01_P05.put(frame)
                while ret:
                    ret, frame = cap.read()
                    cola_Cam_C01_P05.put(frame)
                    if(cola_Cam_C01_P05.qsize()>1):
                        while(cola_Cam_C01_P05.empty()!=True):
                            cola_Cam_C01_P05.get()
            except:
                print("error Capturar_cola_Cam_C01_P05()")

def Capturar_cola_Cam_C01_P06():
        while True:
            try:
                Cam_C01_P06 = cv2.VideoCapture(url_direccion_Cam_C01_P06)# Ubicado en el 4to piso
                print("start Reveive Capturar_cola_Cam_C01_P06()")
                cap = Cam_C01_P06
                ret, frame = cap.read()
                cola_Cam_C01_P06.put(frame)
                while ret:
                    ret, frame = cap.read()
                    cola_Cam_C01_P06.put(frame)
                    if(cola_Cam_C01_P06.qsize()>1):
                        while(cola_Cam_C01_P06.empty()!=True):
                            cola_Cam_C01_P06.get()
            except:
                print("error Capturar_cola_Cam_C01_P06()")

#######################################################################################################
#Get_frame retornor
########################################################################################################

def get_frame_Intercomunicador_01():
    try:
        while (True):

            if cola_Intercomunicador_C01_P01.empty() !=True:
                frame=cola_Intercomunicador_C01_P01.get()
                flag, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    except:
        print("error get_frame_Intercomunicador_01()")


def get_frame_cola_Cam_C01_P01():

    try:
        while (Cam_C01_P01.isOpened()):

            if cola_Cam_C01_P01.empty() !=True:
                frame=cola_Cam_C01_P01.get()
                flag, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except:
        print("error get_frame_cola_Cam_C01_P01()")


def get_frame_cola_Cam_C01_P02():


    try:
        while (Cam_C01_P02.isOpened()):

            if cola_Cam_C01_P02.empty() !=True:
                frame=cola_Cam_C01_P02.get()
                flag, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except:
        print("error get_frame_cola_Cam_C01_P02()")

def get_frame_cola_Cam_C01_P03():

    try:
        while (Cam_C01_P03.isOpened()):

            if cola_Cam_C01_P03.empty() !=True:
                frame=cola_Cam_C01_P03.get()
                flag, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except:
        print("error get_frame_cola_Cam_C01_P03()")

def get_frame_cola_Cam_C01_P04():

    try:
        while (Cam_C01_P04.isOpened()):

            if cola_Cam_C01_P04.empty() !=True:
                frame=cola_Cam_C01_P04.get()
                flag, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except:
        print("error get_frame_cola_Cam_C01_P04()")

def get_frame_cola_Cam_C01_P05():

    try:
        while (Cam_C01_P05.isOpened()):

            if cola_Cam_C01_P05.empty() !=True:
                frame=cola_Cam_C01_P05.get()
                flag, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except:
        print("error get_frame_cola_Cam_C01_P05()")

def get_frame_cola_Cam_C01_P06():

    try:
        while (Cam_C01_P06.isOpened()):

            if cola_Cam_C01_P06.empty() !=True:
                frame=cola_Cam_C01_P06.get()
                flag, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except:
        print("error get_frame_cola_Cam_C01_P06()")

#######################################################################################################
#Striming de Camaras
########################################################################################################

@app.route('/video_Intercomunicador_C01_P01')
def video_Intercomunicador_C01_P01():
   return Response(get_frame_Intercomunicador_01(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_Cam_C01_P01')
def video_Cam_C01_P01():
    return Response(get_frame_cola_Cam_C01_P01(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_Cam_C01_P02')
def video_Cam_C01_P02():
    return Response(get_frame_cola_Cam_C01_P02(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_Cam_C01_P03')
def video_Cam_C01_P03():
    return Response(get_frame_cola_Cam_C01_P03(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_Cam_C01_P04')
def video_Cam_C01_P04():
    return Response(get_frame_cola_Cam_C01_P04(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_Cam_C01_P05')
def video_Cam_C01_P05():
    return Response(get_frame_cola_Cam_C01_P05(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_Cam_C01_P06')
def video_Cam_C01_P06():
    return Response(get_frame_cola_Cam_C01_P06(), mimetype='multipart/x-mixed-replace; boundary=frame')





#######################################################################################################
#Consultas GET
########################################################################################################

@app.route('/AbrirPuerta',methods=['GET'])
def AbrirPuerta():
    hash_equipo  = request.args.get('hash_equipo')
    numPuerta  = request.args.get('num_puerta')
    estado  = request.args.get('estado_puerta')
    tipo_puerta  = request.args.get('tipo_puerta')

    consulta=Coneccion_BD_CD()
    consulta_SeguridadAcceso=Seguridad_Acceso_CN(direccion_ip_PLC)
    row_equipo=consulta.Operacion_buscar_Hash_equipos(hash_equipo)
    respuesta_bool=consulta_SeguridadAcceso.Modificar_estado_puerta(int(numPuerta),tipo_puerta,row_equipo[3])
    if(respuesta_bool):
    #if(True):
        return jsonify({'estado':True})
    else:
        return jsonify({'estado':False})


@app.route('/ConsultaCredenciales',methods=['GET'])
def Get_consulta_credenciales():

    consulta=Coneccion_BD_CD()

    usuario  = request.args.get('usuario')
    contrasena  = request.args.get('contrasena')
    nombre_equipo  = request.args.get('equipo')

    print(request.args.items)

    if(usuario!=None):

        usuario_actual =consulta.Operacion_Verificar_Credenciales(usuario,contrasena)
        #preguntamos si hay un usuario valido
        if(len(usuario_actual) != 0 ):
            hash_equipo=hash(nombre_equipo)

            list_equipos=consulta.Operacion_buscar_Equipos(usuario_actual[0][0])
            id_ultimo_Registro_Equipos=consulta.id_max_table("Equipos","idEquipos")
            if(list_equipos==None):
                hash_equipo=consulta.Operacion_Crear_Equipo(id_ultimo_Registro_Equipos,hash_equipo,usuario_actual[0][0],nombre_equipo)
            else:

                for item in list_equipos:
                    if(item[4]==nombre_equipo):
                        row_equipo=item

                #if(row_equipo!=NULL):
                if(len(row_equipo)!=0):
                    hash_equipo= row_equipo[1]
                else:
                    #id=consulta.id_max_table("Equipos","idEquipos")
                    hash_equipo=consulta.Operacion_Crear_Equipo(id_ultimo_Registro_Equipos,hash_equipo,usuario_actual[0][0],nombre_equipo)

            codigo_qr=consulta.Operacion_get_codigo_QR_CD(usuario_actual[0][0])[0][2]



            return jsonify({'estado':True,'hash':hash_equipo,'codigo_qr':codigo_qr})

        else:

            return jsonify({'estado':False})
    else:
        return jsonify({'estado':None})

@app.route('/getNewQR',methods=['GET'])
def Get_new_codigo_qr():

    consulta=Coneccion_BD_CD()

    hash  = request.args.get('hash')


    print("Hash de cliente consultando a Paris "+ str(request.args.items))

    if(hash!=None):

        equipo_actual =consulta.Operacion_Verificar_Hash_equipo(hash)
        #preguntamos si hay un usuario valido

        if(len(equipo_actual) != 0 ):

            if(equipo_actual[0][2]==1):
                new_codigo =random.randrange(99999999, 9999999999)
                consulta.Operacion_up_codigo_ClaveSeguridad(equipo_actual[0][3],str(new_codigo))

                print("Nuevo QR --- "+ str(new_codigo))
                return jsonify({'estado':True,'codigo':str(new_codigo)})
            else:

                return jsonify({'estado':False})
        else:

            return jsonify({'estado':False})
    else:
        return jsonify({'estado':None})

@app.route('/Get_QR',methods=['GET'])
def Get_QR():

    consulta=Coneccion_BD_CD()

    hash  = request.args.get('hash')


    print("Hash de cliente consultando a Paris "+ str(request.args.items))

    if(hash!=None):

        equipo_actual =consulta.Operacion_Verificar_Hash_equipo(hash)
        #preguntamos si hay un usuario valido

        if(len(equipo_actual) != 0 ):

            if(equipo_actual[0][2]==1):

                row_tabla_Clave_Seguridad= consulta.Operacion_get_codigo_QR_CD(equipo_actual[0][3])

                print("codigo QR consultado por usuario --- "+str(equipo_actual[0][3])+" --- "+ str(row_tabla_Clave_Seguridad))
                codigo=row_tabla_Clave_Seguridad[0][2]
                return jsonify({'estado':True,'codigo':str(codigo)})
            else:

                return jsonify({'estado':False})
        else:

            return jsonify({'estado':False})
    else:
        return jsonify({'estado':None})



@app.route('/Get_list_usuarios',methods=['GET'])
def Get_list_usuarios():

    consulta=Coneccion_BD_CD()

    hash  = request.args.get('hash')


    print("Hash de cliente consultando a Paris "+ str(request.args.items))

    if(hash!=None):

        equipo_actual =consulta.Operacion_Verificar_Hash_equipo(hash)
        #preguntamos si hay un usuario valido

        if(len(equipo_actual) != 0 ):

            if(equipo_actual[0][2]==1):



                lista_usuarios= consulta.Get_list_usuatios()
                print(lista_usuarios)

            

                return jsonify({'estado':True,'lista':lista_usuarios})
            else:

                return jsonify({'estado':False})
        else:

            return jsonify({'estado':False})
    else:
        return jsonify({'estado':None})




@app.route('/testP',methods=['POS'])
def test_post():
    usuario  = request.args.get('usuario')


    return jsonify({'estado':"False"})

@app.route('/test')
def test():

    return jsonify({'estado':"False"})

@app.route('/')
def index():
    #return "Video streaming home page."
    return render_template('index.html')

####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
#Remplasar todo get
####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
def retorno():
    return app


#detector de movimineto, sirve para dar inicio al encendido y apagado del intercomunicador
#def on_servidor_detector_Movimineto(direccion_camara):

    #protocolo_captura_imagen.capturar_video_Sensor_Movimeinto(direccion_camara)

#detector de codigos QR y seriales
def on_servidor_detector_Codigos():
    hilo1 = threading.Thread(name='Cam_intercomunicador_externo', target=on_camera_01)
    hilo2 = threading.Thread(name='Cam_intercomunicador_interno', target=on_camera_02)
    while(True):

        if hilo1.is_alive() !=True:
                hilo1.start()
        if hilo2.is_alive() !=True:
                hilo2.start()


"""         try:
            camara_interna_=cv2.VideoCapture(url_direccion_Cam_C01_P01)
            ret, frame = camara_interna_.read()
            if(ret!=False):

                if hilo1.is_alive() !=True:
                    hilo1.start()

        except:
            print("error lectura qr")

"""

    # hilo1.start()


# def on_camera_01():
#     list_codigos_escaneados = []
#     while (True):
#         print()
#         frame=cola_Intercomunicador_C01_P01.get()
#         #flag, buffer = cv2.imencode('.jpg', frame)
#         #frame = buffer.tobytes()
#         #protocolo_captura_imagen.detectar_Codigo_QR(frame)

#         codigo_barras = pyzbar.decode (frame) # analizar todos los códigos QR capturados por la cámara
#         codigo = ''
#         # Recorre todos los códigos QR
#         for barcode in codigo_barras:
#             codigo = barcode.data.decode ('utf-8') # Transcodificar los datos
#             print (codigo)
#         if codigo != '' and codigo not in list_codigos_escaneados:
#             ###verificar en la base de datos y registra un log en caso el resultado sea true
#             #apaga el intercomunicador

#             #la puerta empieza apartir del 2
#             print ("***"+codigo)
#             bool_respuesta=CN_Seguridad_Acceso.Seguridad_Acceso_CN.Consulta_codigo(codigo,"2",False,"Puerta")
#             if(bool_respuesta):
#                 time.sleep(3)
#             list_codigos_escaneados.append(codigo)

def on_camera_01():

    while True:
        try:
            print('Iniciando lector de QR camara 01')
            protocolo_captura_imagen.detectar_Codigo_QR(direccion_ip_PLC,url_direccion_Inter_C01_P01_Lector_QR)
            #time.sleep(5)
        except:
            print('error lector de QR camara 01')

def on_camera_02():

    while True:
        try:
            print('Iniciando lector de QR camara 02')
            protocolo_captura_imagen.detectar_Codigo_QR(direccion_ip_PLC,url_direccion_Cam_C01_P01_Lector_QR)
            #time.sleep(5)
        except:
            print('error lector de QR camara 02')







# #######################################################################################################
# #detector de movimiento
# ########################################################################################################


#detector de movimineto, sirve para dar inicio al encendido y apagado del intercomunicador
def on_servidor_detector_Movimineto():
    #1 camara usb para detectar quien toco el sensor
    #protocolo_captura_imagen.capturar_video_Sensor_Movimeinto(1)
    #protocolo_captura_imagen.capturar_video_Sensor_Movimeinto('rtsp://admin:Hik12345@192.168.1.37:554/Sreaming/Channels/02')
    protocolo_captura_imagen.capturar_video_Sensor_Movimeinto(direccion_ip_PLC,url_direccion_Cam_C01_P02)
    print("inicio detector de movimiento para encender el intercomunicador")



# #######################################################################################################
# #main
# ########################################################################################################

if __name__ == '__main__':

    direccion_ip_PLC='192.168.70.20'
    threading.Thread(target=Capturar_cola_Intercomunicador_C01_P01,daemon=True).start()
    threading.Thread(target=Capturar_cola_Cam_C01_P01,daemon=True).start()
    threading.Thread(target=Capturar_cola_Cam_C01_P02,daemon=True).start()
    threading.Thread(target=Capturar_cola_Cam_C01_P03,daemon=True).start()
    threading.Thread(target=Capturar_cola_Cam_C01_P04,daemon=True).start()
    threading.Thread(target=Capturar_cola_Cam_C01_P05,daemon=True).start()
    threading.Thread(target=Capturar_cola_Cam_C01_P06,daemon=True).start()

    #cambiar el url 03 por uno que este activo
    #threading.Thread(target=on_servidor_detector_Movimineto,daemon=True).start()
    threading.Thread(target=on_servidor_detector_Codigos,daemon=True).start()

    #app.run( host="192.168.12.30", port=65322,debug=False)
    app.run( host="192.168.70.10", port=65322,debug=False)
    #app.run(debug=True)
    #while True:
    #    app.run(threaded=True