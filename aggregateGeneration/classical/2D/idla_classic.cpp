#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <fstream>
#include <algorithm>

using namespace std;

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

struct Tree
{
    vector<Coord> v;
    vector<Edge> e;
};

bool isEqual(Coord c1, Coord c2)
{
    if (c1.x == c2.x &&
        c1.y == c2.y)
        return true;
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

void progressBar(int total, int current, int &progress)
{
    if (current >= (total / 10.0) * progress)
    {
        cout << "Process is " << progress * 10 << "% done " << endl;
        progress++;
    }
}

Tree idla_2D(int n){
    vector<Coord> agg = { {0, 0} };
    vector<Edge> edges;
    int count = 1;
    int progress = 1; // to keep track of the progress of the process
    while(count < n){
        Coord newCoord = {0, 0};
        Coord previous = {0, 0};
        double proba = ((double)rand() / (RAND_MAX));
        movement(newCoord, proba);
        while(isIn(newCoord, agg)){
            proba = ((double)rand() / (RAND_MAX));
            previous = newCoord;
            movement(newCoord, proba);
        }
        agg.push_back(newCoord);
        edges.push_back({previous, newCoord});
        count++;
        progressBar(n, count, progress);
    }
    Tree T;
    T.v = agg;
    T.e = edges;
    return T;
}

void vectorToFile1(Tree T)
{
    // create and open file
    fstream myFile;
    myFile.open("data/classical_IDLA/sim3/agg.txt", ios::out);
    // write to file
    myFile << "[";
    for (auto num : T.v)
    {
        myFile << "[" << num.x << ", " << num.y << "], ";
    }
    // remove the last comma and space
    myFile.seekp(-2, ios_base::end);
    myFile << "]";
    // close files
    myFile.close();
}

void vectorToFile2(Tree T)
{
    // create and open file
    fstream myFile;
    myFile.open("data/classical_IDLA/sim3/edges.txt", ios::out);
    // write to file
    myFile << "[";
    for (auto num : T.e)
    {
        myFile << "[[" << num.e1.x << ", " << num.e1.y << "], [" << num.e2.x << ", " << num.e2.y << "]], ";
    }
    // remove the last comma and space
    myFile.seekp(-2, ios_base::end);
    myFile << "]";
    // close files
    myFile.close();
}

int main(){
    srand(time(0));
    Tree T = idla_2D(20000);
    vectorToFile1(T);
    vectorToFile2(T);
    return 0;
}