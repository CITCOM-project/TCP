#!/bin/bash
export CARLA_ROOT="../CARLA"
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
export DATA_COLLECTION=True


# TCP evaluation
# export ROUTES=leaderboard/data/evaluation_routes/routes_lav_valid.xml
export ROUTES=leaderboard/data/TCP_training_routes/routes_town01.xml
export ROUTES=leaderboard/data/CITCoM_routes/routes_town01.xml
export TEAM_AGENT=team_code/tcp_agent.py
export TEAM_CONFIG="log/TCP/epoch=59-last.ckpt"
export SCENARIOS=leaderboard/data/scenarios/all_towns_traffic_scenarios.json
export SAVE_PATH=data/results_TCP/
export CHECKPOINT_ENDPOINT=${SAVE_PATH}/results_TCP_screenshots.json

rm -r $SAVE_PATH
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
--numberOfWalkers=0 \
--numberOfDrivers=0 \
--egoVehicle=vehicle.bmw.isetta \
# vehicle.audi.a2 \
# vehicle.audi.tt \
# vehicle.bmw.grandtourer \
# vehicle.yamaha.yzf \
# vehicle.audi.etron \
# vehicle.nissan.micra \
# vehicle.bh.crossbike \
# vehicle.lincoln.mkz2017 \
# vehicle.gazelle.omafiets \
# vehicle.tesla.cybertruck \
# vehicle.dodge_charger.police \
# vehicle.harley-davidson.low_rider \
# vehicle.bmw.isetta \
# vehicle.citroen.c3 \
# vehicle.diamondback.century \
# vehicle.tesla.model3 \
# vehicle.toyota.prius \
# vehicle.seat.leon \
# vehicle.kawasaki.ninja \
# vehicle.nissan.patrol \
# vehicle.mini.cooperst \
# vehicle.mercedes-benz.coupe \
# vehicle.jeep.wrangler_rubicon \
# vehicle.mustang.mustang \
# vehicle.volkswagen.t2 \
# vehicle.chevrolet.impala \
# vehicle.carlamotors.carlacola\
