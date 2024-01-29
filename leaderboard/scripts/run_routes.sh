#!/bin/bash
for i in {0..299}
do
   bash leaderboard/scripts/data_collection.sh -v vehicle.bmw.isetta -c 11 -r $i
   bash leaderboard/scripts/data_collection.sh -v vehicle.lincoln.mkz2017 -c 11 -r $i
done
