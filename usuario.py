from enum import Enum
class Estado(Enum):
    BUSCANDO = 1
    COMPRANDO_IDA = 2
    COMPRANDO_IDA_VUELTA = 3

class Registro_Vuelo:
    def __init__(self, vuelo, cant_asientos):
        self.vuelo = vuelo
        self.cant_asientos = cant_asientos
        

class Usuario:
    def __init__(self, chat_id, estado= Estado.BUSCANDO):
        self.chat_id = chat_id
        self.estado = estado
        self.registro_vuelos_comprados = []
        self.__vuelos_temp__ = []
        self.__cant_asientos_temp__ = 0

    def reset(self):
        self.__vuelos_temp__ = []
        self.__cant_asientos_temp__ = 0
        
    