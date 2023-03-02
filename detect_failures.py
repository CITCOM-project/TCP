#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 13:49:19 2023

@author: michael
"""

import pandas as pd
import sys
import os
import json
import xml.etree.ElementTree as ET

RESULTS_DIR = sys.argv[1]

routes = ET.parse('leaderboard/data/TCP_training_routes/routes_town01.xml').getroot()

data = pd.read_csv(f"{RESULTS_DIR}/big_data.csv", index_col=0)
failures = data.where(data["status"] == "Failed").dropna()["basename"]

failed_routes = ET.Element('routes')

new_i = 0
for i, d in zip(failures.index, failures):
    with open(f"{RESULTS_DIR}/TCP_training_routes/routes_town01/{d}/data_collect_town01_results.json") as f:
        records = json.load(f)['_checkpoint']['records']
    # print(records[i]['infractions'])
    # failed_routes.append(routes[i])
    routes[i].attrib['id'] = str(new_i)
    new_i += 1
    failed_routes.append(routes[i])
    
    # print(os.listdir(f"{RESULTS_DIR}/TCP_training_routes/routes_town01/{d}")[i])
    # print(i, d)

ET.ElementTree(failed_routes).write(f"{RESULTS_DIR}/failed_routes.xml")
