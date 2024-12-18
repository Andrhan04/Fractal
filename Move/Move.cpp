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

using namespace std;
int mx = 10;

Figure* input_pole(int id) {
    ifstream InpPole("..\\Sowing\\Fractal\\koch_curve_pore_" + to_string(id) + ".txt");
    Figure* root = nullptr;
    if (InpPole.is_open()) {
        vector<Figure*> arr;
        string x,y;
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
    }
    else {
        cout << "FATAL" << endl;
    }
    return root;
}



int main(){
    int id_pole = 0;
    int id_exp = 0;
    Figure* root = input_pole(id_pole);
    Figure* copy = root;
    //root->get_param();
    pt p = pt(600, 500);
    auto flag = copy->In_Figure(p);
    cout << flag << endl;
    return 0;
}


/*
koch_curve_pore_{id}

*/