# Jak pracovat s programem

## Funkce
- Připojuje se k WiFi pomocí údajů z CONFIGURATION.txt.
- Získává zeměpisné souřadnice přes http://ip-api.com/json.
- Čte data o počasí z lokálního JSON souboru (testapi.txt).
- Zobrazuje teplotu, vlhkost a popis počasí na 16x2 I2C LCD.
- Automaticky se připojuje znovu k WiFi při ztrátě spojení.

## Co je třeba?
upload následujících souborů na zařízení: main.py, lcd.py, CONFIGURATION.txt, testapi.txt

## Použití
Po spuštění se zařízení:
- Načte konfiguraci z CONFIGURATION.txt.
- Připojí se k WiFi (zkouší až 5×, stav zobrazuje na LCD).
- Získá zeměpisnou šířku a délku podle IP.
- Krátce zobrazí souřadnice.
- Nepřetržitě zobrazuje data o počasí z testapi.txt.
- Pokud se WiFi odpojí, deska se automaticky pokusí připojit znovu.
