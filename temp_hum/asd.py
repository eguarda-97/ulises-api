# Micropython specific libraries
import dht
import machine

# Python libraries
import network
import ntptime
import requests
import sys
import time

# Config
from config import wifi_ssid, wifi_pass, post_url, api_key

# Connect to Wi-Fi
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(wifi_ssid, wifi_pass)
        while not wlan.isconnected():
            machine.idle()

# Sync RTC timer
def sync_time(retries=3):
    for _ in range(retries):
        try:
            ntptime.settime()
            return True
        except Exception:
            time.sleep(1)
    return False

# Main runtime
if __name__ == "__main__":
    try:
        wdt = machine.WDT(timeout=5 * 60 * 1000)

        do_connect()
        wdt.feed()

        sync_time()
        wdt.feed()
        
        dht22 = dht.DHT22(machine.Pin(15))
        time.sleep(2)
        dht22.measure()
        buffer = {"t": dht22.temperature(), "h": dht22.humidity()}

        headers = {
            "Content-Type":  "application/json",
            "User-Agent":    "ESP32-MicroPython",
            "Authorization": "API-Key " + api_key,
            "Connection":    "close"
        }
        print("Sending post request...")
        resp = requests.post(post_url, headers=headers, json=buffer)
        print(resp.status_code)
        print(resp.json())
        resp.close()
    
    except Exception as e:
        print(sys.print_exception(e))

    # Go to sleep
    # print("Going to deep sleep for " + str(sleep_time/1000) + " seconds...")
    rtc = machine.RTC()
    dt = rtc.datetime()
    sleep_time = 3600 - dt[5]*60 - dt[6]
    print(f"Going to deep sleep for {str(sleep_time)} seconds...")
    machine.deepsleep(sleep_time*1000)

