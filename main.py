#
# Main engine for running matrix factorization.
#

import constants, DataParser
import scipy, json, numpy, os.path

if __name__ == '__main__':

  # name caches.
  matrixCacheFile = 'cache/matrices.npz'
  dictCache = 'cache/dicts.json'

  if os.path.exists(matrixCacheFile):

    # get the matrix from the file cache.
    matrices = numpy.load(matrixCacheFile)

    # get the cache of dicts.
    dictCacheFile = open(dictCache)
    dictCacheEntries = json.load(dictCacheFile)

    movies = dictCacheEntries['movies']
    ratings = matrices['ratings']
    users = dictCacheEntries['users']

  else:

    # read in training data.
    parser = DataParser.DataParser()

    # ratings array
    movies = parser.movies
    ratings = parser.ratings
    users = parser.users

    numpy.savez_compressed(matrixCacheFile, ratings = ratings)

    # store movies and users as well.
    dictCacheFile = open(dictCache, 'w')
    cacheData = {
        'movies': movies,
        'users': users,
    }
    json.dump(cacheData, dictCacheFile)

  # number of movies, users.
  movieCount = len(movies)
  userCount = len(users)

  # initialize M with random values from 0 to 1.
  M = numpy.random.rand(constants.F, movieCount)

  # initialize first row with average ratings.
  for movieIndex in range(movieCount):
    M[0, movieIndex] = ratings.getcol(movieIndex).mean()

  print `M`
