# Scanner passif Wi-Fi + Bluetooth LE -> lignes texte sur le port USB
#   W|bssid|ssid|canal|rssi     B|adresse|nom|rssi     C (fin de cycle)
import network, bluetooth, time
import secrets
from machine import Pin

led = Pin(8, Pin.OUT); led.value(1)
wlan = network.WLAN(network.STA_IF)

def connecter(essais=3):
    for _ in range(essais):
        try:
            wlan.active(False); time.sleep(0.5); wlan.active(True); time.sleep(0.5)
            wlan.connect(secrets.SSID, secrets.PASSWORD)
            t = time.time()
            while not wlan.isconnected() and time.time() - t < 15: time.sleep(0.3)
            if wlan.isconnected(): return True
        except OSError as e:
            print('E|wifi|%s' % e)
    return False

connecter()
ble = bluetooth.BLE(); ble.active(True)
vus = {}

def nom_adv(d):
    i = 0
    while i + 1 < len(d):
        n = d[i]
        if n == 0: break
        if d[i + 1] in (8, 9):
            return bytes(d[i + 2:i + 1 + n]).decode('utf-8', 'ignore')
        i += n + 1
    return ''

def irq(ev, data):
    if ev == 5:  # résultat de scan
        t, addr, _, rssi, adv = data
        a = ':'.join('%02x' % b for b in bytes(addr))
        n = nom_adv(adv)
        if a not in vus or n: vus[a] = (n, rssi)

ble.irq(irq)
while True:
    led.value(0)
    if not wlan.isconnected(): connecter(1)
    if wlan.isconnected():
        print('I|%s|%s|%d' % (wlan.ifconfig()[0], wlan.config('ssid'), wlan.status('rssi')))
    try:
        for s in wlan.scan():
            print('W|%s|%s|%d|%d' % (':'.join('%02x' % b for b in s[1]),
                  s[0].decode('utf-8', 'ignore').replace('|', '/'), s[2], s[3]))
    except OSError as e:
        print('E|wifi|%s' % e)
    vus.clear()
    try:
        ble.gap_scan(4000, 30000, 30000, True)
        time.sleep_ms(4300)
    except OSError as e:
        print('E|ble|%s' % e)
    for a, (n, r) in vus.items():
        print('B|%s|%s|%d' % (a, n.replace('|', '/'), r))
    print('C')
    led.value(1)
