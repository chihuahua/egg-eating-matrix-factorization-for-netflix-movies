#
# Contains constants.
#

DEBUG = True

TRAINING_DIR = 'trainingData'

# dimensions of our space.
F = 20

# if we're iterating back and forth from U to M, this is true.
ITERATING = True
STARTING_ITERATION = 6
MAX_ITERATIONS = 30

# lambda for matrix factorization.
LAMBDA = 0.1

# name of the file containing the probe data set.
PROBE_FILE = 'probe.txt'

# name of the file for caching the ratings matrix.
RATINGS_CACHE_FILE = 'cache/matrices.npz'

# name of the file that caches user/movie mappings in json.
USER_MOVIE_MAPPINGS = 'cache/dicts.json'

# name of the file used for stop function probe data.
PROBE_DATA_FILE = 'utility/probeDataStop.json'

U_MATRIX_FILE_BASE = 'cache/UMatrix'
M_MATRIX_FILE_BASE = 'cache/MMatrix'

# name of the file that contains our latest prediction matrix.
PREDICTION_MATRIX_FILE = 'cache/predictionMatrix'

# file to store the RMSEs
RMSE_FILE = 'utility/rmses.txt'
