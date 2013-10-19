#
# Randomly copies training data from Netflix movie data into repo.
# @author Chi Zeng (chi@chizeng.com)
# Oct. 19, 2013
#

import os, os.path, random

# directory of the original movie data.
originalMovieDataDir = '../netflixData/training_set/'

# directory of the destination files.
destination = os.path.join(os.getcwd(), 'trainingData')

# number of movie files to randomly pick.
numFilesToPick = 500

if __name__ == '__main__':

  # randomly chose the names of `numFilesToPick` files.
  filesToMove = random.sample(os.listdir(originalMovieDataDir), numFilesToPick)

  # actually move the files.
  for fileName in filesToMove:
    src = os.path.join(originalMovieDataDir, fileName)
    dest = os.path.join(destination, fileName)
    os.rename(src, dest)
