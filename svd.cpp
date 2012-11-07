#include <iostream>
#include <fstream>
#include <stdlib.h>
using namespace std;

#define TRAINING_FILE "all_um.dta"
#define NUM_USERS 458293
#define NUM_MOVIES 17770
#define NUM_TRAINING 102416306
#define NUM_TESTING 2749898
#define NUM_COMPONENTS 40
#define L_RATE 0.01
#define ERR_MARGIN L_RATE * 0.1

double ** open_training_file() {
    int i = 0;
    int j = 0;
    string line;
    char * p, * line_copy;
    double ** pointers = new double*[3];
    double * training_users = new double[NUM_TRAINING];
    double * training_movies = new double[NUM_TRAINING];
    double * training_ratings = new double[NUM_TRAINING];
    pointers[0] = training_users;
    pointers[1] = training_movies;
    pointers[2] = training_ratings;
    //cout << pointers[0] << pointers[1] << pointers[2] << endl;
    ifstream training_file(TRAINING_FILE);
    if (training_file.is_open()) {
        while (training_file.good()) {
            getline(training_file, line);
            line_copy = new char[line.size() + 1];
            strcpy(line_copy, line.c_str());
            p = strtok(line_copy, " ");
            while (p != NULL) {
                if (j == 0) {
                    training_users[i] = atof(p);
                }
                else if (j == 1) {
                    training_movies[i] = atof(p);
                }
                else if (j == 3) {
                    training_ratings[i] = atof(p);
                }
                j++;
                p = strtok(NULL, " ");
            }
            j = 0;
            delete[] line_copy;
            //cout << line << endl;
            //cout << training_users[i] << ", " << training_movies[i] << ", " << training_ratings[i] << endl;
            i++;
            //if (i > 10000000) { break; }
        }
        training_file.close();
    }
    else cout << "Unable to open file " << TRAINING_FILE << endl;
    return pointers;
}

double ** initialize_feature_matrices() {
    int i, j;
    double ** pointers = new double*[2];
    double * user_features = new double[NUM_USERS * NUM_COMPONENTS];
    double * movie_features = new double[NUM_MOVIES * NUM_COMPONENTS];
    pointers[0] = user_features;
    pointers[1] = movie_features;
    // cout << pointers[0] << pointers[1] << endl;
    for (i = 0; i < NUM_USERS; i++) {
        for (j = 0; j < NUM_COMPONENTS; j++) {
            user_features[i * NUM_COMPONENTS + j] = 0.1;
            //cout << i << ", " << j << ": " << user_features[i * NUM_COMPONENTS + j] << endl;
        }
    }
    for (i = 0; i < NUM_MOVIES; i++) {
        for (j = 0; j < NUM_COMPONENTS; j++) {
            movie_features[i * NUM_COMPONENTS + j] = 0.1;
            //cout << i << ", " << j << ": " << movie_features[i * NUM_COMPONENTS + j] << endl;
        }
    }
    return pointers;
}

void train(double ** training_pointers, double ** feature_pointers) {
    int i, j, k, user, movie;
    double err, rating, predicted_rating, tmp_feature;
    double * training_users = training_pointers[0];
    double * training_movies = training_pointers[1];
    double * training_ratings = training_pointers[2];
    double * user_features = feature_pointers[0];
    double * movie_features = feature_pointers[1];
    //cout << training_users << training_movies << training_ratings << endl;
    //cout << user_features << movie_features << endl;

    for (i = 0; i < NUM_TRAINING; i++) {
        user = training_users[i];
        movie = training_movies[i];
        rating = training_ratings[i];
        // Train all features
        for (j = 0; j < NUM_COMPONENTS; j++) {
            //cout << user << endl;
            //cout << movie << endl;
            //cout << rating << endl;
            err = 1.0;
            while (err > ERR_MARGIN || err < -ERR_MARGIN) {
                // Calculate predicted rating
                cout << "Iterating feature " << j << endl;
                predicted_rating = 0.0;
                for (k = 0; k < NUM_COMPONENTS; k++) {
                    predicted_rating += user_features[(int)user * NUM_COMPONENTS + k] * movie_features[(int)movie * NUM_COMPONENTS + k];
                    //cout << user_features[(int)user * NUM_COMPONENTS + k] << ", " << movie_features[(int)movie * NUM_COMPONENTS + k] << endl;
                    //cout << predicted_rating << endl;
                }
                err = L_RATE * (rating - predicted_rating);
                cout << rating << endl;
                cout << predicted_rating << endl;
                cout << err << endl;
                tmp_feature = user_features[(int)user * NUM_COMPONENTS + j];
                user_features[(int)user * NUM_COMPONENTS + j] += err * movie_features[(int)movie * NUM_COMPONENTS + j];
                movie_features[(int)movie * NUM_COMPONENTS + j] += err * tmp_feature;
            }
            cout << (int)user * NUM_COMPONENTS + j << ", " << (int)movie * NUM_COMPONENTS + j << endl;
            cout << "Feature " << j << " for " << (int)user << ", " << (int)movie << " done: " << user_features[(int)user * NUM_COMPONENTS + j] << ", " << movie_features[(int)movie * NUM_COMPONENTS + j] << endl;
        }
    }

}

int main() {
    /* 
    /  training_pointers[0]: Pointer to training_users array.
    /  training_pointers[1]: Pointer to training_movies array.
    /  training_pointers[2]: Pointer to training_ratings array.
    /  feature_pointers[0]: Pointer to user_features matrix.
    /  feature_pointers[1]: Pointer to movie_features matrix.
    */
    double ** training_pointers = new double*[3];
    double ** feature_pointers = new double*[2];
    cout << "Opening training file..." << endl;
    training_pointers = open_training_file();
    cout << "Training data loaded." << endl;
    cout << "Initializing feature matrices..." << endl;
    feature_pointers = initialize_feature_matrices();
    cout << "Feature matrices initialized." << endl;
    train(training_pointers, feature_pointers);
    //cout << pointers[0] << pointers[1] << pointers[2] << endl;
    //cout << pointers[0][0] << ' ' << pointers[1][0] << ' ' << pointers[2][0] << endl;
    //delete[] training_users;
    //delete[] training_movies;
    //delete[] training_ratings;
    //delete[] pointers;
}