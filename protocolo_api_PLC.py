#pip install python-snap7

import struct
import time
import snap7

class PLC_editor_estado:

    def __init__(self, _direccion_ip):
            self.direccion_ip = _direccion_ip
            self.num_rack = 0
            self.slot_rack = 0
            self.estado_0_bytearray =bytearray(struct.pack('>f', 0))
            self.estado_1_bytearray =bytearray(struct.pack('>f', 1))

    ####
    # 1 --> intercomunicador
    # 2 --> puerta 01 (puerta lateral izquierda la de personas)
    # 3 --> puerta enrrollable cochera
    # 4 --> puerta 4to piso

    def set_datos_jetson_pins(self,_puerto,_tipo_puente):
        db_num_PLC = 1 #numero de PLC fisicamente unido
        puerto=_puerto #numero de puerto del PLC


        try:

            client = snap7.client.Client()
            client.connect(self.direccion_ip, self.num_rack, self.slot_rack,102) # 102 es el puerto por el cual se comunica el ip

            if(_tipo_puente=='Puerta'):
                client.db_write(db_num_PLC, puerto,self.estado_1_bytearray) #modificar el estado de una compuerta
                time.sleep(0.7)
                client.db_write(db_num_PLC, puerto,self.estado_0_bytearray) #modificar el estado de una compuerta

            elif _tipo_puente=='Intercomunicador_on':
                    client.db_write(db_num_PLC, puerto,self.estado_1_bytearray) #modificar el estado de una compuerta

            elif _tipo_puente=='Intercomunicador_off':
                    client.db_write(db_num_PLC, puerto,self.estado_0_bytearray) #modificar el estado de una compuerta

            elif _tipo_puente=='Enrollable':
                client.db_write(db_num_PLC, puerto,self.estado_1_bytearray) #modificar el estado de una compuerta
                time.sleep(8)
                client.db_write(db_num_PLC, puerto,self.estado_0_bytearray) #modificar el estado de una compuerta

            client.delete
            client.destroy
        except Exception as e:
            # Atrapar error
            print("Ocurrió un error : ", e)


if __name__ == "__main__" :

    plc_instancia= PLC_editor_estado('192.168.70.20')

    # plc_instancia.set_datos_jetson_pins(0,"Puerta")
    plc_instancia.set_datos_jetson_pins(0,"Puerta")

