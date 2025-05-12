#include <iomanip>
#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <math.h>
#include <random>
#include <string>
#include "..\Templates\Fractal.h"
#include "..\Templates\Point.h"
#include "..\Templates\Trap.h"
#include "..\Templates\json.hpp"
#include <filesystem>
#include <omp.h>

using namespace std;
using json = nlohmann::json;

Figure* input_pole(int id) {
    ifstream InpPole("..\\Sowing\\Fractal_start\\koch_curve_pore_" + to_string(id) + ".txt");
    Figure* root = nullptr;
    if (InpPole.is_open()) {
        vector<Figure*> arr;
        int id = 0;
        string x,y;
        while (InpPole >> x >> y) {
            pt b = pt(stod(x), stod(y));
            InpPole >> x >> y;
            pt a = pt(stod(x), stod(y));
            InpPole >> x >> y;
            pt d = pt(stod(x), stod(y));
            InpPole >> x >> y;
            pt c = pt(stod(x), stod(y));
            Figure* f = new Figure(a, b, c, d, id++);
            arr.push_back(f);
        }
        if (arr.size() > 1) {
            arr[0]->next = arr[1];
            for (int i = 1; i < arr.size() - 1; i++) {
                arr[i]->next = arr[i + 1];
                arr[i]->prev = arr[i - 1];
            }
            arr[arr.size() - 1]->prev = arr[arr.size() - 2];
            root = arr[0];
        }
        std::cout << "INPUT FRACTAL WAS DONE" << endl;
    }
    else {
        std::cout << "FATAL ERROR \nNOT FIND Sowing\\Fractal\\koch_curve_pore_" << id << ".txt" << endl;
    }
    InpPole.close();
    return root;
}

void input_point(int id, vector<Point>& myArr, Figure* f) {
    string line, X, Y;
    double up; double down; double left; double right;
    ifstream in("..\\Sowing\\Points\\Points_" + to_string(id) + ".txt");
    if (in.is_open()) {
        getline(in, line);
        in >> left >> up >> right >> down;
        cout << left << ' ' << up << ' ' << right << ' ' << down << endl;
        string X, Y;
        while (in >> X >> Y) {
            myArr.push_back(Point(stod(X), stod(Y), f, up, down, left, right) );
        }
        std::cout << "INPUT POINT WAS DONE" << endl;

    }
    else {
        std::cout << "FATAL ERROR \nNOT FIND Sowing\\Points\\Points_" << id << ".txt" << endl;
    }
    in.close();
}

void Program(int id_pole, int id_point, int id_exp, int t){
    Figure* root = input_pole(id_pole);
    Figure* copy = root;
    vector<Point> myPoints;
    input_point(id_point, myPoints, copy);
    int n_p = myPoints.size();
    vector<int> buf(t / 100);
    string path = "..\\log\\pole_" + to_string(id_pole) + "\\Points_" + to_string(id_point);
    ofstream Alive(path + "\\Alive_" + to_string(id_exp) + ".txt");
    if (filesystem::create_directories(path + "\\Iter_" + to_string(id_exp))) {
        std::cout << "Create" << endl;
    }
    for (int a = 0; a < t; a++) {
        if (a % (t / 100) == 0) {
            std::cout << "Complete" << setw(3) << a / (t / 100) << " %" << endl;
        }
        if (a % 1000 == 0) {
            ofstream Iter(path + "\\Iter_" + to_string(id_exp) + "\\Iter_" + to_string(a) + ".txt");
            for (int i = 0; i < n_p; i++) {
                Iter << setprecision(3) << fixed << myPoints[i].X << ' ' << myPoints[i].Y << ' ' << myPoints[i].fig->id <<  endl;
            }
            Iter.close();
        }
        for (int i = 0; i < n_p; i++) {
            myPoints[i].Step();
        }
    }
    ofstream Iter(path + "\\Iter_" + to_string(id_exp) + "\\Iter_" + to_string(t) + ".txt");
    for (int i = 0; i < n_p; i++) {
        Iter << setprecision(3) << fixed << myPoints[i].X << ' ' << myPoints[i].Y << ' ' << myPoints[i].fig->id << endl;
    }
    Iter.close();

    std::cout << "WAS DONE" << endl;
    for (int i = 0; i < n_p; i++) {
        Alive << setprecision(3) << fixed << myPoints[i].X << ' ' << myPoints[i].Y << ' ' << myPoints[i].fig->id << endl;
    }
    Alive.close();
}

void Create(int id_pole, int id_point) {
    string path = "..\\log\\";
    if (filesystem::create_directories(path)) {
        std::cout << "Create" << endl;
    }
    path += "pole_" + to_string(id_pole);
    if (filesystem::create_directories(path)) {
        std::cout << "Create" << endl;
    }
    path += "\\Points_" + to_string(id_point);
    if (filesystem::create_directories(path)) {
        std::cout << "Create" << endl;
    }
}

int main() {
    int id_pole = 5;
    int id_point = 0;
    int exp = 0;
    int t = 1e6;
    Create(id_pole,id_point);
    Program(id_pole, id_point, exp, t);

    /*const int g_nNumberOfThreads = 5;
    omp_set_num_threads(g_nNumberOfThreads);
    for (int exp = 1; exp <= 20; exp++) {
        cout << "TEST " << setw(3) << exp << " WAS DONE" << endl;
    }*/
}