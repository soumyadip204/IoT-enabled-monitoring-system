from machine import Pin
from time import sleep
import dht 

sensor = dht.DHT11(Pin(14))
led_pin = Pin(5, Pin.OUT) #connected with D1
led_pin2 = Pin(4, Pin.OUT) #connected with D2
#sensor = dht.DHT22(Pin(14))

while True:
  try:
    sleep(2)
    
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()

    led_pin.off()
    led_pin2.off()
    
    if temp > 30:
        led_pin.on()
    if hum > 50:
        led_pin2.on()
      
    temp_f = temp * (9/5) + 32.0
    print(f'Temperature: {temp:3.1f}°C / {temp_f:3.1f}°F')
    print(f'Humidity: {hum:3.1f}%')
    
  except OSError as e:
    print('Failed to read sensor.')