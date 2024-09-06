import network

def do_connect(SSID, PASSWORD):
    global sta_if
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        print('Conectando a la red', SSID +"...")
        while not sta_if.isconnected():
            pass