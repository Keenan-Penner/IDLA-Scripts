#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <fstream>
#include <algorithm>

using namespace std;

const int M = 10;
const int n = 10;

struct Coord
{
    signed int x;
    signed int y;
    signed int z;
};

// useful functions

bool isIn(Coord coordinate, vector<Coord> aggregate)
{
    for (auto num : aggregate)
    {
        if (coordinate.x == num.x &&
            coordinate.y == num.y &&
            coordinate.z == num.z)
            return true;
    }
    return false;
}

void progressBar(int total, int current, int &progress)
{
    if (current >= (total / 10.0) * progress)
    {
        cout << "Process is " << progress * 10 << "% done " << endl;
        progress++;
    }
}

void movement(Coord &coordinate, double &prob)
{
    if (prob < 1.0 / 6)
    {
        coordinate.x += 1;
        // cout << "x += 1";
    }
    else if (prob < 1.0 / 3)
    {
        coordinate.x -= 1;
        // cout << "x -= 1";
    }
    else if (prob < 1.0 / 2)
    {
        coordinate.y += 1;
        // cout << "y += 1";
    }
    else if (prob < 2.0 / 3)
    {
        coordinate.y -= 1;
        // cout << "y -= 1";
    }
    else if (prob < 5.0 / 6)
    {
        coordinate.z += 1;
        // cout << "z += 1";
    }
    else
    {
        coordinate.z -= 1;
        // cout << "z -= 1";
    }
}

void levelsPlane(Coord L[(2 * M + 1) * (2 * M + 1)])
{
    int index = 0;
    for (int i = 0; i < 2 * M + 1; i++)
    {
        for (signed int j = 0; j < 2 * M + 1; j++)
        {
            L[index].x = 0;
            L[index].y = i - M;
            L[index].z = j - M;
            index++;
        }
    }
}

// Functions handling randomness

// Random number generation function
double random_double()
{
    return static_cast<double>(rand()) / RAND_MAX;
}

// Poisson point process function

std::vector<double> poissonPointProcess(int n, double lambda_)
{
    std::vector<double> event_times;
    double current_time = 0;
    while (current_time < n)
    {
        // Generate the next inter-arrival time from an exponential distribution
        double inter_arrival_time = -log(random_double()) / lambda_;
        current_time += inter_arrival_time;

        // If the event time is within the interval [0, n], add it to the list
        if (current_time <= n)
        {
            event_times.push_back(current_time);
        }
    }
    return event_times;
}

std::vector<Coord> levels_poisson(int n, int M)
{
    Coord levels[(2 * M + 1) * (2 * M + 1)];
    levelsPlane(levels);
    std::vector<std::pair<Coord, double>> coordinates_with_times;

    // For each level, generate Poisson point process event times
    for (const auto &level : levels)
    {
        auto event_times = poissonPointProcess(n, 1.0); // Assuming lambda = 1.0
        for (const auto &time : event_times)
        {
            coordinates_with_times.push_back({level, time});
        }
    }

    // Sort coordinates based on the event times (second element of pair)
    std::sort(coordinates_with_times.begin(), coordinates_with_times.end(),
              [](const std::pair<Coord, double> &a, const std::pair<Coord, double> &b)
              {
                  return a.second < b.second;
              });

    // Extract the sorted coordinates
    std::vector<Coord> sorted_coordinates;
    for (const auto &coord_time : coordinates_with_times)
    {
        sorted_coordinates.push_back(coord_time.first);
    }

    return sorted_coordinates;
}

// We code the whole process using vectors (rather than arrays)
vector<Coord> An(int nb_particle, int levels)
{
    vector<Coord> agg;                              // will store coordinates of settled particles
    int source_count = 0;                           // number of sources we have gone through
    vector<Coord> level_list = levels_poisson(nb_particle, levels); //list of all sources to go through
    // get the size of the list
    int size = level_list.size();
    int progress = 1;        // to keep track of the progress of the process
    while (source_count < size)
    {
        Coord source = level_list[source_count]; // source from which we need to send particles
            Coord newCoord = source; // at first, the 'new' coordinate is the source
            while (isIn(newCoord, agg))
            { // if the coordinate is in the aggregate, it continues its path
                double proba = ((double)rand() / (RAND_MAX));
                movement(newCoord, proba);
            }
            agg.push_back(newCoord); // we add the new coordinate to the list of settled particles
        source_count++;
        progressBar(size, source_count, progress);
    }
    return agg;
}

void vectorToFile(vector<Coord> agg)
{
    // create and open file
    fstream myFile;
    myFile.open("C:/Users/keena/OneDrive/Bureau/Math/Python/Scripts IDLA/data/multi-source/An-dagger/3D/agg.txt", ios::out);
    // write to file
    myFile << "[";
    for (auto num : agg)
    {
        myFile << "[" << num.x << ", " << num.y << ", " << num.z << "], ";
    }
    // remove the last comma and space
    myFile.seekp(-2, ios_base::end);
    myFile << "]";
    // close files
    myFile.close();
}

int main()
{
    vector<Coord> agg = An(n, M);
    vectorToFile(agg);

    return 0;
}

/*
int main(){
    Coord coord;
    coord.x = 1;
    coord.y = 1;
    coord.z = 1;
    vector<Coord> v = {coord};
    double prob = 0;
    coord = movement(coord, prob);
    v.push_back(coord);
    vectorToFile(v);
    return 0;
}
*/