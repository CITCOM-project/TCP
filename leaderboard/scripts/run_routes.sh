#!/bin/bash
for i in {0..299}
do
   bash leaderboard/scripts/data_collection.sh -v vehicle.bmw.isetta -c 11 -r 1
done
