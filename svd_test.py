# Dependencies:
# sudo pip install numpy scipy
# https://code.google.com/p/pyrsvd/

import os, sys
import time
import numpy as np
from rsvd import RSVD, rating_t

# 458293 users
# 17700  movies
# Training set size: 102416306
# Testing set size:  2749898

FILE_LOC = "/Users/epelz/cs156b_data/"
TRAINING_FILENAME = FILE_LOC + "mu_base0.dta"
PROBE_FILENAME = FILE_LOC + "mu_probe0.dta"
TESTING_FILENAME = FILE_LOC + "qual_um.dta"
OUTPUT_FILENAME = FILE_LOC + "submission3.dta"
FILESIZE = os.stat(TRAINING_FILENAME).st_size
NUM_USERS = 458293
NUM_MOVIES = 17770
NUM_TRAINING = 102416306
NUM_TESTING = 2749898
NUM_COMPONENTS = 2
INCR = 1000
NUM_LEARN_ITER = 100
RATIO_PREDICT_LEARN = 0.1 # what ratio of the iterations should we predict and export

def predict(model,fn=""):
    f_testing = open(TESTING_FILENAME, 'r')
    f_out = open(OUTPUT_FILENAME + fn, 'w')
    print "Making %d predictions..." % NUM_TESTING
    start_time = time.time()
    i = 0
    j = 0
    for line in f_testing:
        user, movie, date = line.strip().split()
        f_out.write(str(model(int(user), int(movie))) + '\n')
        i += 1
        if i % (NUM_TESTING / INCR) == 0:
            j += 100.0 / INCR
            sys.stdout.write("\r%.1f%% done (elapsed time: %f s)." % (j, time.time() - start_time))
            sys.stdout.flush()
    f_testing.close()
    print "Predictions complete (elapsed time: %f s)." % (time.time() - start_time)
    f_out.close()

if __name__=='__main__':
    print "Importing ratings..."
    ratings = np.fromfile(TRAINING_FILENAME, dtype=rating_t)
    print "Importing probes..."
    probeRatings = np.fromfile(PROBE_FILENAME, dtype=rating_t)
    print "running svd..."
    model = RSVD.train(10, ratings, (17770, 458292), probeRatings)
    print "predicting..."
    predict(model)
