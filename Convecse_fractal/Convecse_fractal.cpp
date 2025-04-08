#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>
#include <filesystem>
#include "..\\Templates\\Fractal_convecse.h"
#include "..\\Templates\\json.hpp"

using namespace std;
using json = nlohmann::json;

double mysqr(double x1, double y1, double x2, double y2, double x3, double y3) {
    return ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2;
}

Figure* input_pole(int id, vector<pair<double,double>>& v) {
    ifstream InpPole("..\\Sowing\\Fractal_start\\koch_curve_pore_" + to_string(id) + ".txt");
    Figure* root = nullptr;
    if (InpPole.is_open()) {
        vector<Figure*> arr;
        string x,y;
        while (InpPole >> x >> y) {
            v.push_back({ stod(x), stod(y) });
            pt b = pt(stod(x), stod(y));
            
            InpPole >> x >> y;
            v.push_back({stod(x), stod(y)});
            pt a = pt(stod(x), stod(y));
            
            InpPole >> x >> y;
            v.push_back({ stod(x), stod(y) });
            pt d = pt(stod(x), stod(y));
            
            InpPole >> x >> y;
            v.push_back({ stod(x), stod(y) });
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

void Program(int id) {
    vector<pair<double, double>> v;
    Figure* root = input_pole(id,v);
    ofstream OutPole("..\\Sowing\\Fractal_convecs\\koch_curve_pore_" + to_string(id) + ".txt");
    root->get_param();
    while (root->next != nullptr) {
        OutPole << root->get_up_point() << endl;
        root = root->next;
    }
    OutPole << root->get_up_point() << endl;
    while (root->prev != nullptr) {
        OutPole << root->get_down_point() << endl;
        root = root->prev;
    }
    OutPole << root->get_down_point() << endl;
    OutPole.close();
    
    set<double> s; 
    json j;
    //----------------------------------Разделение по х----------------------------------------------------------------------------
    OutPole.open("..\\Sowing\\Fractal_convecs\\deleting_x\\koch_curve_pore_" + to_string(id) + ".txt");
    Figure* copy = root;
    for (auto i : v) {
        s.insert(i.first);
    }
    double prev = *s.begin();
    int dist_x = 60;
    for (auto i : s) {
        if (abs(i - prev) > 1) {
            if (abs(i - prev) > dist_x) {
                vector<string> v = copy->get_param();
                j["interval"] = { prev, i };
                j["up"] = v[2];
                j["down"] = v[3];
                OutPole << j << endl;
                copy = copy->next;
            }
            else {
                j["interval"] = { i, prev };
                j["up"] = ((copy->prev)->get_param())[2];
                j["down"] = (copy->get_param())[3];
                OutPole << j << endl;
            }
            prev = i;
        }
    }
    OutPole.close();
//------------------------------------------Площадь по x-----------------------------------------------------------------
    OutPole.open("..\\Sowing\\Fractal_convecs\\square_x\\koch_curve_pore_" + to_string(id) + ".txt");
    copy = root;
    pair<double, double> prev_p_1 = { (*min_element(v.begin(), v.end())).first, copy->get_y_points((*min_element(v.begin(), v.end())).first).second };
    pair<double, double> prev_p_2 = { (*min_element(v.begin(), v.end())).first, copy->get_y_points((*min_element(v.begin(), v.end())).first).first };
    pair<double, double> curr_p;
    vector<double> pr_summ_square(abs((*max_element(v.begin(), v.end())).first) + 1);
    pr_summ_square[0] = 0;
    auto help = (++s.begin());
    bool need_next_down = false;
    for (int i = (*min_element(v.begin(), v.end())).first + 1; i < pr_summ_square.size(); i++) {
        if (need_next_down) {
            curr_p = copy->get_y_points(prev_p_1.first + 1);
            if (copy->next != nullptr) {
                curr_p.second = copy->next->get_y_points(prev_p_1.first + 1).second;
            }
        }
        else {
            curr_p = copy->get_y_points(prev_p_1.first + 1);
        }
        //-----------------------------------------------переход в другую часть
        if (prev_p_1.first + 1 > *help) { 
            auto mem = help;
            help++;
            if (abs(*help - *mem) > dist_x) {
                need_next_down = false;
                if (copy->next != nullptr) {
                    copy = copy->next;
                    curr_p = copy->get_y_points(prev_p_1.first + 1);

                }
                else {
                    pr_summ_square[i] = pr_summ_square[i - 1];
                    continue;
                }
            }
            else {
                need_next_down = true;
                if (copy->next != nullptr) {
                    curr_p.second = copy->next->get_y_points(prev_p_1.first + 1).second;
                }
            }
        }
        //-----------------------------------------------------------------------------------------подсчёт
        pr_summ_square[i] = pr_summ_square[i - 1] 
            + mysqr(prev_p_1.first, prev_p_1.second, prev_p_2.first, prev_p_2.second, prev_p_1.first + 1, curr_p.first) 
            + mysqr(prev_p_1.first, prev_p_1.second, prev_p_1.first + 1, curr_p.first, prev_p_1.first + 1, curr_p.second);
        prev_p_1 = { prev_p_1.first + 1, curr_p.second };
        prev_p_2 = { prev_p_2.first + 1, curr_p.first };
    }
    for (auto i : pr_summ_square) {
        OutPole << abs(i) << endl;
    }
    OutPole.close();
//---------------------------------------------Разделение по у-------------------------------------------------------------------
    OutPole.open("..\\Sowing\\Fractal_convecs\\deleting_y\\koch_curve_pore_" + to_string(id) + ".txt");
    s = {};
    for (auto i : v) {
        s.insert(i.second);
    }
    prev = *s.begin();
    for (auto i : s) {
        if (abs(i - prev) > 1) {
            j["interval"] = { prev, i };
            OutPole << j << endl;
            prev = i;
        }
    }
    OutPole.close();

//-------------------------------------------------------------------------------------------------------------------------------------------
}

int main(){
    int id = 0;
    Program(id);
    return 0;
}