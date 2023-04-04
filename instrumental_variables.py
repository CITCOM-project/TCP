#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:34:58 2023

@author: michael
"""

import pandas as pd
import statsmodels.api as sm

v1_datapath = "data/TCP_random_vehicle.csv"
v2_datapath = "data/results_original_TCP_agent.csv"
inputs = [
    "cloudiness",
    #  No fog in the runs
    # "fog_density",
    # "fog_distance",
    # "fog_falloff",
    "precipitation",
    "precipitation_deposits",
    "sun_altitude_angle",
    "sun_azimuth_angle",
    # "wetness",
    "wind_intensity",
    # "ego_vehicle",
    # "ego_vehicle_color",
    # "ego_vehicle_number_of_wheels",
    # "ego_vehicle_object_type",
    # "ego_vehicle_role_name",
    # "ego_vehicle_sticky_control",
    # "number_of_drivers", # Can't use as an instrument
    # "number_of_walkers", # Can't use as an instrument
    "percentage_speed_limit",
    "route_length",
]


df_modified = pd.read_csv(v1_datapath, index_col=0)
df_modified["Intercept"] = 1
df_original = pd.read_csv(v2_datapath, index_col=0)
df_original["Intercept"] = 1
df_original["number_of_drivers"] = 120
df_original["number_of_walkers"] = 0

data = {}

# Try each input as an instrument
for ip in inputs:
    print(ip, len(set(df_modified[ip])))
    # Calculate ip -> system time
    # using df_modified[[ip]] to calculate total_effect_original is NOT a bug because the
    # routes have the same weather conditions
    total_effect_modified = sm.OLS(
        df_modified["duration_system"], df_modified[[ip, "Intercept"]]
    ).fit()
    total_effect_original = sm.OLS(
        df_original["duration_system"], df_modified[[ip, "Intercept"]]
    ).fit()

    # calculate ip -> game time
    # using df_modified[[ip]] to calculate direct_effect_original is NOT a bug because the
    # routes have the same weather conditions
    direct_effect_modified = sm.OLS(
        df_modified["duration_game"], df_modified[[ip, "Intercept"]]
    ).fit()
    direct_effect_original = sm.OLS(
        df_original["duration_game"], df_modified[[ip, "Intercept"]]
    ).fit()
    
    print("  original", total_effect_original.params[ip], direct_effect_original.params[ip])
    print("  modified", total_effect_modified.params[ip], direct_effect_modified.params[ip])

    # We do not want numbers of walkers and drivers for the original version since these were always the same
    data[ip.replace("_", "\_")] = [
        len(set(df_modified[ip])),
        str(round(total_effect_original.params[ip] / direct_effect_original.params[ip], 2)),
        str(round(total_effect_modified.params[ip] / direct_effect_modified.params[ip], 2)),
    ]

adjusted_modified = sm.OLS(
    df_modified["duration_system"],
    df_modified[
        [
            "duration_game",
            "number_of_drivers",
            "number_of_walkers",
            "Intercept",
        ]
    ],
).fit()
adjusted_original = sm.OLS(
    df_original["duration_system"],
    df_original[
        [
            "duration_game",
            "number_of_drivers",
            "number_of_walkers",
            "Intercept",
        ]
    ],
).fit()


data["Classical adjustment"] = [
    "",
    f"{round(adjusted_modified.params['duration_game'], 2)} {adjusted_modified.conf_int().loc['duration_game'].round(2).to_list()}",
    f"{round(adjusted_original.params['duration_game'], 2)} {adjusted_original.conf_int().loc['duration_game'].round(2).to_list()}",
]



data = (
    pd.DataFrame(data)
    .transpose()
    .rename({0: "No. points", 1: "Original", 2: "Modified"}, axis=1)
)
print(data.style.to_latex())
