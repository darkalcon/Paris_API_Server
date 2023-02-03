
#from cadena_con_SQLserver import conexion

#from asyncio.windows_events import NULL

from math import fabs
from cadena_con_MYSQL import Cadena_mysql
from datetime import datetime



class Coneccion_BD_CD:



    #def __init__(self):

    def consulta_codigo_CD(self,codigo):

        cadena_=Cadena_mysql().coneccion()
        try:

            with cadena_.cursor() as cursor :
                #cursor.execute("SELECT * FROM claves_Seguridad WHERE codigo LIKE '%"+codigo+"%'")
                cursor.execute("SELECT * FROM Claves_Seguridad WHERE codigo = '"+codigo+"'")
                claves_seguridad=cursor.fetchall()
                cursor.close()

                if claves_seguridad==[]:
                    return None
                else:
                    return claves_seguridad


        except Exception as e:
        # Atrapar error
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return None

        finally:

            cadena_.close()

    def Operacion_Verificar_Credenciales(self,usuario,contrasena):

        cadena_=Cadena_mysql().coneccion()
        try:

            with cadena_.cursor() as cursor :

                cursor.execute("SELECT * FROM Usuario WHERE nombre_clave = '"+usuario+"' and contrasena = '"+contrasena+"'")
                resultado=cursor.fetchall()
                cursor.close()
                cadena_.close()
                return resultado


        except Exception as e:
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return e

        finally:

            cadena_.close()

    def Operacion_Verificar_Hash_equipo(self,hash_equipo):

        cadena_=Cadena_mysql().coneccion()
        try:

            with cadena_.cursor() as cursor :

                cursor.execute("SELECT * FROM Equipos WHERE hash_equipo = '"+hash_equipo+"'")
                resultado=cursor.fetchall()
                cursor.close()
                cadena_.close()
                return resultado


        except Exception as e:
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return e

        finally:

            cadena_.close()

    def Operacion_up_codigo_ClaveSeguridad(self,id_user,new_qr):

        cadena_=Cadena_mysql().coneccion()
        try:

            with cadena_.cursor() as cursor :

                sql = "UPDATE Claves_Seguridad SET codigo = '"+new_qr+"' WHERE iD_usuaro = '"+str(id_user)+"'"

                cursor.execute(sql)

                cadena_.commit()

                cursor.close()
                cadena_.close()
                return True


        except Exception as e:
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return e

        finally:

            cadena_.close()

    def id_max_table(self,nombre_tabla,nombre_id):
            cadena_=Cadena_mysql().coneccion()
            try:

                with cadena_.cursor() as cursor :
                    cursor.execute("SELECT MAX("+nombre_id +") AS id FROM "+nombre_tabla+"")
                    resultado=cursor.fetchall()
                    cursor.close()
                    cadena_.close()
                    return int(resultado[0][0])

            except Exception as e:

                print("Ocurrió un error al conectar a SQL Server: ", e)
                return 0

            finally:

                cadena_.close()

    def Operacion_Crear_Equipo(self,id_ultimo_registro,hash_equipo,id_usuario,nombre_equipo):

        
        

        cadena_=Cadena_mysql().coneccion()
        try:


            with cadena_.cursor() as cursor :



                #cursor.execute("SELECT * FROM claves_Seguridad WHERE codigo LIKE '%"+codigo+"%'")
                comando_sql="INSERT INTO Equipos (idEquipos,hash_equipo,activo,id_usuario,nombre_equipo) VALUES (%s,%s,%s,%s,%s)"
                datos=(id_ultimo_registro + 1 , hash_equipo, 1, id_usuario,nombre_equipo)
                cursor.execute(comando_sql,datos)
                cadena_.commit()
                cursor.close()


        except Exception as e:
        # Atrapar error
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return None

        finally:

            cadena_.close()

    def Operacion_buscar_Equipos(self,id_usuario):

        cadena_=Cadena_mysql().coneccion()
        try:

            with cadena_.cursor() as cursor :
                #cursor.execute("SELECT * FROM claves_Seguridad WHERE codigo LIKE '%"+codigo+"%'")
                #cursor.execute("SELECT * FROM Equipos WHERE id_usuario = '"+id_usuario+"'")
                cursor.execute("SELECT * FROM Equipos WHERE id_usuario = '"+str(id_usuario)+"'")
                resultado=cursor.fetchall()
                cursor.close()
                cadena_.close()
                return resultado


        except Exception as e:
        # Atrapar error
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return None

        finally:

            cadena_.close()
    def Operacion_buscar_Hash_equipos(self,hash_equipo):

        cadena_=Cadena_mysql().coneccion()
        try:

            with cadena_.cursor() as cursor :
                #cursor.execute("SELECT * FROM claves_Seguridad WHERE codigo LIKE '%"+codigo+"%'")
                #cursor.execute("SELECT * FROM Equipos WHERE id_usuario = '"+id_usuario+"'")
                cursor.execute("SELECT * FROM Equipos WHERE hash_equipo = '"+str(hash_equipo)+"'")
                resultado=cursor.fetchall()
                cursor.close()
                cadena_.close()
                return resultado[0]


        except Exception as e:
        # Atrapar error
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return None

        finally:

            cadena_.close()

    def Operacion_get_codigo_QR_CD(self,id_usuario):

        cadena_=Cadena_mysql().coneccion()
        try:

            with cadena_.cursor() as cursor :
                cursor.execute("SELECT * FROM Claves_Seguridad WHERE iD_usuaro = '"+str(id_usuario)+"'")
                resultado=cursor.fetchall()
                cursor.close()
                cadena_.close()
                return resultado


        except Exception as e:
        # Atrapar error
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return None

        finally:

            cadena_.close()


    def Get_list_usuatios(self,):

        cadena_=Cadena_mysql().coneccion()
        try:


            with cadena_.cursor() as cursor :
                cursor.execute("SELECT nombre_clave, nombre_completo, codigo FROM Usuario")
                resultado=cursor.fetchall()
                cursor.close()
                cadena_.close()
                return resultado


        except Exception as e:
        # Atrapar error
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return None

        finally:

            cadena_.close()

    def up_log_CD(self,id_Usuario,descripcion,tipo_Evento,nivel_Alarma):

        cadena_=Cadena_mysql().coneccion()
        try:
            id_ultimo=0

            #id_ultimo=ultimo_id_table("ID_log","log")

            with cadena_.cursor() as cursor :
            
                cursor.execute("SELECT MAX(ID_log) FROM Log")
                resultado=cursor.fetchone() #selecciona la siguiente fila
                #resultado=cursor.fetchall() #selecciona todas las filas 
                if((resultado[0]==None) ):                
                    id_ultimo=1
                else:
                    id_ultimo=int(resultado[0])+1
        
                
                sql = "INSERT INTO paris.Log (ID_log,Usuario_ID_usuaro,descripcion,fecha_creado,tipo_evento,nivel_alarma) VALUES (%s, %s, %s, %s, %s, %s);"         
                val =(id_ultimo,id_Usuario,descripcion, str(datetime.today()),tipo_Evento,nivel_Alarma)
        
                cursor.execute(sql,val)          
                
                print(val)

                cadena_.commit()

                cursor.close()
                return True

        except Exception as e:
            # Atrapar error
            print("Ocurrió un error al conectar a SQL Server: ", e)
            return False
        
        finally:
            
            cadena_.close()



if __name__ == "__main__" :

    consulta=Coneccion_BD_CD()
   # tem=str(consulta.Operacion_up_codigo_ClaveSeguridad(0,"4444444444444"))
   # tem2=str(consulta.Operacion_Crear_Equipo(5,"sadfad",4,"test"))
    #print(tem)
    #print(tem2)
    #consulta2=Coneccion_BD_CD()
    #consulta2.up_log_CD(0,"se abrio la puerta 01","","")

    print(consulta.Get_list_usuatios())
