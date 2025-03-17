#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

const int M = 1;
const int n= 1;


struct Coord{
    signed int x;
    signed int y;
    signed int z;
};



bool isIn(Coord coordinate, vector<Coord> aggregate){
    for (auto num : aggregate){
        if (coordinate.x == num.x && 
            coordinate.y == num.y && 
            coordinate.z == num.z)
            return true;
    }
    return false;
}

void progressBar(int total, int current, int &progress){
    if (current >= (total/10.0)*progress){
        cout << "Process is " << progress*10 << "% done " << endl;
        progress++;
    }
}


void movement(Coord &coordinate, double &prob){
    if (prob < 1.0/6){
        coordinate.x += 1;
        //cout << "x += 1";
    }
    else if (prob < 1.0/3){
        coordinate.x -= 1;
        //cout << "x -= 1";
    } 
    else if (prob < 1.0/2){
        coordinate.y += 1;
        //cout << "y += 1";
    }
    else if (prob < 2.0/3){
        coordinate.y -= 1;
        //cout << "y -= 1";
    }
    else if (prob < 5.0/6){
        coordinate.z += 1;
        //cout << "z += 1";
    }
    else{
        coordinate.z -= 1;
        //cout << "z -= 1";
    }
}



void levelsPlane(Coord L[(2*M+1)*(2*M+1)]){
    int index = 0;
    for (int i = 0; i < 2*M + 1; i++){
        for (signed int j = 0; j < 2*M + 1; j++){
            L[index].x = 0;
            L[index].y = i - M;
            L[index].z = j - M;
            index++;
        }
    }
}

// function needs to be modified to work with vectors
/*
void idla(Coord source, Coord L[], int num){  //num is the number of particles we wish to send
    int count = 0;
    while (count < num){
        int proba = ((double) rand() / (RAND_MAX)); // uniformally picks a number between 0 and 1
        Coord newCoord = movement(source, proba);
        while (isIn(newCoord, L, count)){
            proba = ((double) rand() / (RAND_MAX));
            newCoord = movement(newCoord, proba);
        }
        L[count] = newCoord;    
        count++;
    }
}
*/

// instead, we code the whole process using vectors 
vector<Coord> An(int nb_particle, int levels){
    vector<Coord> agg; // will store coordinates of settled particles
    int size = (2*levels+1)*(2*levels+1); // total number of sources to go through
    int source_count = 0; // number of sources we have gone through
    Coord level_list[(2*M+1)*(2*M+1)];
    levelsPlane(level_list); // this creates a list with all the sources to go through
    int progress = 1; // to keep track of the progress of the process
    while (source_count < size){
        Coord source = level_list[source_count]; // source from which we need to send particles
        int num_sent_source = 0; // number of particles sent from this source
        while (num_sent_source < nb_particle){
            Coord newCoord = source; // at first, the 'new' coordinate is the source
            while (isIn(newCoord, agg)){ // if the coordinate is in the aggregate, it continues its path
                double proba = ((double) rand() / (RAND_MAX));
                movement(newCoord, proba);
            }
            agg.push_back(newCoord); // we add the new coordinate to the list of settled particles
            num_sent_source++;
        }
        source_count++;
        progressBar(size, source_count, progress);
    }
    return agg;
}

void vectorToFile(vector<Coord> agg){
    // create and open file
    fstream myFile;
    myFile.open("C:/Users/keena/OneDrive/Bureau/Math/Python/Scripts IDLA/data/multi-source/An-standard/3D/agg.txt", ios::out);
    // write to file
    myFile << "[";
    for (auto num : agg){
        myFile << "[" << num.x << ", " << num.y << ", " << num.z << "], ";
    }
    //remove the last comma and space
    myFile.seekp(-2, ios_base::end);
    myFile << "]";
    // close files
    myFile.close();
}



int main(){
    vector<Coord> agg = An(n, M);
    vectorToFile(agg);
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