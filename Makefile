default:
	echo "Delete stuff with `make clean`"

clean:
	rm data_collect_town01_results.json
	rm -rf data/*
