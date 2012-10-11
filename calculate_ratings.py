f = open(r'average_movie_ratings.out', 'r')

avg_movie_ratings = {}

for line in f:
    line = line.split(':')
    movie_id = line[0].strip()
    movie_rating = line[1].strip()
    avg_movie_ratings[movie_id] = movie_rating

f.close()

f_in = open(r'qual.dta', 'r')
f_out = open(r'submission.dta', 'w')

for line in f_in:
    line = line.split()
    user_id = line[0].strip()
    movie_id = line[1].strip()
    date = line[2].strip()
    if movie_id in avg_movie_ratings:
        predicted_rating = avg_movie_ratings[movie_id]
    else:
        predicted_rating = 2.5
    f_out.write(str(predicted_rating) + '\n')

f_in.close()
f_out.close()