import sys

if __name__ == "__main__":
    # open file
    fname = sys.argv[1]

    # store average rating for each movie
    movies = {}

    # read file intelligently (don't load all at once to memory)
    with open(fname, 'r') as FILE:
        ## compute the average rating for each movie ##
        # store current movie id, sum and number for averaging
        curMovieID = 1
        curMovieSum = 0
        curMovieNum = 0

        for line in FILE:
            user,movie,date,rating = map(lambda i: int(i), line.split())
            # if new movie, then store average of previous movie
            if movie != curMovieID:
                movies[curMovieID] = curMovieSum/float(curMovieNum)
                curMovieID = movie
                curMovieSum = rating
                curMovieNum = 1
            # otherwise, then store rating of this movie
            else:
                curMovieSum += rating
                curMovieNum += 1

    ## print all movies and ratings ##
    print movies
