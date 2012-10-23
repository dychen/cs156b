# Dependencies:
# sudo pip install numpy scipy

import os, sys
import time

# 458293 users
# 17700  movies
# Training set size: 102416306
# Testing set size:  2749898

FILE_LOC = "/Users/epelz/cs156b_data/"
TRAINING_FILENAME = FILE_LOC + "all_um.dta"
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

# From "funny article"
def predictRating_Baseline(user,movie):
    K = 25 #constant

    averageRating = (globalAverage * K + sum(observedRatings)) / (K + len(observedRatings))
    averageUserOffset = (sum(actualRatings) * K - sum(observedRatings)) / (K + len(observedRatings))

    return averageRating + averageUserOffset

def train(user, movie, rating):
    lrate = 0.001 #arbitrarily set according to the paper

    err = lrate * (rating - predictRating(movie, user))
    oldUserValue = userValue[user]
    userValue[user] += err * movieValue[movie]
    movieValue[movie] += err * oldUserValue

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
    user_mat, axis_weights, movie_mat = mat.svd(k=NUM_COMPONENTS)
    print "Matrix decomposition complete (elapsed time: %f s)." % (time.time() - start_time)
    start_time = time.time()
    predictions = divisi2.reconstruct(user_mat, axis_weights, movie_mat)
    print "Matrix reconstruction (elapsed time: %f s)." % (time.time() - start_time)
    print "Learning process complete."
    return predictions

def learn_iter(mat):
    for i in range(NUM_LEARN_ITER):
        mat = learn(mat)

        if i % (RATIO_PREDICT_LEARN * NUM_LEARN_ITER) == 0:
            predict(mat, ("."+str(i)+".dat"))

    return mat

def predict(mat,fn=""):
    f_testing = open(TESTING_FILENAME, 'r')
    f_out = open(OUTPUT_FILENAME + fn, 'w')
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
    predictions = learn_iter(training_mat)
    #predict(predictions)
