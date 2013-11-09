clearCache:
	rm -rf cache/*

newTraining:
	rm -rf trainingData/*; python obtainData.py

