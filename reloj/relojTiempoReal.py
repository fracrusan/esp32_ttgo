import socket, struct, utime
from machine import RTC


host = "hora.roa.es"       # El servidor proporciona el EPOCH con referencia a 1900-01-01 00:00:00 UTC (Coordinated Universal Time)
NTP_DELTA = 3155673600     # El RTC (Real Time Clock) del microcontrolador utiliza el EPOCH con referencia a 2000-01-01. Es preciso corregirlo.
                           # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60 = 3155673600

def time():                                              # Función para obtener el EPOCH del servidor
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA                

def settime():                                           # Función para sincronizar el RTC
    t = time()
    tm = utime.localtime(t)                              # Conversión de hora de EPOCH a fecha: año[0], mes[1], día[2], hora[3], minuto[4], segundo[5], díaDeLaSemana[6], díaDelAño[8]
    
    def sec_lastSundayMonth_1hUTC (month):               # Función para conocer el EPOCH de la 01:00:00 UTC del último domingo de un mes de 31 días y poder corregir la hora UTC con la oficial de España
        sw = (tm[0], month, 31, 1, 0, 0, 0, 0, 0)        # El cambio de hora en ESPAÑA se hace los últimos domingos de los meses de marzo y septiembre a la 01:00:00 UTC
        sw_secs = utime.mktime(sw)                       # Horario de verano UTC+2 - horario de invierno UTC+1
        swm = utime.localtime(sw_secs)
        weekday_swm = swm[6]
        if swm[6] != 6:
            sw = (tm[0], month, 31-(swm[6] + 1), 1, 0, 0, 0, 0, 0)
            sw_secs = utime.mktime(sw)
        return sw_secs                                                                                         
    
    if sec_lastSundayMonth_1hUTC (3) <= t < sec_lastSundayMonth_1hUTC (9): # Sincronización con el RTC: año[0], mes[1], día[2], díaDeLaSemana[3], hora[4], minuto[5], segundo[6], subsegundo[7] 
        RTC().datetime((tm[0], tm[1], tm[2], 0, tm[3]+2, tm[4], tm[5], 0)) # Horario de verano                                                            subsegundo -> cuenta atras de 255 a 0
    else:
        RTC().datetime((tm[0], tm[1], tm[2], 0, tm[3]+1, tm[4], tm[5], 0)) # Horario de invierno