#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:32:32 2022

@author: michael
"""

import pandas as pd
import json
import re
import sys

# RESULTS_FILE = "data/CITCoM_data_collect_town01_results/data_collect_town01_results.json"
RESULTS_FILE = sys.argv[1]

collision_re = re.compile(r"Agent with velocity (\d+\.\d+((e-?\d+)?)) collided against object with type=\w+\.[\w-]+\.\w+ and id=\d+ and velocity (\d+\.\d+((e-?\d+)?)) at")


def get_velocity(collision):
    match = collision_re.match(collision)
    assert match is not None, f"COULD NOT MATCH '{collision}'"
    return float(match.group(1)), float(match.group(4))

routes = {}

with open(RESULTS_FILE) as f:
    results = json.load(f)

for route in results['_checkpoint']['records']:
    if "weather" not in route:
        continue
    index = int(route.pop("index"))
    for weather in route['weather']:
        route[weather] = route['weather'][weather]
    for infraction in route['infractions']:
        route[infraction] = len(route['infractions'][infraction])
        if infraction.startswith("collisions_") and len(route['infractions'][infraction]) > 0:
            ev, ov = get_velocity(route['infractions'][infraction][0])
            # route['collision_ego_velocity'] = ev
            # route['collision_other_velocity'] = ov
    for meta in route['meta']:
        route[meta] = route['meta'][meta]
    for score in route['scores']:
        route[score] = route['scores'][score]
    route.pop('weather')
    route.pop('infractions')
    route.pop('friction')
    route.pop('meta')
    route.pop('scores')
    routes[index] = route

print(routes)

data = pd.DataFrame.from_dict(routes, orient="index")#.dropna()
# for col in data:
#     if len(set(data[col])) == 1:
#         data.drop(col, axis=1, inplace=True)


data.to_csv(RESULTS_FILE.replace(".json", ".csv"))
print(len(data), "data points")
print(data['collisions_vehicle'].sum(), "Vehicle collisions")
