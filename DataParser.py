#
# Parses data.
#

import constants
import numpy, os, os.path, scipy.sparse

class DataParser:

  def __init__(self):
    '''
    Creates a new data parser.
    '''

    # users is a mapping from user id -> 0-based index.
    # movies is a mapping from movie id -> 0-based index.
    # ratings is an N by M matrix.
    #     N is the number of users.
    #     M is the number of movies.
    self.users, self.movies, self.ratings = self.readData()

  def readData(self):
    '''
    Reads in the relevant data.
    @return 3 things:
        mapping from users -> 0-based user index
        mapping from movies mapping -> 0-based movie index
    '''

    trainingDir = os.path.join(os.getcwd(), constants.TRAINING_DIR)
    fileNames = os.listdir(trainingDir)

    # create empty user, movie mappings -> index.
    users = {}
    movies = {}
    userIndex = -1
    movieIndex = -1

    # mapping from user index to list of movie indices.
    movieIndicesPerUser = {}
    userIndicesPerMovie = {}

    # create sparse matrix of r.
    # mapping: movie index -> [(user index, rating) ... ]
    sparseR = []

    for fileName in fileNames:

      # if this file is not a text file, ignore it.
      if not fileName.endswith('.txt'):
        continue

      # open the file for reading.
      filePath = os.path.join(trainingDir, fileName)
      file = open(filePath)

      # skip first line.
      file.readline()

      # store the movie id.
      movieId = int(fileName[3:-4])

      if movieId not in movies:
        movieIndex += 1

        # create new entry in sparse R for this movie.
        sparseR.append([])
        movies[movieId] = movieIndex

      for line in file:

          # split line into el[0]-user, el[1]-rating, el[2]-date
          elements = line.split(',')

          # if no elements, ignore line.
          if not elements:
            continue

          # store the user Id.
          userId = int(elements[0])
          if userId not in users:
            userIndex += 1
            users[userId] = userIndex
            currentUserIndex = userIndex
          else:
            currentUserIndex = users[userId]

          # record the rating of this user.
          rating = int(elements[1])
          sparseR[movieIndex].append((currentUserIndex, rating))

      # close file.
      file.close()

    if constants.DEBUG:
      print 'Finished making sparse R.'

    # create the ratings matrix.
    ratings = numpy.zeros((len(users), len(movies)))

    for movieIndex, ratingEntries in enumerate(sparseR):
      # record the ratings for this single movie.

      for ratingEntry in ratingEntries:
        # for each rating made by the user, record it.
        userIndex = ratingEntry[0]
        rating = ratingEntry[1]
        ratings[userIndex][movieIndex] = rating

      if constants.DEBUG:
        print 'Finished storing ratings for movie ' + `movieIndex` + '.'

    # turn them into sparse matices.
    ratings = scipy.sparse.csr_matrix(ratings)

    return users, movies, ratings
