#!/bin/bash
export CARLA_ROOT=/home/michael/Documents/CITCoM/carla/CARLA
export CARLA_SERVER=${CARLA_ROOT}/CarlaUE4.sh
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:leaderboard
export PYTHONPATH=$PYTHONPATH:leaderboard/team_code
export PYTHONPATH=$PYTHONPATH:scenario_runner

export LEADERBOARD_ROOT=leaderboard
export CHALLENGE_TRACK_CODENAME=SENSORS
export PORT=2000
export TM_PORT=8000
export DEBUG_CHALLENGE=0
export REPETITIONS=1 # multiple evaluation runs
export RESUME=True
export DATA_COLLECTION=False


# Roach data collection
export ROUTES=$1
export SCENARIOS=$2
export SAVE_PATH=$3
# export ROUTES=leaderboard/data/CITCoM_routes/routes_town01.xml
# export SCENARIOS=leaderboard/data/CITCoM_scenarios/all_towns_traffic_scenarios.json
# export SAVE_PATH=data/CITCoM_data_collect_town01_results/
# export ROUTES=leaderboard/data/TCP_training_routes/routes_town01_weather_20.xml
# export SCENARIOS=leaderboard/data/scenarios/all_towns_traffic_scenarios.json
# export SAVE_PATH=data/data_collect_town01_results_weather_20/

export TEAM_AGENT=team_code/roach_ap_agent.py
export TEAM_CONFIG=roach/config/config_agent.yaml
export CHECKPOINT_ENDPOINT=$SAVE_PATH/data_collect_town01_results.json



python3 ${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator.py \
--scenarios=${SCENARIOS}  \
--routes=${ROUTES} \
--repetitions=${REPETITIONS} \
--track=${CHALLENGE_TRACK_CODENAME} \
--checkpoint=${CHECKPOINT_ENDPOINT} \
--agent=${TEAM_AGENT} \
--agent-config=${TEAM_CONFIG} \
--debug=${DEBUG_CHALLENGE} \
--record=${RECORD_PATH} \
--resume=${RESUME} \
--port=${PORT} \
--trafficManagerPort=${TM_PORT} \
--trafficManagerSeed=200 \
--percentSpeedLimit=$4 \
--numberOfDrivers=$5 \
--numberOfWalkers=$6
# --routeScenario=RouteScenario_85
