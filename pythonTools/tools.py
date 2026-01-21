#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 28 11:36:58 2025

@author: kamen
"""

import socket

def print_my_ip():
    """Prints the local machine's external IP address.

    Uses a dummy UDP connection to determine the preferred outbound IP address.
    """
    print([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1],
          [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0], end="")


import serial.tools.list_ports

def serial_ports_list():
    """Lists and returns all available serial ports.

    Returns
    -------
    list
        A list of serial port objects, each containing:
        - device: device path (e.g., '/dev/ttyUSB0')
        - manufacturer: USB manufacturer name
    """
    ports = serial.tools.list_ports.comports()
    print("\n")
    for i, p in enumerate(ports):
        print(f"{i}.   {p.manufacturer}   {p.device}")
    print("")
    return ports


def search_by_manufacturer(ports, mnfact):
    """Finds the first serial port matching a specific manufacturer string.

    Parameters
    ----------
    ports : list
        List of serial port objects (from serial_ports_list())
    mnfact : str
        Manufacturer name prefix (case-sensitive)

    Returns
    -------
    str or None
        Device path (e.g., '/dev/ttyACM0') if found, otherwise None.
    """
    ret_val = None
    for p in ports:
        if str(p.manufacturer).startswith(mnfact):
            ret_val = p.device
            break
    return ret_val
