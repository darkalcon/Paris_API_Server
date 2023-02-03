#import CD_coneccion_BD

from protocolo_api_PLC import PLC_editor_estado

import CD_coneccion_BD


class Seguridad_Acceso_CN:

    def __init__(self,_direccion_ip):
            self.direccion_ip=_direccion_ip
    """
    #pendiente implementar

    def Consulta_codigo(codigo,puerto,estado,tipo_puente):

        consulta=Coneccion_BD_CD()
        item_claveSeguridad=consulta.consulta_codigo_CD(codigo)
        if(item_claveSeguridad!=None):
            #converted_obj = ccnx.convert_to_mysql(item_claveSeguridad)
            row_claveSeguridad=list(item_claveSeguridad)[0]
            if(row_claveSeguridad[7] ==1):
                if(bool(row_claveSeguridad[7])):
                    protocolo_modificarEstado_puertas.set_datos_jetson_pins(puerto,estado,tipo_puente)
                    ##registro del log para cualquier actividad
                    up_log_CN(int(row_claveSeguridad[8]),"se abrio la puerta 01")

                    print(bool(row_claveSeguridad[7]))
            return True
        else:
            return False
        
    """

    ##temporal hasta terminar el de arriba

    def Modificar_estado_puerta(self,num_puerta,puerta,id_usuario):

        local_protocolo_plc=PLC_editor_estado
        local_protocolo_plc.__init__(self,self.direccion_ip)
        try:
            
            consulta=CD_coneccion_BD.Coneccion_BD_CD()
            local_protocolo_plc.set_datos_jetson_pins(self,num_puerta,puerta)
                    ##registro del log para cualquier actividad
                    #up_log_CN(int(row_claveSeguridad[8]),"se abrio la puerta 01")
            consulta.up_log_CN(int(id_usuario),"se abrio la puerta 01","","")
        #CN_Seguridad_Acceso.up_log_CN(0,"se abrio la puerta 01","","")
        #se apaga el intercomunicador despues de abrir la puerta //  1 --> es el puerto del rele 1 el intercomunicador  
        #True regresa a su estado original de apagado

        #protocolo_modificarEstado_puertas.set_datos_jetson_pins("1",True,"Intercomunicador")
            return True
        except:
            return False



    def Consulta_codigo(self,codigo,num_puerta,puerta):

        consulta=CD_coneccion_BD.Coneccion_BD_CD() 
        local_protocolo_plc=PLC_editor_estado
        local_protocolo_plc.__init__(self,self.direccion_ip)
       
        item_claveSeguridad=consulta.consulta_codigo_CD(codigo)
        if(item_claveSeguridad!=None):
            #converted_obj = ccnx.convert_to_mysql(item_claveSeguridad)
            row_claveSeguridad=list(item_claveSeguridad)[0]
            
            ##5 -->estado de la clave de la seguridad 
            if(row_claveSeguridad[5] ==1):
                if(row_claveSeguridad[2]==codigo):
                    #abre la puerta 01 //  2 --> es el puerto del rele 2  
                    #print(num_puerta + row_claveSeguridad[2] +" ==="+codigo)
                    local_protocolo_plc.set_datos_jetson_pins(self,num_puerta,puerta)
                    local_protocolo_plc.set_datos_jetson_pins(self,0,"Intercomunicador_off")
                    ##registro del log para cualquier actividad
                    #up_log_CN(int(row_claveSeguridad[8]),"se abrio la puerta 01")

                    #consulta.up_log_CN(int(row_claveSeguridad[1]),"se abrio la puerta 01","","")
                    
                    #CN_Seguridad_Acceso.up_log_CN(0,"se abrio la puerta 01","","")
                    #se apaga el intercomunicador despues de abrir la puerta //  1 --> es el puerto del rele 1 el intercomunicador  
                    #True regresa a su estado original de apagado

                    #protocolo_modificarEstado_puertas.set_datos_jetson_pins("1",True,"Intercomunicador")

                    print(bool(row_claveSeguridad[5]))
                    return True
                else:
                    return False
            else:
                    return False
            
        else:
            return False



    def up_estado_intercomunicador_01(self,estado):
        #True regresa a su estado original de apagado
        try:

            local_protocolo_plc=PLC_editor_estado
            local_protocolo_plc.__init__(self,self.direccion_ip)

            if(estado):
                local_protocolo_plc.set_datos_jetson_pins(self,0,"Intercomunicador_on")
            else:
                local_protocolo_plc.set_datos_jetson_pins(self,0,"Intercomunicador_off")


            return True
        except:
            return False


    def up_log_CN(self,id_usuario,descripcion,tipo_Evento,nivel_Alarma):
        consulta=CD_coneccion_BD.Coneccion_BD_CD()
        esValido= consulta.up_log_CD(id_usuario,descripcion,tipo_Evento,nivel_Alarma)
        if esValido:
            print("up log exito")
            return True
        else:
            return False


if __name__ == "__main__" :

    local=Seguridad_Acceso_CN('192.168.70.20')
    local.Consulta_codigo("3050867776",1,"Puerta")

    consulta=CD_coneccion_BD.Coneccion_BD_CD()
    print("return base datos "+str(consulta.consulta_codigo_CD("3050867776")))
    #consulta.up_log_CD(0,"se abrio la puerta 01","","")
