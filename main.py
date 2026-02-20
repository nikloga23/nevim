import network
import requests
import utime
import json
from machine import Pin, I2C
from lcd import Lcd_i2c

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = Lcd_i2c(i2c, cols=16, rows=2)

def load_config():
    try:
        with open("CONFIGURATION.txt") as f:
            return json.load(f)
    except Exception as e:
        lcd.clear()
        lcd.write("Config error")
        print("Config error:", e)
        while True:
            utime.sleep(1)

config = load_config()

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    lcd.clear()
    lcd.write("Connecting WiFi")
    
    attempts = 0
    while not wlan.isconnected() and attempts < 5:
        wlan.connect(config["wifi_ssid"], config["wifi_password"])
        timeout = 5
        while timeout > 0 and not wlan.isconnected():
            utime.sleep(1)
            timeout -= 1
        attempts += 1

    if wlan.isconnected():
        print("WiFi connected")
        return wlan
    else:
        lcd.clear()
        lcd.write("WiFi Failed")
        utime.sleep(3)
        return None

import urequests

def get_location():
    try:
        response = urequests.get("http://ip-api.com/json")
        
        data = response.json()

        response.close()

        if data.get("status") == "success":
            return data["lat"], data["lon"]
        else:
            print("IP API failed:", data)
            return None, None

    except Exception as e:
        print("LOCATION ERROR:", e)
        return None, None

def get_weather(lat, lon):
    try:
        with open("testapi.txt") as f:
            data = json.load(f)

        return {
            "temp": data["current"]["temp"] - 273.15,  # convert Kelvin to C
            "humidity": data["current"]["humidity"],
            "desc": data["current"]["weather"][0]["description"]
        }

    except Exception as e:
        print("Weather FILE error:", e)
        return None

def show_weather(weather):
    lcd.clear()
    if weather:
        lcd.write("T:{:.1f}C H:{}%".format(
            weather["temp"], weather["humidity"]
        ))
        lcd.set_cursor(0,1)
        lcd.write(weather["desc"][:16])
    else:
        lcd.write("Weather error")

wlan = connect_wifi()

if not wlan:
    while True:
        utime.sleep(10)

lat, lon = get_location()

if lat and lon:
    lcd.clear()
    lcd.write("Lat:{:.2f}".format(lat))
    lcd.set_cursor(0,1)
    lcd.write("Lon:{:.2f}".format(lon))
    utime.sleep(5)
else:
    lcd.clear()
    lcd.write("Loc error")
    utime.sleep(3)

while True:

    if not wlan.isconnected():
        wlan = connect_wifi()
        if not wlan:
            continue

    weather = get_weather(lat, lon)
    show_weather(weather)

    for _ in range(600):
        utime.sleep(1)
        if not wlan.isconnected():
            break
