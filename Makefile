clearCache:
	rm -rf cache/*

clearUM:
	rm -rf cache/UMatrix.npy cache/MMatrix.npy

newTraining:
	rm -rf trainingData/*; python obtainData.py

