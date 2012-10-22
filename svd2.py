# Dependencies:
# sudo pip install numpy scipy sparsesvd

import os, sys
import time
# from multiprocessing import Process, Queue
import numpy, scipy.sparse
from sparsesvd import sparsesvd

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
NUM_LEARN_ITER = 100

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
    user_mat, axis_weights, movie_mat = sparsesvd(mat, NUM_COMPONENTS)
    print "Matrix decomposition complete (elapsed time: %f s)." % (time.time() - start_time)
    print "Learning process complete."
    return (user_mat, axis_weights, movie_mat)

def learn_iter(mat):
    for i in range(NUM_LEARN_ITER):
        mat = learn(mat)
    return mat

def predict(users_mat, movies_mat):
    f_testing = open(TESTING_FILENAME, 'r')
    f_out = open(OUTPUT_FILENAME, 'w')
    print "Making %d predictions..." % NUM_TESTING
    start_time = time.time()
    i = 0
    j = 0
    for line in f_testing:
        user, movie, date = line.strip().split()
        predicted_rating = numpy.dot(users_mat[:,int(user)-1], movies_mat[:,int(movie)-1])
        f_out.write(str(predicted_rating) + '\n')
        i += 1
        if i % (NUM_TESTING / INCR) == 0:
            j += 100.0 / INCR
            sys.stdout.write("\r%.1f%% done (elapsed time: %f s)." % (j, time.time() - start_time))
            sys.stdout.flush()
    f_testing.close()
    print "Predictions complete (elapsed time: %f s)." % (time.time() - start_time)
    f_out.close()

if __name__=='__main__':
    training_mat = scipy.sparse.lil_matrix((NUM_USERS, NUM_MOVIES))
    add_data_to_matrix(training_mat)
    training_smat = scipy.sparse.csc_matrix(training_mat)
    (user_mat, axis_weights, movie_mat) = learn_iter(training_smat)
    predict(user_mat, movie_mat)