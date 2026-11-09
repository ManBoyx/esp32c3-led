#!/usr/bin/env python3
"""Tableau en direct des réseaux Wi-Fi et appareils BLE vus par la carte."""
import sys, time, serial
from rich.live import Live
from rich.table import Table
from rich.text import Text

PORT = sys.argv[1] if len(sys.argv) > 1 else '/dev/ttyACM0'
ACTIF_S = 15    # vu depuis moins de N s -> actif
OUBLI_S = 120   # plus vu depuis N s -> retiré
items = {}      # clé -> dict
cycles = 0

def barres(rssi):
    n = max(0, min(5, (rssi + 100) // 10 - 0))
    return '█' * n + '░' * (5 - n)

def table():
    now = time.time()
    t = Table(title=f"Scan en direct — cycle {cycles} — {len(items)} appareils",
              header_style="bold cyan", expand=True)
    for c in ("Type", "Nom", "Adresse", "Signal", "dBm", "Vu il y a", "Statut"):
        t.add_column(c, no_wrap=(c != "Nom"))
    rows = sorted(items.values(), key=lambda d: (now - d['t'] > ACTIF_S, -d['rssi']))
    for d in rows:
        age = now - d['t']
        actif = age <= ACTIF_S
        st = Text("● ACTIF", "bold green") if actif else Text("○ inactif", "dim red")
        nom = Text(d['nom']) if d['nom'] else Text("(sans nom)" if d['k'] == 'B' else "(réseau caché)", "dim")
        col = "green" if d['rssi'] > -60 else "yellow" if d['rssi'] > -80 else "red"
        t.add_row("Wi-Fi" if d['k'] == 'W' else "BLE", nom, Text(d['addr']),
                  Text(barres(d['rssi']), col), str(d['rssi']), f"{age:.0f} s", st)
    return t

def main():
    global cycles
    ser = serial.Serial()
    ser.port, ser.baudrate, ser.timeout = PORT, 115200, 0.2
    ser.dtr = False; ser.rts = False   # évite de redémarrer la carte à l'ouverture
    ser.open()
    with Live(table(), refresh_per_second=4, screen=False) as live:
        while True:
            ligne = ser.readline().decode('utf-8', 'ignore').strip()
            if ligne:
                p = ligne.split('|')
                if p[0] == 'W' and len(p) >= 5:
                    items['W' + p[1]] = dict(k='W', addr=p[1], nom=p[2], rssi=int(p[4]), t=time.time())
                elif p[0] == 'B' and len(p) >= 4:
                    old = items.get('B' + p[1])
                    nom = p[2] or (old['nom'] if old else '')
                    items['B' + p[1]] = dict(k='B', addr=p[1], nom=nom, rssi=int(p[3]), t=time.time())
                elif p[0] == 'C':
                    cycles += 1
                for k in [k for k, d in items.items() if time.time() - d['t'] > OUBLI_S]:
                    del items[k]
            live.update(table())

try:
    main()
except KeyboardInterrupt:
    pass
