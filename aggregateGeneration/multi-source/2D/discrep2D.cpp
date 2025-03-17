#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <fstream>
#include <algorithm>

using namespace std;

// ENSURE M2 IS ALWAYS LARGER THAN M1
const int M_1 = 10;
const int M_2 = 20;
const int n = 30;


struct Coord
{
    signed int x;
    signed int y;
};

struct Edge
{
    Coord e1;
    Coord e2;
};

struct Forest
{
    vector<Coord> vertices;
    vector<Edge> edges;
};

struct Discrep
{
    Forest f1;
    Forest f2;
    vector<Coord> c; // coordinates that will only be in the big aggregate, not the small one 
    vector<Edge> edges;  // edges common in both f1 and f2
    vector<Coord> disc;  // sites in both aggregates reached by different particles
};


bool isEqual(Coord c1, Coord c2){
    if (c1.x == c2.x &&
        c1.y == c2.y)
        return true;
    return false;
}

bool isIn(Edge edge, vector<Edge> edge_vect)
{
    for (auto num : edge_vect){
        if ((isEqual(edge.e1, num.e1) && isEqual(edge.e2, num.e2)) ||
            (isEqual(edge.e1, num.e2) && isEqual(edge.e2, num.e1)))
            return true;
    }
    return false;
}

bool isIn(Coord coordinate, vector<Coord> aggregate)
{
    for (auto num : aggregate)
    {
        if (coordinate.x == num.x &&
            coordinate.y == num.y)
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
    if (prob < 1.0 / 4)
    {
        coordinate.x += 1;
        // cout << "x += 1";
    }
    else if (prob < 1.0 / 2)
    {
        coordinate.x -= 1;
        // cout << "x -= 1";
    }
    else if (prob < 3.0 / 4)
    {
        coordinate.y += 1;
        // cout << "y += 1";
    }
    else
    {
        coordinate.y -= 1;
        // cout << "y -= 1";
    }
}

void levelsPlane(Coord L[(2 * M_2 + 1)])
{
    int index = 0;
    for (int i = 0; i < 2* M_2 + 1; i++)
    {
        L[index].x = 0;
        L[index].y = i - M_2;
        index++;
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

vector<Coord> levels_poisson(int n, int M)
{
    Coord levels[(2 * M + 1)];
    levelsPlane(levels);
    vector<std::pair<Coord, double>> coordinates_with_times;

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

Discrep discrep(int nb_particle, int M1, int M2)
{   
    Discrep D;
    Forest forest1; //small forest
    Forest forest2; //big forest
    vector<Edge> common_edges;
    vector<Coord> agg1; // small aggregate
    vector<Coord> agg2; //big aggregate   both will store coordinates of settled particles
    vector<Coord> discrepancy; //stores the coordinates of the particles that are in the big aggregate but not the small one
    int source_count = 0; // number of sources we have gone through
    vector<Coord> level_list = levels_poisson(nb_particle, M2); // list of all sources to go through
    // store the levels of the small aggregate, ie the ones inside level_list with coordinates between -M1 and M1
    vector<Coord> levels_small;
    copy_if(level_list.begin(), level_list.end(), back_inserter(levels_small),
                                         [M1](const Coord &c)
                                         { return c.y <= M1 && -M1 <= c.y  ; });
    // get the size of the list
    int size = level_list.size();
    int progress = 1; // to keep track of the progress of the process
    while (source_count < size)
    {
        Coord source = level_list[source_count]; // source from which we need to send particles
        Coord newCoord = source;                 // at first, the 'new' coordinate is the source
        Coord previous = source;                 // the previous coordinate is the source
        if (isIn(newCoord, levels_small)) //particle works for both aggregates
        {
            bool worksForBoth = isIn(newCoord, level_list); // only for debugging purposes
            while (isIn(newCoord, agg1))
            { // if the coordinate is in the small aggregate, it continues its path (and we know we are in the big one also)
                double proba = ((double)rand() / (RAND_MAX));
                previous = newCoord; // we keep track of the previous coordinate
                movement(newCoord, proba); // we update the new coordinate according to the direction of the random walk
            }
            agg1.push_back(newCoord); // we add the new coordinate to the list of settled particles
            forest1.edges.push_back({previous, newCoord});
                // so now we have exited the small aggregate, but not necessarily the big one
            Coord start = newCoord; // we keep track of the starting point of the particle
            while (isIn(newCoord, agg2))
            { // if the coordinate is in the big aggregate, it continues its path
                double proba = ((double)rand() / (RAND_MAX));
                previous = newCoord;   // we keep track of the previous coordinate
                movement(newCoord, proba);
            }
            if (!isEqual(start, newCoord)) // if the particle has moved, it means that there is a dicrepancy
            {
                discrepancy.push_back(newCoord); // we add the new coordinate to the list of discrepancies
            }
            agg2.push_back(newCoord); // we add the new coordinate to the list of settled particles
            forest2.edges.push_back({previous, newCoord});
            //edges.push_back({previous, newCoord}); // we add the edge to the list of edges common to both 
            //removed this line because we can have same edges but not reached with the same particles
            source_count++;
        }
        else // the particle only works for the big one, it is a discrepancy
        {
            while (isIn(newCoord, agg2))
            { // if the coordinate is in the big aggregate, it continues its path
                double proba = ((double)rand() / (RAND_MAX));
                previous = newCoord;
                movement(newCoord, proba);
            }
            agg2.push_back(newCoord); // we add the new coordinate to the list of settled particles
            forest2.edges.push_back({previous, newCoord});
            discrepancy.push_back(newCoord); // we add the new coordinate to the list of discrepancies
            source_count++;
        }
        progressBar(size, source_count, progress);
    }
    // we now need to take out of discrepancies the sites that are not in the small one 
    // discrepancies needs to be made up of vertices common to both, but reached by different particles 
    vector<Coord> final_discrep;
    for (auto num : discrepancy)
    {
        if (isIn(num, agg1)) // if the site is also in the small aggregate, then it is a REAL discrep
        {
            final_discrep.push_back(num);
        }
    }
    // we loop through elements of agg2, and see if they are in agg1, and we add them to D.c if they are not
    for (auto num : agg2)
    {
        if (!isIn(num, agg1))
        {
            D.c.push_back(num);
        }
    }
    // we need to find the edges common to both forests
    // we loop through the edges of forest1, and see if they are in forest2, and we add them to D.edges if they are
    for (auto num : forest1.edges)
    {
        if (isIn(num, forest2.edges))
        {
            common_edges.push_back(num);
        }
    }
    D.f1 = forest1;
    D.f2 = forest2;
    D.edges = common_edges;
    D.disc = final_discrep;
    D.f1.vertices = agg1;
    D.f2.vertices = agg2;
    return D;
}

void vectorToFile1(Discrep D)
{
    // create and open file
    fstream myFile;
    myFile.open("C:/Users/keena/OneDrive/Bureau/Math/Python/Scripts IDLA/data/multi-source/An-dagger/2D/agg.txt", ios::out);
    // write to file
    myFile << "[";
    for (auto num : D.c)
    {
        myFile << "[" << num.x << ", " << num.y << "], ";
    }
    // remove the last comma and space
    myFile.seekp(-2, ios_base::end);
    myFile << "]";
    // close files
    myFile.close();
}

void vectorToFile2(Discrep D)
{
    // create and open file
    fstream myFile;
    myFile.open("C:/Users/keena/OneDrive/Bureau/Math/Python/Scripts IDLA/data/multi-source/An-dagger/2D/edges.txt", ios::out);
    // write to file
    myFile << "[";
    for (auto num : D.edges)
    {
        myFile << "[[" << num.e1.x << ", " << num.e1.y << "], [" << num.e2.x << ", " << num.e2.y << "]], ";
    }
    // remove the last comma and space
    myFile.seekp(-2, ios_base::end);
    myFile << "]";
    // close files
    myFile.close();
}

void vectorToFile3(Discrep D)
{
    // create and open file
    fstream myFile;
    myFile.open("C:/Users/keena/OneDrive/Bureau/Math/Python/Scripts IDLA/data/multi-source/An-dagger/2D/disc.txt", ios::out);
    // write to file
    myFile << "[";
    for (auto num : D.disc)
    {
        myFile << "[" << num.x << ", " << num.y << "], ";
    }
    // remove the last comma and space
    myFile.seekp(-2, ios_base::end);
    myFile << "]";
    // close files
    myFile.close();
}

void vectorToFile4(Discrep D)
{
    // create and open file
    fstream myFile;
    myFile.open("C:/Users/keena/OneDrive/Bureau/Math/Python/Scripts IDLA/data/multi-source/An-dagger/2D/smallforest.txt", ios::out);
    // write to file
    myFile << "[";
    for (auto num : D.f1.edges)
    {
        myFile << "[[" << num.e1.x << ", " << num.e1.y << "], [" << num.e2.x << ", " << num.e2.y << "]], ";
    }
    // remove the last comma and space
    myFile.seekp(-2, ios_base::end);
    myFile << "]";
    // close files
    myFile.close();
}

void vectorToFile5(Discrep D)
{
    // create and open file
    fstream myFile;
    myFile.open("C:/Users/keena/OneDrive/Bureau/Math/Python/Scripts IDLA/data/multi-source/An-dagger/2D/bigforest.txt", ios::out);
    // write to file
    myFile << "[";
    for (auto num : D.f2.edges)
    {
        myFile << "[[" << num.e1.x << ", " << num.e1.y << "], [" << num.e2.x << ", " << num.e2.y << "]], ";
    }
    // remove the last comma and space
    myFile.seekp(-2, ios_base::end);
    myFile << "]";
    // close files
    myFile.close();
}



void param_description(){
    // create and open file
    fstream myFile;
    myFile.open("C:/Users/keena/OneDrive/Bureau/Math/Python/Scripts IDLA/data/multi-source/An-dagger/2D/description.txt", ios::out);
    // write to file
    myFile << "Parameters : n= " << n << ", M1= " << M_1 << ", M2= " << M_2; 
    // close files
    myFile.close();
}

int main()
{
    Discrep D = discrep(n, M_1, M_2);
    vectorToFile1(D);
    vectorToFile2(D);
    vectorToFile3(D);
    vectorToFile4(D);
    vectorToFile5(D);
    param_description();
    return 0;
}