import queue
import cv2
import numpy as np

import threading
#Requisitoto para 'pyzbar' \\python3 -m pip install pyzbar
import pyzbar.pyzbar as pyzbar
import pyzbar.pyzbar as ZBarSymbol
#import CN_Seguridad_Acceso
import time
#import Seguridad_Acceso_CN
import CN_Seguridad_Acceso

list_codigos_escaneados = []

""" def detectar_Codigo_QR(direccion_ip_PLC,url_camara):
    camera = cv2.VideoCapture (url_camara) # video local
    Cam_C01_P02 = cv2.VideoCapture(url_camara)# ubucador en la calle puertacalle
    while True:
        
        ret, frame = camera.read() 
        if ret == False:
            list_codigos_escaneados.clear()
            break

        #if(equipo_estado):  
        #empiesa el tiempo de espera para el apagado de intercomunicador    
        #    hilo1 = threading.Thread(name='Tiempor_regresivo', target=apagar_intercomunicador_tiempo_Regresivo,args= (5,))
         #   hilo1.start() 
            #equipo_estado=False   


        codigo_barras = pyzbar.decode (frame) # analizar todos los códigos QR capturados por la cámara 
        codigo = ''
        # Recorre todos los códigos QR
        for barcode in codigo_barras:
            codigo = barcode.data.decode ('utf-8') # Transcodificar los datos
            print (codigo)
        if codigo != '' and codigo not in list_codigos_escaneados:
            ###verificar en la base de datos y registra un log en caso el resultado sea true
            #apaga el intercomunicador

            local=CN_Seguridad_Acceso.Seguridad_Acceso_CN(direccion_ip_PLC)
            local.Consulta_codigo(codigo,1,"Puerta")
            print ("puerta abierta por qr")
            list_codigos_escaneados.append(codigo)
            
            camera.release()
            cv2.destroyAllWindows()
            break


        cv2.imshow("frame", frame)
        cv2.waitKey(1) """

def detectar_Codigo_QR(direccion_ip_PLC,url_camara):

    cola_Cam_C01_P02=queue.Queue()
    while True:
        try:
            camera = cv2.VideoCapture (url_camara) # video local    Cam_C01_P02 = cv2.VideoCapture(url_camara)# ubucador en la calle puertacalle
            ret, frame = camera.read()
            #print("Empieza lectura de Qr en "+url_camara )
            if ret == False:
                list_codigos_escaneados.clear()
                break
            codigo = ''
            cola_Cam_C01_P02.put(frame)
            if(cola_Cam_C01_P02.qsize()>1):
                #while(ret):
                while(cola_Cam_C01_P02.empty()!=True):
                    codigo_barras = pyzbar.decode (cola_Cam_C01_P02.get())
                    # Recorre todos los códigos QR
                    for barcode in codigo_barras:
                        codigo = barcode.data.decode ('utf-8') # Transcodificar los datos
                        print (codigo)
                    if codigo != '' and codigo not in list_codigos_escaneados:
                        ###verificar en la base de datos y registra un log en caso el resultado sea true
                        #apaga el intercomunicador
                        local=CN_Seguridad_Acceso.Seguridad_Acceso_CN(direccion_ip_PLC)
                        local.Consulta_codigo(codigo,1,"Puerta")
                        print ("puerta abierta por qr")
                        list_codigos_escaneados.append(codigo)
                        camera.release()
                        cv2.destroyAllWindows()
                        break
                    #cv2.imshow("frame", frame)
                    cv2.waitKey(1)
                #print("----------------------------")
        except:
            print("Error camara " + url_camara)








def detectar_Codigo_QR_test(direccion_ip_PLC,name_camara):
    
 
    while True:
        camera = cv2.VideoCapture (name_camara) # video local
        ret, frame = camera.read() 
        if ret == False:
            list_codigos_escaneados.clear()
            break

 

        codigo_barras = pyzbar.decode (frame) # analizar todos los códigos QR capturados por la cámara 
        codigo = ''
        #print (codigo_barras)
        # Recorre todos los códigos QR
        for barcode in codigo_barras:
            #print ("aaaaaaa")
            codigo = barcode.data.decode ('utf-8') # Transcodificar los datos
            print (codigo)
        if codigo != '' and codigo not in list_codigos_escaneados:
            ###verificar en la base de datos y registra un log en caso el resultado sea true


            local=CN_Seguridad_Acceso.Seguridad_Acceso_CN(direccion_ip_PLC)
            local.Consulta_codigo(codigo,1,"Puerta")
        #cv2.imshow("frame", frame)
        cv2.waitKey(1)  
        list_codigos_escaneados.append(codigo)



def capturar_video_InterComunicador(camara):
    cap=cv2.VideoCapture(camara)

    i = 0
    while True:
        ret, frame = cap.read()
        if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if i == 20:
            bgGray = gray
        if i > 20:
            dif = cv2.absdiff(gray, bgGray)
            _, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)
            # Para OpenCV 3
            #_, cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # Para OpenCV 4
            cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(frame, cnts, -1, (0,0,255),2)        
            
            for c in cnts:
                area = cv2.contourArea(c)
                if area > 9000:
                    x,y,w,h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
            #frame = read_barcodes(frame)
            #codigo_barras=pyzbar.decode(frame)
            #print("codig oes :"+codigo_barras)
            #imagen= zbar.Image()
        cv2.imshow('Frame ',frame)
        i = i+1
        if cv2.waitKey(30) & 0xFF == ord ('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def capturar_video_Sensor_Movimeinto(direccion_ip_PLC,camara):

    # EJES (X,Y)
    p1_TOP_Izquierdo=[270,450]
    p2_TOP_Derecho=  [420,450]
    
    p3_LOW_Izquierdo=[270,480]
    p4_LOW_Derecho=  [420,480]
    print('detector de movimiento encendiendo ')
    while True:
        mi_hilo = threading.Thread(target=apagar_intercomunicador_tiempo_Regresivo,args=(direccion_ip_PLC,))
        try:
            cap=cv2.VideoCapture(camara)

            i = 0
            fgbg = cv2.createBackgroundSubtractorMOG2()
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
            while cap.isOpened():

                ret, frame = cap.read()
                if ret == False: break
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Dibujamos un rectángulo en frame, para señalar el estado
                # del área en análisis (movimiento detectado o no detectado)
                cv2.rectangle(frame,(0,0),(frame.shape[1],40),(0,0,0),-1)
                color = (0, 255, 0)
                texto_estado = "Estado: No se ha detectado movimiento"
                # Especificamos los puntos extremos del área a analizar


                #area_pts = np.array([[200,300], [480,320], [520,frame.shape[0]], [50,frame.shape[0]]])
                area_pts = np.array([p3_LOW_Izquierdo,p4_LOW_Derecho, p2_TOP_Derecho, p1_TOP_Izquierdo])
                # Con ayuda de una imagen auxiliar, determinamos el área
                # sobre la cual actuará el detector de movimiento
                imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
                imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
                image_area = cv2.bitwise_and(gray, gray, mask=imAux)
                # Obtendremos la imagen binaria donde la región en blanco representa
                # la existencia de movimiento
                fgmask = fgbg.apply(image_area)
                fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
                fgmask = cv2.dilate(fgmask, None, iterations=2)
                # Encontramos los contornos presentes en fgmask, para luego basándonos
                # en su área poder determina si existe movimiento
                cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

                contador_bool =False
                for cnt in cnts:
                    if cv2.contourArea(cnt) > 200:
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0), 2)
                        texto_estado = "Estado: Alerta Movimiento Detectado!"
                        ##enciende el intercomunicador
                        #True regresa a su estado original de apagado
                        local=CN_Seguridad_Acceso.Seguridad_Acceso_CN(direccion_ip_PLC)
                        local.up_estado_intercomunicador_01(True)
                        print('Se detecto movimiento encendiendo intercomunicador')
                        contador_bool=True


                        #CN_Seguridad_Acceso.up_log_CN(0,"se abrio la puerta 01","","")
                        color = (0, 0, 255)
                # Visuzalizamos el alrededor del área que vamos a analizar
                # y el estado de la detección de movimiento
                cv2.drawContours(frame, [area_pts], -1, color, 2)
                cv2.putText(frame, texto_estado , (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color,2)
                #cv2.imshow('fgmask', fgmask)
                #cv2.imshow("frame", frame)
                cv2.waitKey(1)

                if contador_bool:
                    if mi_hilo.is_alive() !=True:
                        mi_hilo.start()
                        #print("El hilo no está ejecutándose")

                    #else:
                        #print("El hilo está ejecutándose")
                
            cap.release()
            cv2.destroyAllWindows()
        except:
            print('error apagando sensor')


            
def apagar_intercomunicador_tiempo_Regresivo(direccion_ip_PLC):
    tiempo_restante=8
    time.sleep(tiempo_restante)
    #True regresa a su estado original de apagado
    local=CN_Seguridad_Acceso.Seguridad_Acceso_CN(direccion_ip_PLC)
    local.up_estado_intercomunicador_01(False)


def validar():
    print("ddatos")

def capturar_video_camara(camara):
    capture = cv2.VideoCapture(camara)

    while (capture.isOpened()):
        ret, frame = capture.read()
        cv2.imshow('webCam',frame)
        if (cv2.waitKey(1) == ord('s')):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    
    #«01» indica el stream principal, «02» el substream
    ##('rtsp://admin:Hik12345@192.168.1.36:554/Sreaming/Channels/02')
    
    #detectar_Codigo_QR_test(0)
    #capturar_video_camara('rtsp://admin:Hik12345@192.168.12.230:554/cam/realmonitor?channel=1&subtype=0&unicast=true')
    #capturar_video_camara('rtsp://admin:ECIOVL@192.168.12.231:554/Streaming/Channels/02')
    #capturar_video_InterComunicador('rtsp://admin:Hik12345@192.168.50.30:554/Sreaming/Channels/01')
    #while(True):
    #capturar_video_camara('rtsp://admin:Hik12345@192.168.13.179:8080/h264_ulaw.sdp')
    #capturar_video_Sensor_Movimeinto('rtsp://admin:Hik12345@192.168.1.36:554/Sreaming/Channels/02')
    #capturar_video_Sensor_Movimeinto('192.168.12.4','rtsp://admin:Hik12345@192.168.12.230:554/cam/realmonitor?channel=1&subtype=1&unicast=true')
    #capturar_video_Sensor_Movimeinto('192.168.12.4','rtsp://admin:Hik12345@192.168.12.230:554/cam/realmonitor?channel=1&subtype=1&unicast=true')
    #capturar_video_camara('rtsp://admin:ECIOVL@192.168.70.62:554/Streaming/Channels/02')
    #capturar_video_camara('rtsp://admin:Ronald11@192.168.12.4:554/cam/realmonitor?channel=1&subtype=0&unicast=true')
    detectar_Codigo_QR('192.168.12.4','rtsp://admin:ECIOVL@192.168.70.62:554/subStreaming/Channels/1')
    #detectar_Codigo_QR_test('192.168.70.21','rtsp://admin:Ronald11@192.168.12.4:554/cam/realmonitor?channel=1&subtype=1&unicast=true')
    #detectar_Codigo_QR('192.168.12.4','rtsp://admin:ECIOVL@192.168.12.231:554/Streaming/Channels/2')
    