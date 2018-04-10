# coding: utf-8
import os
import sys
import time


# 'esp8266' or 'win32'
# SYS_PLATFORM = sys.platform

# 'micropython' or 'cpython'
IS_MICROPYTHON = sys.implementation.name == 'micropython'
IS_COMPUTER = sys.implementation.name == 'cpython'

if IS_MICROPYTHON:
    IS_ESP8266 = (os.uname().sysname == 'esp8266')
    IS_ESP32 = (os.uname().sysname == 'esp32')
    import esp
    IS_TTGO_LORA_OLED = (esp.flash_size() > 5000000)

IS_RPi = not (IS_MICROPYTHON or IS_COMPUTER)


# def mac2eui(mac):
#     mac = mac[0:6] + 'fffe' + mac[6:]
#     return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:]


if IS_MICROPYTHON:

    # Node Name
    import machine
    import binascii
    uuid = binascii.hexlify(machine.unique_id()).decode()

    if IS_ESP8266:
        NODE_NAME = 'ESP8266_'
    if IS_ESP32:
        NODE_NAME = 'ESP32_'

    # NODE_EUI = mac2eui(uuid)
    NODE_NAME = NODE_NAME + uuid

    # millisecond
    millisecond = time.ticks_ms


if IS_COMPUTER:

    # Node Name
    import socket
    NODE_NAME = socket.gethostname()

    # millisecond
    millisecond = lambda: time.time() * 1000