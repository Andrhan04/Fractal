#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <omp.h>
#include <string>
#include <unordered_map>
#include <fstream>
#include <math.h>
#include <random>

using namespace std;

vector<double> fractal_x, fractal_y;

struct pt
{
    double x, y;
    pt() :x(0), y(0) {};
    pt(double x, double y) : x(x), y(y) {};
};

struct Line{
    pt start, end;
    Line(double x1, double y1, double x2, double y2) {
        start = pt(x1, y1);
        end = pt(x2, y2);
    }
    pt get_Trap(int dist) {
        pt res = pt((end.x - start.x) / get_dist() * dist + start.x, (end.y - start.y) / get_dist() * dist + start.y);
        return res;
    }
    int get_dist() {
        return sqrt((start.x - end.x) * (start.x - end.x) + (start.y - end.y) * (start.y - end.y));
    }
};

class Trap {
public:
    Trap() {
        std::random_device device;
        random_generator_.seed(device());
        for (int i = 0; i < fractal_x.size() - 1; i++) {
            arr.push_back(Line(fractal_x[i], fractal_y[i], fractal_x[i + 1], fractal_y[i + 1]));
        }
        Create();
    }
    int wall, dist;
    bool Same(Trap& t) {
        return (t.wall == wall && t.dist == dist);
    }
    bool Same(Trap* t) {
        return (t->wall == wall && t->dist == dist);
    }
    void Create() {
        wall = returnRandom(0, arr.size() - 1);
        dist = returnRandom(0, arr[wall].get_dist());
    }
    string Info_slow() {
        pt p = arr[wall].get_Trap(dist);
        string ans = to_string(p.x) + " " + to_string(p.y);
        return ans;
    }
    string Info_Fast() {
        pt p = arr[wall].get_Trap(dist);
        string ans = to_string(p.x) + " " + to_string(p.y) + " " + to_string(wall);
        return ans;
    }
    string Info_Fastest() {
        string ans = to_string(dist) + " " + to_string(wall);
        return ans;
    }
private:
    double eps = 2 * range;
    double range = 0.5;
    vector<Line> arr;
    std::mt19937 random_generator_;
    int returnRandom(int min, int max) {
        if (max < min) std::swap(max, min);
        std::uniform_int_distribution<int> range(min, max);
        return range(random_generator_);
    }
};

void programm(int id, int n){    
    int r = 0;
    ofstream Start_slow("..\\Sowing\\Trap_slow\\Traps_" + to_string(id) + ".txt");
    ofstream Start_fast("..\\Sowing\\Trap_fast\\Traps_" + to_string(id) + ".txt");
    if (!Start_slow.is_open()) return;
    if (!Start_fast.is_open()) return;
    vector<Trap> arr;
    Start_slow << n << endl;
    Start_fast << n << endl;
    for (int i = 0; i < n; i++) {
        Trap tr = Trap();
        bool unic = true;
        bool repeat = true;
        while (repeat) {
            for (int i = 0; i < arr.size(); i++) {
                if (tr.Same(arr[i])) {
                    unic = false;
                    break;
                }
            }
            if (!unic) {
                tr.Create();
                unic = true;
                r++;
            }
            else {
                repeat = false;
            }
        }
        arr.push_back(tr);
    }
    sort(arr.begin(), arr.end(), [&](Trap t1, Trap t2) {return (t1.wall > t2.wall || (t1.wall == t2.wall && t1.dist > t2.dist)); });
    for (auto tr : arr) {
        //cout << setprecision(3) << fixed << setw(10) << tr.wall << setw(10) << tr.dist << endl;
        Start_slow << tr.Info_slow() << endl;
        Start_fast << tr.Info_Fast() << endl;
    }
    Start_slow.close();
    Start_fast.close();
    cout << id << " was done" << endl;
}

void Get_pole(int id) {
    ifstream Input("..\\Sowing\\Fractal_convecs\\koch_curve_pore_" + to_string(id) + ".txt");
    vector<pair<double, double>> mem;
    if (Input.is_open()) {
        double x, y;
        while (Input >> x >> y) {
            mem.push_back({ x,y });
        }
        Input.close();
        fractal_x.push_back(mem[0].first);
        fractal_y.push_back(mem[0].second);
        for (int i = 1; i < mem.size(); i++) {
            if (mem[i - 1] != mem[i]) {
                fractal_x.push_back(mem[i].first);
                fractal_y.push_back(mem[i].second);
            }
        }
    }
    else {
        cout << "WARRING NOT OPEN\n ..\\Sowing\\Fractal_convecs\\koch_curve_pore_" + to_string(id) + ".txt" << endl;
        throw "File not open";
    }
}


int main() {
    const int g_nNumberOfThreads = 20;
    int pole_id = 4;
    Get_pole(pole_id);
    int ans = 0;
    for (int i = 1; i < fractal_x.size(); i++) {
        Line l = Line(fractal_x[i - 1], fractal_y[i - 1], fractal_x[i], fractal_y[i]);
        ans += l.get_dist();
    }
    cout << ans << endl;
/*
    omp_set_num_threads(g_nNumberOfThreads);
    for (int i = 700; i <= 2800; i += 10) {
        programm((i - 700)/10 + 401, i);
    }
*/
    return 0;
}