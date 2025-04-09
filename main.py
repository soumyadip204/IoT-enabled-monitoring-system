import network
import socket
from machine import Pin, Timer
import dht
import time

# Wi-Fi Access Point Configuration
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP8266-AP', password='12345678')

# Sensor Configuration
sensor = dht.DHT11(Pin(14))  # DHT11 connected to GPIO2

# LED Configuration
temp_led = Pin(4, Pin.OUT)   # Temperature alert LED on GPIO4
hum_led = Pin(5, Pin.OUT)    # Humidity alert LED on GPIO5

# Thresholds
TEMP_THRESHOLD = 30   # 30°C
HUM_THRESHOLD = 50    # 50%

# Global variables to store sensor data
current_temp = 0
current_hum = 0

def read_sensor(timer):
    global current_temp, current_hum
    try:
        sensor.measure()
        current_temp = sensor.temperature()
        current_hum = sensor.humidity()
        
        # Controls LEDs based on thresholds
        temp_led.value(1 if current_temp > TEMP_THRESHOLD else 0)
        hum_led.value(1 if current_hum > HUM_THRESHOLD else 0)
        
    except Exception as e:
        print("Error reading sensor:", e)

# Set up timer to read sensor every 2 seconds
timer = Timer(-1)
timer.init(period=2000, mode=Timer.PERIODIC, callback=read_sensor)

# Web Server Configuration
def web_page():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ESP8266 Sensor Data</title></head>
    <body><h1>Environment Monitor</h1>
    <p>Temperature: <strong>""" + str(current_temp) + """ &deg;C</strong></p>
    <p>Humidity: <strong>""" + str(current_hum) + """ %</strong></p>
    </body></html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

print('Access Point IP:', ap.ifconfig()[0])
print('Waiting for connections...')

while True:
    conn, addr = s.accept()
    print('Client connected from:', addr)
    request = conn.recv(1024)
    conn.send('HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n')
    conn.sendall(web_page())
    conn.close()
