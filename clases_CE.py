from json import JSONEncoder

class Usuario(object):
    def __init__(self,ID_usuaro, nombre_clave, nombre_completo,codigo):
        self.ID_usuaro = ID_usuaro
        self.nombre_clave = nombre_clave
        self.nombre_completo = nombre_completo
        self.codigo =codigo


class Log(object):
     def __init__(self,ID_log, Usuario_ID_usuaro, descripcion,fecha_creado,tipo_evento,nivel_alarma):
        self.ID_log = ID_log
        self.Usuario_ID_usuaro = Usuario_ID_usuaro
        self.descripcion = descripcion
        self.fecha_creado =fecha_creado
        self.tipo_evento = tipo_evento
        self.nivel_alarma = nivel_alarma

class Claves_Seguridad(object):
    def __init__(self, ID_clavesSeguridad, Usuario_ID_usuaro,codigo,cantidad_permisos,cantidad_usados,estado_clave,fecha_creado,fecha_inicio,fecha_fin,tipo_clave):
        self.ID_clavesSeguridad = ID_clavesSeguridad
        self.Usuario_ID_usuaro = Usuario_ID_usuaro        
        self.codigo = codigo
        self.cantidad_permisos = cantidad_permisos        
        self.cantidad_usados = cantidad_usados
        self.estado_clave = estado_clave
        self.fecha_creado =fecha_creado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo_clave =tipo_clave       

class Peticion_hacia_servidor(object):
     def __init__(self,id_cliente,operacion,entidad):
         self.id_cliente=id_cliente
         self.operacion=operacion
         self.entidad=entidad

class Respuesta_del_servidor(object):
    def __init__(self,respuesta,entidad) :
        self.respuesta=respuesta
        self.entidad=entidad




class json_Encoder(JSONEncoder):
        def default(self, objeto):
            return objeto.__dict__
