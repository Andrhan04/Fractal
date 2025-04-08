#include <iomanip>
#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <math.h>
#include <random>
#include <string>
#include "..\Templates\Fractal_Fast.h"
#include "..\Templates\Point_Fast.h"
#include "..\Templates\Trap_Fast.h"
#include "..\Templates\json.hpp"
#include <filesystem>

using namespace std;
using json = nlohmann::json;


Figure* input_pole(int id) {
    ifstream InpPole("..\\Sowing\\Fractal\\koch_curve_pore_" + to_string(id) + ".txt");
    Figure* root = nullptr;
    if (InpPole.is_open()) {
        vector<Figure*> arr;
        string x, y;
        while (InpPole >> x >> y) {
            pt b = pt(stod(x), stod(y));
            InpPole >> x >> y;
            pt a = pt(stod(x), stod(y));
            InpPole >> x >> y;
            pt d = pt(stod(x), stod(y));
            InpPole >> x >> y;
            pt c = pt(stod(x), stod(y));
            Figure* f = new Figure(a, b, c, d);
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
        cout << "INPUT FRACTAL WAS DONE" << endl;
    }
    else {
        cout << "FATAL ERROR \nNOT FIND Sowing\\Fractal\\koch_curve_pore_" << id << ".txt" << endl;
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
            myArr.push_back(Point(stod(X), stod(Y), f, up, down, left, right));
        }
        cout << "INPUT POINT WAS DONE" << endl;

    }
    else {
        cout << "FATAL ERROR \nNOT FIND Sowing\\Points\\Points_" << id << ".txt" << endl;
    }
    in.close();
}


void input_trap(int id, vector<Trap>& myArr, Figure* root) {
    ifstream in("..\\Sowing\\Trap_fast\\Traps_" + to_string(id) + ".txt");
    string line, X, Y;
    vector<Figure*> fig;
    while (root->next != nullptr) {
        fig.push_back(root);
        root = root->next;
    }
    fig.push_back(root);
    fig.push_back(root);
    while (root->prev != nullptr) {
        fig.push_back(root);
        root = root->prev;
    }
    fig.push_back(root);
    if (in.is_open()) {
        getline(in, line);
        string WALL;
        while (in >> X >> Y >> WALL) {
            int i = stoi(WALL);
            fig[i]->add_trap(myArr.size(), (i > fig.size() - 1 / 2 ? 2 : (i == fig.size() - 1 ? 3 : 1)));
            myArr.push_back(Trap(stod(X), stod(Y)));
        }
        cout << "INPUT TRAP WAS DONE" << endl;
    }
    else {
        cout << "FATAL ERROR \nNOT FIND Sowing\\Trap\\Traps_" << id << ".txt" << endl;
    }
    in.close();
}

void Program(int id_pole, int id_point, int id_trap, int id_exp, int t) {
    Figure* root = input_pole(id_pole);
    Figure* copy = root;
    vector<Point> myPoints;
    vector<Trap> myTraps;
    input_point(id_point, myPoints, copy);
    input_trap(id_trap, myTraps, copy);
    int n_p = myPoints.size();
    vector<int> buf(t / 100);
    string path = "..\\log\\pole_" + to_string(id_pole) + "\\Points_" + to_string(id_point);
    ofstream Alive(path + "\\Alive_" + to_string(id_exp) + ".txt");
    ofstream Death(path + "\\Dead_" + to_string(id_exp) + ".txt");
    if (filesystem::create_directories(path + "\\Iter_" + to_string(id_exp))) {
        cout << "Create" << endl;
    }
    for (int a = 0; a < t; a++) {
        if (a % (t / 100) == 0) {
            cout << "Complete" << setw(3) << a / (t / 100) << " %" << endl;
        }
        if (a % 1000 == 0) {
            ofstream Iter(path + "\\Iter_" + to_string(id_exp) + "\\Iter_" + to_string(a) + ".txt");
            for (int i = 0; i < n_p; i++) {
                Iter << setprecision(3) << fixed << myPoints[i].X << ' ' << myPoints[i].Y << ' ' << myPoints[i].Work << endl;
            }
            Iter.close();
        }
        for (int i = 0; i < n_p; i++) {
            myPoints[i].Step();
            if (myPoints[i].Work && myPoints[i].try_cath(myTraps)) {
                Death << a << ' ' << myPoints[i].X << ' ' << myPoints[i].Y << endl;
                swap(myPoints[i], myPoints[n_p - 1]);
                n_p--;
            }
        }
    }
    cout << "WAS DONE" << endl;
    for (int i = 0; i < n_p; i++) {
        Alive << setprecision(3) << fixed << myPoints[i].X << ' ' << myPoints[i].Y << endl;
    }
    Alive.close();
    Death.close();
}

void Create(int id_pole, int id_point) {
    string path = "..\\log";
    if (filesystem::create_directories(path)) {
        cout << "Create" << endl;
    }
    path += "\\pole_" + to_string(id_pole);
    if (filesystem::create_directories(path)) {
        cout << "Create" << endl;
    }
    path += "\\Points_" + to_string(id_point);
    if (filesystem::create_directories(path)) {
        cout << "Create" << endl;
    }
}

int main() {
    int id_pole = 2;
    int id_point = 0;
    int id_trap = 0;
    int exp = 0;
    int t = 1e6;
    Create(id_pole, id_point);
    Program(id_pole, id_point, id_trap, exp, t);
}