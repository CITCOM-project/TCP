import numpy as np
import pandas as pd
import scipy
from enum import Enum

from causal_testing.testing.estimators import LinearRegressionEstimator, LogisticRegressionEstimator
from causal_testing.testing.causal_test_outcome import SomeEffect, NoEffect
from causal_testing.json_front.json_class import JsonUtility
from causal_testing.testing.estimators import Estimator
from causal_testing.specification.scenario import Scenario
from causal_testing.specification.variable import Input, Output


inputs = [
    {"name": "percentage_speed_limit", "type": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "cloudiness", "type": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "fog_density", "type": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "fog_distance", "type": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "fog_falloff", "type": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "number_of_drivers", "type": int, "distribution": scipy.stats.rv_discrete(name="drivers", values=(range(0, 200), [1/200]*200))},
    {"name": "number_of_walkers", "type": int, "distribution": scipy.stats.rv_discrete(name="drivers", values=(range(0, 200), [1/200]*200))},
    {"name": "precipitation", "type": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "precipitation_deposits", "type": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "sun_altitude_angle", "type": float, "distribution": scipy.stats.uniform(0, 180)},
    {"name": "sun_azimuth_angle", "type": float, "distribution": scipy.stats.uniform(0, 180)},
    {"name": "wetness", "type": float, "distribution": scipy.stats.uniform(0, 100)},
    {"name": "wind_intensity", "type": float, "distribution": scipy.stats.uniform(0, 1)}
]


Status = Enum('Status', ['Completed', 'Failed', 'Failed - Agent timed out'])

outputs = [
    {"name": "collisions_layout", "type": int},
    # {"name": "collisions_pedestrian", "type": int},
    {"name": "collisions_vehicle", "type": int},
    {"name": "red_light", "type": int},
    {"name": "route_length", "type": float},
    {"name": "route_timeout", "type": float},
    {"name": "score_route", "type": float},
    # {"name": "status", "type": Status},
    # {"name": "stop_infraction", "type": int},
    {"name": "total_steps", "type": int}
]


effects = {
    "NoEffect": NoEffect(),
    "SomeEffect": SomeEffect()
}

estimators = {
    "LinearRegressionEstimator": LinearRegressionEstimator,
    "LogisticRegressionEstimator": LogisticRegressionEstimator
}

# Create input structure required to create a modelling scenario
variables = [Input(i['name'], i['type'], i['distribution']) for i in inputs] + \
                   [Output(i['name'], i['type']) for i in outputs]

vnames = {v.name: v for v in variables}

constraints = [vnames["wind_intensity"].z3 <= 1,
vnames["wind_intensity"].z3 >= 0.3]

# Create modelling scenario to access z3 variable mirrors
modelling_scenario = Scenario(variables, constraints)
modelling_scenario.setup_treatment_variables()
print(modelling_scenario.variables)

mutates = {
    "Increase": lambda x: modelling_scenario.treatment_variables[x].z3 >
                          modelling_scenario.variables[x].z3,
    "Plus5": lambda x: modelling_scenario.treatment_variables[x].z3 ==
                          modelling_scenario.variables[x].z3 + 5,
    "Plus10": lambda x: modelling_scenario.treatment_variables[x].z3 ==
                          modelling_scenario.variables[x].z3 + 10,
    "Plus20": lambda x: modelling_scenario.treatment_variables[x].z3 ==
                          modelling_scenario.variables[x].z3 + 20
}


if __name__ == "__main__":
    args = JsonUtility.get_args()
    json_utility = JsonUtility(args.log_path)  # Create an instance of the extended JsonUtility class
    json_utility.set_path(args.json_path, args.dag_path, args.data_path)  # Set the path to the data.csv, dag.dot and causal_tests.json file

    # Load the Causal Variables into the JsonUtility class ready to be used in the tests
    json_utility.set_variables(inputs, outputs, [])
    json_utility.setup()  # Sets up all the necessary parts of the json_class needed to execute tests

    json_utility.generate_tests(effects, mutates, estimators, args.f)
