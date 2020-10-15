import telebot
from vuelos import Aeropuerto, Vuelo
from usuario import Registro_Vuelo, Usuario, Estado
import json
import time
import datetime


import telebot
from vuelos import Aeropuerto, Vuelo
from usuario import Registro_Vuelo, Usuario, Estado
import json
import time
import datetime


aeropuertos_json = json.load(open("aeropuertos.json", "r",encoding="utf-8", errors="ignore"))
resp_bot = json.load(open("resp_bot.json", "r",encoding="utf-8", errors="ignore"))

aeropuertos = []
usuarios = []

for datos_aeropuerto in aeropuertos_json:
    aeropuerto = Aeropuerto(datos_aeropuerto)
    aeropuertos.append(aeropuerto)

for aeropuerto in aeropuertos:
    aeropuerto.generar_vuelos(aeropuertos, min_vuelos=15, max_vuelos=26)
    
def arreglar_texto(texto):
    texto_dividido = texto.split()
    texto_arreglado = "" 
    longitud = len(texto_dividido)

    for i in range( 0, longitud):
        if i == longitud - 1:
            texto_arreglado += texto_dividido[i].capitalize() + "" 
        else:
            texto_arreglado += texto_dividido[i].capitalize() + " " 

    return texto_arreglado

def buscar_aeropuerto_iata(codigo_iata):
    for aeropuerto in aeropuertos:
        if aeropuerto.iata == codigo_iata.upper():
            return aeropuerto
    return None

def usuario_en_lista(chat_id):
    for usuario in usuarios:
        if usuario.chat_id == chat_id:
            return True
    return False

def buscar_usuario(chat_id):
    for u in usuarios:
        if u.chat_id == chat_id:
            return u
    return None

token = "1238450301:AAH6bn7nqmDvQMlmU8--OT6FuQbX7uK5a38"
bot = telebot.TeleBot(token = token)

#region Metodos del bot
#Comienzo de la conversación
@bot.message_handler(commands = ["start"])
def saludar(message):
    bot.send_message(message.chat.id, resp_bot["saludo"] + " " + message.from_user.first_name + " " + message.from_user.last_name) 
    bot.send_message(message.chat.id, "".join(resp_bot["ayuda"]))
    if usuario_en_lista(message.chat.id) == False:
        usuarios.append( Usuario(message.chat.id))

@bot.message_handler(commands = ["help"])
def ayuda(message):
    bot.send_message(message.chat.id, "".join(resp_bot["ayuda"]))

#buscar los vuelos de los aeropuertos
@bot.message_handler(commands = ["list"])
def mostrar_lista_vuelos(message):
    for aeropuerto in aeropuertos:
        bot.send_message(message.chat.id, "*Vuelos desde " +"\("+aeropuerto.iata+"\)" + aeropuerto.nombre+"\(" +aeropuerto.pais +"\)" + " hacia:*", parse_mode="MarkdownV2")        
        for vuelo in aeropuerto.vuelos:
            if vuelo.asientos > 0:
                mensaje = "("+vuelo.aeropuerto_destino.iata+")"+vuelo.aeropuerto_destino.nombre+"(" +vuelo.aeropuerto_destino.pais +")" + ", el día " + vuelo.fecha.isoformat() + " a las " + vuelo.hora.isoformat() + ", asientos disponibles: " + str(vuelo.asientos)
                bot.send_message(message.chat.id, mensaje)


#va a mostrar los vuelos que vayan a ese lugar
@bot.message_handler(commands = ["searchd"])
def buscar_vuelos_destino(message):
    
    mensaje = message.text.split(" ")
    l_aeropuerto = []
    try:
        if len(mensaje) > 1:
            if buscar_aeropuerto_iata(mensaje[1]) != None:
                mensj = mensaje[1].upper()
            else:
                m = message.text
                m = arreglar_texto(m)
                mensj = arreglar_texto(m[8:])
            print(mensj)
            for a in aeropuertos:
                if mensj == a.iata:
                    l_aeropuerto.append(a)
                    
                elif mensj == a.nombre:
                    l_aeropuerto.append(a)

                elif mensj == a.pais:
                    l_aeropuerto.append(a)

                elif mensj == a.ciudad:
                    l_aeropuerto.append(a)

        if l_aeropuerto:
            bot.send_message(message.chat.id, "*Vuelos que van a " + mensj + " son:*", parse_mode="MarkdownV2")
            for aeropuerto in l_aeropuerto:
                for a in aeropuertos:
                    for vuelo in a.vuelos:
                        if aeropuerto.nombre == vuelo.aeropuerto_destino.nombre and vuelo.asientos > 0:
                            m = "Desde " +"("+a.iata+")" + a.nombre + " hasta " +"("+aeropuerto.iata +")" +aeropuerto.nombre + ", el día " + vuelo.fecha.isoformat() + " a las " + vuelo.hora.isoformat() + ", asientos disponibles: " + str(vuelo.asientos)
                            bot.send_message(message.chat.id, m)

    except Exception:
        bot.send_message(message.chat.id, "Ingresó mal la información")


#va a mostrar los vuelos que dispone ese aeropuerto o lugar
@bot.message_handler(commands = ["searcho"])
def buscar_vuelos_origen(message):
    mensaje = message.text.split(" ")
    l_aeropuerto = []
    try:
        if len(mensaje) > 1:
            if buscar_aeropuerto_iata(mensaje[1]) != None:
                mensj = mensaje[1].upper()
            else:
                m = message.text
                m = arreglar_texto(m)
                mensj = arreglar_texto(m[8:])
            for a in aeropuertos:
                if mensj == a.iata:
                    l_aeropuerto.append(a)
                    
                elif mensj == a.nombre:
                    l_aeropuerto.append(a)

                elif mensj == a.pais:
                    l_aeropuerto.append(a)

                elif mensj == a.ciudad:
                    l_aeropuerto.append(a)

        if l_aeropuerto:
            for aeropuerto in l_aeropuerto:
                bot.send_message(message.chat.id, "*Vuelos que dispone " + aeropuerto.nombre + " son:*", parse_mode="MarkdownV2")
                for vuelo in aeropuerto.vuelos:
                    if vuelo.asientos > 0:
                        m = "("+vuelo.aeropuerto_destino.iata+")"+vuelo.aeropuerto_destino.nombre + ", el día " + vuelo.fecha.isoformat() + " a las " + vuelo.hora.isoformat() + ", asientos disponibles: " + str(vuelo.asientos)
                        bot.send_message(message.chat.id, m)

    except Exception:
        bot.send_message(message.chat.id, "Ingresó mal la información")


#comprar vuelo de ida
@bot.message_handler(commands = ["buy_ticket"])
def comprar_vuelo_ida(message):
    usuario = buscar_usuario(message.chat.id)
    if usuario == None:
        usuarios.append( Usuario(message.chat.id, estado= Estado.COMPRANDO_IDA))
        usuario = buscar_usuario(message.chat.id)
    else:
        usuario.estado = Estado.COMPRANDO_IDA
        usuario.reset()

    try:
        mensaje = message.text
        mensaje = mensaje.split(" ")
        if len(mensaje) == 4:
            aeropuerto_origen = buscar_aeropuerto_iata(mensaje[1])
            aeropuerto_destino = buscar_aeropuerto_iata(mensaje[2])
            cant = int(mensaje[3])
            usuario.__cant_asientos_temp__ = cant
            i = 1
            imprimir_mensaje = True
            
            for vuelo in aeropuerto_origen.vuelos:
                if vuelo.aeropuerto_destino == aeropuerto_destino and vuelo.asientos >= cant:
                    if imprimir_mensaje:
                        bot.send_message(message.chat.id, "Escriba el número de la opción que desea comprar")
                        imprimir_mensaje = False
                    m = str(i)+".-Día " + vuelo.fecha.isoformat() + " a las " + vuelo.hora.isoformat() + ", asientos disponibles: " + str(vuelo.asientos)
                    bot.send_message(message.chat.id, m)
                    usuario.__vuelos_temp__.append(vuelo)
                    i += 1
            
            if imprimir_mensaje:
                bot.send_message(message.chat.id, "No existe vuelos para ese lugar")
    except Exception:
        bot.send_message(message.chat.id, "Ingresó mal la información")


#comprar vuelo de ida-vuelta
@bot.message_handler(commands = ["buyrt_ticket"])
def comprar_vuelo_ida_vuelta(message):
    usuario = buscar_usuario(message.chat.id)
    if usuario == None:
        usuarios.append( Usuario(message.chat.id, estado= Estado.COMPRANDO_IDA_VUELTA))
        usuario = buscar_usuario(message.chat.id)
    else:
        usuario.estado = Estado.COMPRANDO_IDA_VUELTA
        usuario.reset()

    try:
        mensaje = message.text
        mensaje = mensaje.split(" ")
        if len(mensaje) == 4:
            aeropuerto_origen = buscar_aeropuerto_iata(mensaje[1])
            aeropuerto_destino = buscar_aeropuerto_iata(mensaje[2])
            cant = int(mensaje[3])
            usuario.__cant_asientos_temp__ = cant
            i = 1
            imprimir_mensaje = True
            
            #Busca cada vuelo que tenga el aeropuerto de origen
            for vuelo in aeropuerto_origen.vuelos:
                #Si el vuelo tiene como destino el aeropuerto destino
                if vuelo.aeropuerto_destino == aeropuerto_destino and vuelo.asientos >= cant:
                    #Busca los vuelos que tenga el aeropurto de destino
                    for vuelo_2 in aeropuerto_destino.vuelos:
                        #Si el vuelo del aeropuerto de destino tiene un viaje de vuelta
                        if vuelo_2.aeropuerto_destino == aeropuerto_origen and vuelo_2.asientos >= cant:
                            #Si ese viaje de vuelta es después del viaje de ida
                            if vuelo.fecha <= vuelo_2.fecha:
                                if vuelo.fecha == vuelo_2.fecha  and vuelo.hora >= vuelo_2.hora :
                                    continue
                                if imprimir_mensaje:
                                    bot.send_message(message.chat.id, "Escriba el número de la opción que desea comprar")
                                    imprimir_mensaje = False
                                m = str(i)+".-Desde "+ aeropuerto_origen.nombre +" hasta"+ aeropuerto_destino.nombre+"el día " + vuelo.fecha.isoformat() + " a las " + vuelo.hora.isoformat() + ", asientos disponibles: " + str(vuelo.asientos)
                                m2 = "Desde "+ aeropuerto_destino.nombre +" hasta"+ aeropuerto_origen.nombre+"el día " + vuelo_2.fecha.isoformat() + " a las " + vuelo_2.hora.isoformat() + ", asientos disponibles: " + str(vuelo_2.asientos)
                                bot.send_message(message.chat.id, m)
                                bot.send_message(message.chat.id, m2)
                                usuario.__vuelos_temp__.append(vuelo)
                                usuario.__vuelos_temp__.append(vuelo_2)
                                i += 1
            
            if imprimir_mensaje:
                bot.send_message(message.chat.id, "No existe vuelos de ida-vuelta para ese lugar")
    except Exception:
        bot.send_message(message.chat.id, "Ingresó mal la información")

@bot.message_handler(func = lambda msg: buscar_usuario(msg.chat.id) != None)
def escoger(message):
    usuario = buscar_usuario(message.chat.id)
    #Para venta de ida
    if usuario.estado == Estado.COMPRANDO_IDA:
        try:
            opcion = int(message.text) - 1
            vuelos = []
            for vuelo in usuario.__vuelos_temp__:
                vuelos.append(vuelo)
            
            
            vuelos[opcion].asientos -= usuario.__cant_asientos_temp__
            usuario.registro_vuelos_comprados.append( Registro_Vuelo(vuelos[opcion], usuario.__cant_asientos_temp__ ))

            bot.send_message(message.chat.id, "Vuelo registrado")
            usuario.reset()
            usuario.estado = Estado.BUSCANDO
        except Exception:
            pass
        
    elif usuario.estado == Estado.COMPRANDO_IDA_VUELTA:
        try:
            opcion = int(message.text) - 1
            vuelos = []
            for vuelo in usuario.__vuelos_temp__:
                vuelos.append(vuelo)
            
            i = 0
            for i in range(0, len(vuelos)):
                if i == opcion:
                    vuelos[i].asientos -= usuario.__cant_asientos_temp__
                    vuelos[i+1].asientos -= usuario.__cant_asientos_temp__
                    usuario.registro_vuelos_comprados.append( Registro_Vuelo(vuelos[i], usuario.__cant_asientos_temp__ ))
                    usuario.registro_vuelos_comprados.append( Registro_Vuelo(vuelos[i+1], usuario.__cant_asientos_temp__ ))

            bot.send_message(message.chat.id, "Vuelo registrado")
            usuario.reset()
            usuario.estado = Estado.BUSCANDO
        except Exception:
            bot.send_message(message.chat.id, "Ingresó mal la información")
        

        

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)