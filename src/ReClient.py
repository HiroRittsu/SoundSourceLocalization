#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import usb.core
import usb.util
from tuning import Tuning
from time import sleep

before_angular=0


dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
while(1):
    cliant = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Mic_tuning=Tuning(dev)
    theta=Mic_tuning.direction
    s.connect(('localhost', 11451))
    if(before_angular-theta>=40 or before_angular-theta<=-40):
        s.sendall(str(theta))
    before_angular=theta
