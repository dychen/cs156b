from sklearn import linear_model
import time

# Learn #
f_learn = open("all_um.dta", 'r')

input_vector = []
output_vector = []

num_iter = 0
LIMIT = 10000000

start_time = time.time()
for line in f_learn:
    uid, mid, date, rating = line.strip().split()
    input_vector.append([int(uid), int(mid)])
    output_vector.append(int(rating))
    num_iter += 1
    if num_iter >= LIMIT:
        break
print "Read input time: %s s." % (time.time() - start_time)
f_learn.close()

start_time = time.time()
clf = linear_model.LinearRegression()
clf.fit(input_vector, output_vector)
print "Learn time: %s s." % (time.time() - start_time)


# Predict #
f_predict = open("qual_mu.dta", 'r')
f_predict_out = open("submission2.dta", 'w')
start_time = time.time()
target_input_vector = []
target_output_vector = []
for line in f_predict:
    uid, mid, date = line.strip().split()
    target_input_vector.append([int(uid), int(mid)])
target_output_vector = clf.predict(target_input_vector)
for predicted_rating in target_output_vector:
    f_predict_out.write(str(predicted_rating) + '\n')
print "Predict time: %s s." % (time.time() - start_time)
f_predict.close()
f_predict_out.close()

# For LIMIT = 1000000 data points:
# Read input time: 5.19124603271 s.
# Learn time: 4.09771299362 s.
# Predict time: 52.6327300072 s.