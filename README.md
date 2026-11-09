**Français** · [English](#english)

# esp32c3-led

Scanner **passif** Wi-Fi + Bluetooth LE sur une carte **ESP32-C3** (MicroPython), avec un tableau en direct dans le terminal.

- `carte/main.py` : tourne sur la carte. Il scanne les réseaux Wi-Fi et les appareils BLE alentour et envoie des lignes texte sur le port USB : `W|bssid|ssid|canal|rssi`, `B|adresse|nom|rssi`, `I|ip|ssid|rssi` (connexion de la carte), `C` (fin de cycle), `E|…` (erreur). La LED (broche 8) s'allume entre deux cycles.
- `pc/tableau.py` : tableau en direct (bibliothèque `rich`) des réseaux et appareils vus : « actif » s'ils ont été vus il y a moins de 15 s, retirés après 120 s.

## Installation
1. Installez MicroPython pour ESP32-C3 sur la carte (firmware « ESP32_GENERIC_C3 » depuis [micropython.org](https://micropython.org/download/ESP32_GENERIC_C3/) : il n'est pas inclus ici).
2. Copiez `carte/secrets.example.py` en `carte/secrets.py`, renseignez votre Wi-Fi, puis copiez `carte/main.py` et `carte/secrets.py` sur la carte (par exemple avec `mpremote`).
3. Côté PC :
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./lance.sh [/dev/ttyACM0]        # Ctrl+C pour quitter
```

`secrets.py` contient votre mot de passe Wi-Fi : il est dans `.gitignore`, ne le versionnez jamais.

## Remarque
Le scan est passif (écoute seulement), mais il liste les adresses matérielles des appareils voisins : utilisez-le chez vous ou avec l'accord des personnes concernées, dans le respect de la loi.

## Licence
[MIT](LICENSE).

---

# English

# esp32c3-led

A **passive** Wi-Fi + Bluetooth LE scanner on an **ESP32-C3** board (MicroPython), with a live table in the terminal.

- `carte/main.py`: runs on the board. It scans nearby Wi-Fi networks and BLE devices and sends text lines over USB: `W|bssid|ssid|channel|rssi`, `B|address|name|rssi`, `I|ip|ssid|rssi` (the board's own connection), `C` (end of cycle), `E|…` (error). The LED (pin 8) lights between cycles.
- `pc/tableau.py`: live table (`rich` library) of the networks and devices seen: "active" if seen less than 15 s ago, dropped after 120 s.

## Installation
1. Install MicroPython for ESP32-C3 on the board ("ESP32_GENERIC_C3" firmware from [micropython.org](https://micropython.org/download/ESP32_GENERIC_C3/); it is not included here).
2. Copy `carte/secrets.example.py` to `carte/secrets.py`, fill in your Wi-Fi, then copy `carte/main.py` and `carte/secrets.py` to the board (for example with `mpremote`).
3. On the PC:
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
./lance.sh [/dev/ttyACM0]        # Ctrl+C to quit
```

`secrets.py` holds your Wi-Fi password: it is in `.gitignore`, never commit it.

## Note
Scanning is passive (listen only), but it lists the hardware addresses of nearby devices: use it at home or with the consent of the people concerned, in accordance with the law.

## License
[MIT](LICENSE).
