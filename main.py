#
# Main engine for running matrix factorization.
#

import constants, DataParser
import math, scipy, json, numpy, os.path, pdb

def stop(probeData, mMatrixT, uMatrix, movieMapping, userMapping, rmseFile):
  '''
  Returns if we should stop doing more iterations of alternating. One iteration
  is defined as solving for both U and M.
  @param probeData is a dictionary mapping movie ID -> user ID -> rating
      for our data in our probe.
  @param predictionMatrix is an actual matrix variable. It's (movies x users)
  @param movieMapping mapping from movie id -> movie index.
  @param userMapping mapping from user id -> user index
  '''
  # cumError = 0.
  # ratingCount = 0
  # for movieId in probeData:
  #   for userId in probeData[movieId]:
  #     probeRating = probeData[movieId][userId]
  #     predictedRating =\
  #         predictionMatrix[movieMapping[movieId], userMapping[userId]]
  #     cumError += (probeRating - predictedRating) ** 2
  #     ratingCount += 1
  #
  # rmse = math.sqrt(cumError / ratingCount)
  # print `rmse`
  # rmseFile.write(str(rmse))
  # return rmse < 1.

  cumError = 0.
  ratingCount = 0
  for movieId in probeData:
    for userId in probeData[movieId]:
      probeRating = probeData[movieId][userId]
      predictedRating = numpy.dot(
          mMatrixT[movieMapping[movieId], :],
              uMatrix[:, userMapping[userId]])
      cumError += (probeRating - predictedRating) ** 2
      ratingCount += 1

  rmse = math.sqrt(cumError / ratingCount)
  print `rmse`
  rmseFile.write(str(rmse))
  return rmse < 1.

if __name__ == '__main__':

  # name caches.
  matrixCacheFile = constants.RATINGS_CACHE_FILE
  dictCache = constants.USER_MOVIE_MAPPINGS
  UMatrixFile = constants.U_MATRIX_FILE_BASE
  MMatrixFile = constants.M_MATRIX_FILE_BASE
  iterations = constants.STARTING_ITERATION

  if not os.path.exists(constants.PROBE_DATA_FILE):
    print 'Probe data for stop function not found.'
    exit(1)

  # Get the probe data for stop function.
  probeDataForStopFunction = json.load(open(constants.PROBE_DATA_FILE))

  # Open the file to store RMSEs.
  rmseFile = open(constants.RMSE_FILE, 'w')

  if os.path.exists(matrixCacheFile):

    # get the matrix from the file cache.
    matrices = numpy.load(matrixCacheFile)

    # get the cache of dicts.
    dictCacheFile = open(dictCache)
    dictCacheEntries = json.load(dictCacheFile)

    movies = dictCacheEntries['movies']
    ratings = scipy.sparse.csr_matrix(
        (
            (
                matrices['ratingsData'],
                matrices['ratingsIndices'],
                matrices['ratingsIntptr']
            )
        ),
        shape=matrices['ratingsShape'])
    users = dictCacheEntries['users']

  else:

    # read in training data.
    parser = DataParser.DataParser()

    # ratings array
    movies = parser.movies
    ratings = parser.ratings
    users = parser.users

    numpy.savez_compressed(matrixCacheFile,
        ratingsData = ratings.data,
        ratingsIndices = ratings.indices,
        ratingsIntptr = ratings.indptr,
        ratingsShape = ratings.shape
      )

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

  # make U matrix.
  U = numpy.zeros((constants.F, userCount))

  # identity matrix.
  E = numpy.identity(constants.F)

  keepIterating = True
  while keepIterating:

    # initialize first row with average ratings.
    for movieIndex in range(movieCount):
      movieCol = ratings.getcol(movieIndex)
      nonZeroIndices = movieCol.nonzero()
      M[0, movieIndex] = movieCol[nonZeroIndices].mean()

    UMatrixFileFullPath = UMatrixFile + str(iterations) + '.npy'
    if os.path.exists(UMatrixFileFullPath):
      # We have found a cached version of U.
      U = numpy.load(UMatrixFileFullPath)

    else:

      for userIndex in range(len(users)):

        # the columns of M for that pertain to movies rated by the user.
        userRatingRow = ratings.getrow(userIndex)
        indicesOfMoviesRatedByUser = userRatingRow.nonzero()
        indicesOfMoviesRatedByUserCount = len(indicesOfMoviesRatedByUser[0])
        # columnIndicesofM = indicesOfMoviesRatedByUser[0]
        # print columnIndicesofM;
        #
        # print 'indicesOfMoviesRatedByUser: ' + `indicesOfMoviesRatedByUser`
        # print 'indicesOfMoviesRatedByUserCount: ' + `indicesOfMoviesRatedByUserCount`

        indicesArray = [indicesOfMoviesRatedByUser[1][i] for i in range(
          indicesOfMoviesRatedByUserCount)]
        #m = M[indicesOfMoviesRatedByUser]
        m = [[M[i][j] for j in indicesArray] for i in range(constants.F)]
        m = numpy.matrix(m)

        # ratings made by user.
        r = numpy.matrix([userRatingRow[0, i] for i in indicesArray])

        A = m * m.getT() + constants.LAMBDA * indicesOfMoviesRatedByUserCount * E
        v = m * r.getT()
        userCol = (A.getI() * v).getT()
        U[:, userIndex] = userCol

        #
        # #print 'Finished with user with ID ' + `userIndex`
        # if userIndex == 0 :
        #   print `U`

        if userIndex % 1000 == 0:
          print 'Finished ' +\
                `userIndex` + ' out of ' + `len(users)` + \
                    ' users for iteration ' + `iterations` + '.'

      # save our U matrix.
      numpy.save(UMatrixFile + str(iterations), U)

    # at this point, we have U.
    MMatrixFileFullPath = MMatrixFile + str(iterations) + '.npy'
    if os.path.exists(MMatrixFileFullPath):
      M = numpy.load(MMatrixFileFullPath)
    else:
      for movieIndex in range(len(movies)):

        # get the column of ratings for that movie.
        movieRatingColumn = ratings.getcol(movieIndex)
        indicesOfRaters = movieRatingColumn.nonzero()
        indicesOfRatersCount = len(indicesOfRaters[0])
        print "countNonZeros" + `indicesOfRatersCount`

        # convert indicesOfRaters into a simple array
        indicesArray = [indicesOfRaters[0][i] for i in range(indicesOfRatersCount)]

        # calculate u
        u = [[U[i][j] for j in indicesArray] for i in range(constants.F)]
        u = numpy.matrix(u)

        # ratings for this movie
        r_array = [[movieRatingColumn[j, 0]] for j in indicesArray]
        r = numpy.matrix(r_array)
        print "countNonZerosAgain" + `len(r_array)`

        A = u * u.getT() + constants.LAMBDA * indicesOfRatersCount * E
        v = u * r
        M[:, movieIndex] = (A.getI() * v).getT()

        print 'Finished ' + `movieIndex` + ' out of ' + `len(movies)` + ' movies.'

      numpy.save(MMatrixFile + str(iterations), M)

    print `(M.shape, U.shape)`
    mMatrixT = numpy.matrix(M).getT()
    uMatrix = numpy.matrix(U)

    print 'Just finished iteration ' + `iterations` + '.'

    stop(probeDataForStopFunction, mMatrixT, uMatrix, movies, users, rmseFile)
    if iterations == constants.MAX_ITERATIONS:
      break

    iterations += 1
