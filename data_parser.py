with open("file.txt") as f:
  f.readline()
  for line in f:
      el = f.split(',')
      # el[0]-user, el[1]-rating, el[2]-date