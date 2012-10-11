Ideas
=====
- Partition
    - Split users into "light" and "heavy" users, based on how many movies they've rated total.
    - Compute weighted average, giving more weight to the "heavy" users
- Remove users who only rate movies a 1 or 5 (extreme users)
- Calculate how much higher/lower a user typically rates their movies
    - for a given user i who rated movies j, sum up and average (r_{i,j} - r_j_avg)
- Split data into multiples files for speed.
    - one file for each movie? one file for each user?
