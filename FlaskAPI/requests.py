# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 20:57:00 2022

@author: sonaw
"""

import requests
from data_input import data_in

URL = 'http://127.0.0.1:5000/predict'
headers = {"Content-Tyte":"application/json"}
data = {"input":data_in}

r = requests.get(url = URL, headers=headers, json=data )

r.json()