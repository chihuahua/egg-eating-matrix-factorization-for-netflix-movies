#
# Makes dictionary for verifying if we should stop iterating.
# Can only run this if the ratings matrix is cached.
#

import json, numpy, os, os.path, scipy, scipy.sparse
import constants

if __name__ == '__main__':

  if not os.path.exists(constants.RATINGS_CACHE_FILE):
    # no ratings matrix yet.
    print 'You must generate the ratings matrix first.'
    exit(1)

  if not os.path.exists(constants.USER_MOVIE_MAPPINGS):
    # mappings from user ID -> idx and movie ID -> idx do not exist.
    print 'You must generate the mappings first.'
    exit(1)

  if not os.path.exists(constants.PROBE_FILE):
    print 'Could not find probe file.'
    exit(1)

  # get the matrix from the file cache.
  matrices = numpy.load(constants.RATINGS_CACHE_FILE)

  # get the matrix of ratings.
  # (number of users x number of movies)
  ratings = scipy.sparse.csr_matrix(
      (
          (
              matrices['ratingsData'],
              matrices['ratingsIndices'],
              matrices['ratingsIntptr']
          )
      ),
      shape=matrices['ratingsShape'])

  # get the mapping dictionaries.
  dictCacheFile = open(constants.USER_MOVIE_MAPPINGS)
  if not dictCacheFile:
    print 'File open failed.'
    exit(1)

  dictCacheEntries = json.load(dictCacheFile)

  # maps from movie ID -> our movie index.
  moviesMapping = dictCacheEntries['movies']

  # maps from user ID -> user index.
  usersMapping = dictCacheEntries['users']

  try:
    probeFile = open(constants.PROBE_FILE)
  except IOError:
    print 'Probe file coult not be opened.'
    exit(1)

  # stores our ratings. It maps movie ID -> user ID -> rating.
  probeData = {}

  movieIndex = -1
  latestMovieId = -1
  for line in probeFile:
    if line.find(':') != -1:
      # if colon in line, then we have a movie ID.
      movieId = line[:-2]

      if movieId in moviesMapping:
        # We used this movie.
        movieIndex = int(moviesMapping[movieId])
        latestMovieId = movieId
        probeData[latestMovieId] = {}
      else:
        # Don't include the following user ratings since we don't use movie.
        movieIndex = -1

      # This is a movie, not a user ID.
      continue

    if movieIndex == -1:
      # the previous movie ID is not within our training data set.
      continue

    userId = line[:-1]
    if userId not in usersMapping:
      # We did not use this user.
      continue

    userIndex = int(usersMapping[userId])
    probeData[latestMovieId][userId] =\
        ratings[userIndex, movieIndex]

  print `probeData`
  json.dump(probeData, open(constants.PROBE_DATA_FILE, 'w'))
