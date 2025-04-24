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
#include <omp.h>

using namespace std;
using json = nlohmann::json;


Figure* input_pole(int id) {
    ifstream InpPole("..\\Sowing\\Fractal_start\\koch_curve_pore_" + to_string(id) + ".txt");
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
        else {
            //cout << "FATAL ERROR \nlin fractal =" << arr.size() << endl;
        }
        //cout << "INPUT FRACTAL WAS DONE" << endl;
    }
    else {
        //cout << "FATAL ERROR \nNOT FIND Sowing\\Fractal\\koch_curve_pore_" << id << ".txt" << endl;
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
        //cout << left << ' ' << up << ' ' << right << ' ' << down << endl;
        string X, Y;
        while (in >> X >> Y) {
            myArr.push_back(Point(stod(X), stod(Y), f, up, down, left, right));
        }
        //cout << "INPUT POINT WAS DONE" << endl;

    }
    else {
        //cout << "FATAL ERROR \nNOT FIND Sowing\\Points\\Points_" << id << ".txt" << endl;
    }
    in.close();
}


void input_trap(int id, vector<Trap>& myArr, Figure* root) {
    if (root == nullptr) {
        //cout << "WRRING" << endl;
        return;
    }
    ifstream in("..\\Sowing\\Trap_fast\\Traps_" + to_string(id) + ".txt");
    string line, X, Y;
    vector<Figure*> fig;
    while (root->next != nullptr) {
        //(*root).get_param();
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
        //cout << "INPUT TRAP WAS DONE" << endl;
    }
    else {
        //cout << "FATAL ERROR \nNOT FIND Sowing\\Trap\\Traps_" << id << ".txt" << endl;
    }
    in.close();
}

void Program(int id_pole, int id_point, int id_trap, int id_exp, int t) {
    vector<int> mem;
    Figure* root = input_pole(id_pole);
    int Live_time = -1;
    if (root == nullptr) {
        //cout << "WRRING" << endl;
        return;
    }
    Figure* copy = root;
    vector<Point> myPoints;
    vector<Trap> myTraps;
    input_point(id_point, myPoints, copy);
    copy = root;
    input_trap(id_trap, myTraps, copy);
    int n_p = myPoints.size();
    json j;
    j["experiment_id"] = id_exp;
    j["pole_id"] = id_pole;
    j["point_id"] = id_point;
    j["trap_id"] = id_trap;
    j["iterationsCount"] = t;
    j["pointsCount"] = n_p;
    j["trapsCount"] = myTraps.size();
    j["trapsSeeds"] = "..\\Sowing\\Trap_fast\\Traps_" + to_string(id_trap) + ".txt";
    j["pointsSeed"] = "..\\Sowing\\Points\\Points_" + to_string(id_point) + ".txt";
    vector<int> buf(t / 100);
    string path = "..\\log_whith_traps\\pole_" + to_string(id_pole) + "\\Points_" + to_string(id_point) + "\\Traps_" + to_string(id_trap);
    ofstream Death(path + "\\Dead_" + to_string(id_exp) + ".txt");
    if (filesystem::create_directories(path + "\\Iter_" + to_string(id_exp))) {
        //cout << "Create" << endl;
    }
    for (int a = 0; a < t; a++) {
        if (a % (t / 100) == 0) {
            //cout << "Complete" << setw(3) << a / (t / 100) << " %" << endl;
        }
        if (a % 1000 == 0) {
            mem.push_back(n_p);
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
        if (Live_time < 0 && n_p < myPoints.size() / 2.71) {
            Live_time = a;
        }
    }
    ofstream Iter(path + "\\Iter_" + to_string(id_exp) + "\\Iter_" + to_string(t) + ".txt");
    for (int i = 0; i < n_p; i++) {
        Iter << setprecision(3) << fixed << myPoints[i].X << ' ' << myPoints[i].Y << ' ' << myPoints[i].Work << endl;
    }
    Iter.close();
    //cout << "WAS DONE" << endl;
    ofstream Alive(path + "\\Alive_" + to_string(id_exp) + ".txt");
    for (int i = 0; i < n_p; i++) {
        Alive << setprecision(3) << fixed << myPoints[i].X << ' ' << myPoints[i].Y << endl;
    }
    j["Live_time"] = Live_time;
    ofstream Statist(path + "\\Statist_" + to_string(id_exp) + ".txt");
    Statist << j << endl;
    for (int i = 0; i < mem.size(); i++) {
        Statist << i*1000 << ' ' << mem[i] << endl;
    }
    Statist << t << ' ' << n_p << endl;
    Statist.close();
    Alive.close();
    Death.close();
    //cout << id_exp << ' ' << "Was done" << endl;
}

void Create(int id_pole, int id_point, int id_trap) {
    string path = "..\\log_whith_traps";
    if (filesystem::create_directories(path)) {
        //cout << "Create" << endl;
    }
    path += "\\pole_" + to_string(id_pole);
    if (filesystem::create_directories(path)) {
        //cout << "Create" << endl;
    }
    path += "\\Points_" + to_string(id_point);
    if (filesystem::create_directories(path)) {
        //cout << "Create" << endl;
    }
    path += "\\Traps_" + to_string(id_point);
    if (filesystem::create_directories(path)) {
        //cout << "Create" << endl;
    }
}

int main() {
    int id_pole = 0;
    int id_point = 0;
    int id_trap = 0;
    int exp = 0;
    int t = 1e6;
    const int g_nNumberOfThreads = 30;
    omp_set_num_threads(g_nNumberOfThreads);
#pragma omp parallel for
    for (int i = 0; i <= 131; i++) {
        cout << i << ' ' << "Start " << endl;
        Create(id_pole, id_point, i);
        Program(id_pole, id_point, i, exp, t);
        cout << i << ' ' << "Was done" << endl;
    }
}