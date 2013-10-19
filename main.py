#
# Main engine for running matrix factorization.
#

import DataParser

if __name__ == '__main__':

  # read in training data.
  parser = DataParser.DataParser()

  print `parser.ratings`
