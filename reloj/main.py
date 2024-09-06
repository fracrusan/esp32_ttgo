import conexionStation
import relojTiempoReal
import grafos_st7789
from machine import RTC

minuto_ref = None
diaSemana = {0:'Lunes', 1:'Martes', 2:'Miercoles', 3:'Jueves', 4:'Viernes', 5:'Sabado', 6:'Domingo'}

while True:   
    
    if minuto_ref == None or RTC().datetime()[4:7] == (2,0,0) or RTC().datetime()[4:7] == (3,0,0):
        conexionStation.do_connect("MOVISTAR_54CC","69FJ72E99FJ03Ecruzsanchez")
        print("conectado a la red")
        relojTiempoReal.settime()
        print("HORA recibida")
        grafos_st7789.blanco()
        conexionStation.sta_if.active(False)
    
    if minuto_ref != RTC().datetime()[5]:
        print("Cambio de minuto")
        grafos_st7789.H(RTC().datetime()[4]//10,16,17)
        grafos_st7789.H(RTC().datetime()[4]%10,66,17)
        grafos_st7789.M(RTC().datetime()[5]//10,130,17)
        grafos_st7789.M(RTC().datetime()[5]%10,180,17)
        grafos_st7789.tft.text(grafos_st7789.font, "{:02d}-{:02d}-{}  {}    ".format(RTC().datetime()[2],
                                                                                     RTC().datetime()[1],
                                                                                     RTC().datetime()[0],
                                                                                     diaSemana[RTC().datetime()[3]]),
                               35, 114, grafos_st7789.color_dibujo, grafos_st7789.color_fondo)
        minuto_ref = RTC().datetime()[5]
    
    if RTC().datetime()[6]% 2 == 0:
        grafos_st7789.color = grafos_st7789.color_dibujo
    else:
        grafos_st7789.color = grafos_st7789.color_fondo
    
    grafos_st7789.puntos()