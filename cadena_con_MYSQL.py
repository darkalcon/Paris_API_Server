#pip install mysql-connector-python

import mysql.connector.connection 
from mysql.connector import errors

class Cadena_mysql:

    direccion_servidor = '200.20.20.60'
    nombre_bd = 'paris'
    nombre_usuario = 'user'
    #nombre_usuario = 'soporte'
    password = 'Coanqui11@'


    def coneccion(self):

        try:

            con_BD= mysql.connector.connect(host=self.direccion_servidor,database=self.nombre_bd,user=self.nombre_usuario,password=self.password,)

            print("ok coneccion BD")

            return con_BD
        except Exception as e:
        # Atrapar error
            print("Ocurrió un error al conectar a MYSQL: ", e)

if __name__ == "__main__" :
    cadena=Cadena_mysql()
    cadena.coneccion()
    print(cadena.direccion_servidor)
