# Dependencies:
# sudo pip install numpy scipy divisi2 csc-pysparse

import os, sys
import time
# from multiprocessing import Process, Queue
import divisi2
from divisi2.sparse import SparseMatrix

# 458293 users
# 17700  movies
# Training set size: 102416306
# Testing set size:  2749898

TRAINING_FILENAME = "all_um.dta"
TESTING_FILENAME = "qual_um.dta"
OUTPUT_FILENAME = "submission3.dta"
FILESIZE = os.stat(TRAINING_FILENAME).st_size
NUM_USERS = 458293
NUM_MOVIES = 17770
NUM_TRAINING = 102416306
NUM_TESTING = 2749898
NUM_COMPONENTS = 100
INCR = 1000

def add_data_to_matrix(mat):
    f_training = open(TRAINING_FILENAME, 'r')
    print "Loading data..."
    i = 0
    j = 0
    start_time = time.time()
    for line in f_training:
        user, movie, date, rating = line.strip().split()
        mat[int(user)-1, int(movie)-1] = float(rating)
        i += 1
        if i % (NUM_TRAINING / INCR) == 0:
            j += 100.0 / INCR
            sys.stdout.write("\r%.1f%% done, %d ratings inserted (elapsed time: %f s)." % (j, i, time.time() - start_time))
            sys.stdout.flush()
    print "Data loaded."
    f_training.close()

def learn(mat):
    print "Starting learning process..."
    start_time = time.time()
    concept_axes, axis_weights, feature_axes = mat.svd(k=NUM_COMPONENTS)
    print "Matrix decomposition complete (elapsed time: %f s)." % (time.time() - start_time)
    start_time = time.time()
    predictions = divisi2.reconstruct(concept_axes, axis_weights, feature_axes)
    print "Matrix reconstruction (elapsed time: %f s)." % (time.time() - start_time)
    print "Learning process complete."
    return predictions

def predict(mat):
    f_testing = open(TESTING_FILENAME, 'r')
    f_out = open(OUTPUT_FILENAME, 'w')
    print "Making %d predictions..." % NUM_TESTING
    start_time = time.time()
    i = 0
    j = 0
    for line in f_testing:
        user, movie, date = line.strip().split()
        f_out.write(str(mat.entry_named(int(user), int(movie))) + '\n')
        i += 1
        if i % (NUM_TESTING / INCR) == 0:
            j += 100.0 / INCR
            sys.stdout.write("\r%.1f%% done (elapsed time: %f s)." % (j, time.time() - start_time))
            sys.stdout.flush()
    f_testing.close()
    print "Predictions complete (elapsed time: %f s)." % (time.time() - start_time)
    f_out.close()

if __name__=='__main__':
    training_mat = SparseMatrix((NUM_USERS, NUM_MOVIES), range(1,NUM_USERS+1), range(1,NUM_MOVIES+1))
    add_data_to_matrix(training_mat)
    predictions = learn(training_mat)
    predict(predictions)