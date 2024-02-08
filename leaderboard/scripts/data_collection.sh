#!/bin/bash
# Roach data collection
while getopts "p:d:w:s:v:c:r:" flag; do
  case "$flag" in
    p) percentSpeedLimit=$OPTARG;;
    d) numberOfDrivers=$OPTARG;;
    w) numberOfWalkers=$OPTARG;;
    s) trafficManagerSeed=$OPTARG;;
    v) egoVehicle=$OPTARG;;
    c) carlaVersion=$OPTARG;;
    r) routeIndex=$OPTARG;;
  esac
done

carlaVersion=${carlaVersion:-10}

export CARLA_ROOT="../CARLA-$carlaVersion"
export CARLA_SERVER=${CARLA_ROOT}/CarlaUE4.sh
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.${carlaVersion}-py3.7-linux-x86_64.egg
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




# export ROUTES=${@:$OPTIND:1}
# export SCENARIOS=${@:$OPTIND+1:1}

function join_by {
  local d=${1-} f=${2-}
  if shift 2; then
    printf %s "$f" "${@/#/$d}"
  fi
}

SAVE_DIR=$(join_by _ ${@:1:$OPTIND})

export SAVE_PATH="results/$SAVE_DIR"
# export SAVE_PATH=data/CITCoM_data_collect_town01_results/

# export SAVE_PATH=data/data_collect_town01_results_weather_20/

# export TEAM_AGENT=team_code/roach_ap_agent.py
# export TEAM_CONFIG=roach/config/config_agent.yaml
export TEAM_AGENT=team_code/tcp_agent.py
export TEAM_CONFIG="TCP-agent/epoch=59-last.ckpt"
export CHECKPOINT_ENDPOINT=$SAVE_PATH/data_collect_town01_results.json

export ROUTES=leaderboard/data/TCP_training_routes/splitroutes_01/route_$routeIndex.xml
# export ROUTES=leaderboard/data/TCP_training_routes/routes_town01.xml
export SCENARIOS=leaderboard/data/scenarios/all_towns_traffic_scenarios.json
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
--percentSpeedLimit=${percentSpeedLimit:-70} \
--trafficManagerSeed=${trafficManagerSeed:-0} \
--egoVehicle=${egoVehicle:-vehicle.lincoln.mkz2017} \
--color 0 0 0 \
--randomise
