#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 10:51:51 2022

@author: michael
"""

import xml.etree.ElementTree as ET


ROUTES_FILE = "leaderboard/data/TCP_training_routes/routes_town01.xml"
FACTOR = 1.2

WEATHER = {
    "cloudiness": (0, 100),
    "precipitation": (0, 100),
    "precipitation_deposits": (0, 100),
    "wind_intensity": (0, 1),
}


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


tree = ET.parse(ROUTES_FILE)
root = tree.getroot()

for route in root.findall("route"):
    weather = route.find("weather")
    for attr, (min_, max_) in WEATHER.items():
        weather.set(
            attr, str(clamp(float(weather.get(attr)) * FACTOR, min_, max_))
        )

tree.write(ROUTES_FILE.replace(".xml", "_mutated.xml"))
