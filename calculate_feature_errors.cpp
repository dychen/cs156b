#include <iostream>
#include <fstream>
#include <stdlib.h>
using namespace std;

#define TRAINING_FILE "all_um.dta"
#define USER_FEATURE_FILE "user_features.dta"
#define MOVIE_FEATURE_FILE "movie_features.dta"
#define OUTPUT_FILE "feature_errors.dta"
#define NUM_USERS 458293
#define NUM_MOVIES 17770
#define NUM_TRAINING 102416306
#define NUM_TESTING 2749898
#define NUM_COMPONENTS 40

double ** load_feature_matrices() {
    int i = 0;
    int j = 0;
    string line;
    char * p, * line_copy;
    double ** pointers = new double*[2];
    double * user_features = new double[NUM_USERS * NUM_COMPONENTS];
    double * movie_features = new double[NUM_MOVIES * NUM_COMPONENTS];
    pointers[0] = user_features;
    pointers[1] = movie_features;
    // cout << pointers[0] << pointers[1] << endl;
    ifstream user_feature_file(USER_FEATURE_FILE);
    if (user_feature_file.is_open()) {
        while (user_feature_file.good()) {
            getline(user_feature_file, line);
            line_copy = new char[line.size() + 1];
            strcpy(line_copy, line.c_str());
            p = strtok(line_copy, " ");
            while (p != NULL) {
                if (j < NUM_COMPONENTS) {
                    user_features[i * NUM_COMPONENTS + j] = atof(p);
                }
                j++;
                p = strtok(NULL, " ");
            }
            j = 0;
            delete[] line_copy;
            i++;
        }
        user_feature_file.close();
    }
    else cout << "Unable to open file " << USER_FEATURE_FILE << endl;
    i = 0;
    j = 0;
    ifstream movie_feature_file(MOVIE_FEATURE_FILE);
    if (movie_feature_file.is_open()) {
        while (movie_feature_file.good()) {
            getline(movie_feature_file, line);
            line_copy = new char[line.size() + 1];
            strcpy(line_copy, line.c_str());
            p = strtok(line_copy, " ");
            while (p != NULL) {
                if (j < NUM_COMPONENTS) {
                    movie_features[i * NUM_COMPONENTS + j] = atof(p);
                }
                j++;
                p = strtok(NULL, " ");
            }
            j = 0;
            delete[] line_copy;
            i++;
        }
        movie_feature_file.close();
    }
    else cout << "Unable to open file " << MOVIE_FEATURE_FILE << endl;
    return pointers;
}

void calculate_errors(double ** feature_pointers) {
    int i = 0;
    int j = 0;
    int k, user, movie;
    double total_error = 0.0;
    double error, predicted_rating;
    string line;
    char * p, * line_copy;
    double * user_features = feature_pointers[0];
    double * movie_features = feature_pointers[1];

    ifstream training_file(TRAINING_FILE);
    ofstream output_file(OUTPUT_FILE);
    if (training_file.is_open() && output_file.is_open()) {
        while (training_file.good()) {
            getline(training_file, line);
            line_copy = new char[line.size() + 1];
            strcpy(line_copy, line.c_str());
            p = strtok(line_copy, " ");
            while (p != NULL) {
                if (j == 0) {
                    user = atoi(p);
                }
                else if (j == 1) {
                    movie = atoi(p);
                }
                else if (j == 3) {
                    predicted_rating = 0.0;
                    for (k = 0; k < NUM_COMPONENTS; k++) {
                        predicted_rating += user_features[user * NUM_COMPONENTS + k] * movie_features[movie * NUM_COMPONENTS + k];
                    }
                    error = (atof(p) - predicted_rating);
                    if (error < 0) {
                        error = -error;
                    }
                    output_file << error << '\n' << endl;
                    total_error += error;
                }
                j++;
                p = strtok(NULL, " ");
            }
            j = 0;
            delete[] line_copy;
            if (i % 1000000 == 0) {
                cout << i << " rating errors calculated." << endl;
            }
            i++;
        }
        cout << "Total error: " << total_error << endl;
        training_file.close();
        output_file.close();
    }
    else cout << "Unable to open fils." << endl;
}

int main() {
    double ** feature_pointers = new double*[2];
    cout << "Loading feature matrices..." << endl;
    feature_pointers = load_feature_matrices();
    cout << "Feature matrices loaded." << endl;
    cout << "Writing errors between predicted and actual values..." << endl;
    calculate_errors(feature_pointers);
    cout << "Done." << endl;
    delete[] feature_pointers;
}