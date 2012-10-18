from sklearn import svm
import time

# Learn #
f_learn = open("all_um.dta", 'r')

input_vector = []
output_vector = []

num_iter = 0
LIMIT = 100000

start_time = time.time()
for line in f_learn:
    uid, mid, date, rating = line.strip().split()
    input_vector.append([uid, mid])
    output_vector.append(rating)
    num_iter += 1
    if num_iter >= LIMIT:
        break
print "Read input time: %s s." % (time.time() - start_time)
f_learn.close()

start_time = time.time()
clf = svm.SVC()
clf.fit(input_vector, output_vector)
print "Learn time: %s s." % (time.time() - start_time)


# Predict #
f_predict = open("qual.dta", 'r')
f_predict_out = open("submission2.dta", 'w')
start_time = time.time()
for line in f_predict:
    uid_mid = line.strip().split()[:2]
    f_predict_out.write(str(clf.predict(uid_mid)[0]) + '\n')
print "Predict time: %s s." % (time.time() - start_time)
f_predict.close()
f_predict_out.close()

# For LIMIT = 100000 data points:
# Read input time: 0.196299791336 s.
# Learn time: 1528.42140293 s.
# Predict time: 8086.82230496 s.