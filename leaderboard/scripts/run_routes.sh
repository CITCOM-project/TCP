#!/bin/bash
# @author: michael
for i in {0..299}
do
   bash leaderboard/scripts/data_collection.sh -v vehicle.bmw.isetta -c $1 -r $i
   bash leaderboard/scripts/data_collection.sh -v vehicle.lincoln.mkz2017 -c $1 -r $i
done
