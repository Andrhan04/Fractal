#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <string>
#include <unordered_map>
#include <fstream>
#include <math.h>
#include <random>
#include <omp.h>

using namespace std;

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
    vector<double> fractal_x = { 100, 428.86751345948124, 550, 671.1324865405187, 1000, 1000, 728.8675134594813, 550, 371.13248654051864, 100},
                fractal_y = { 550, 550, 340.1923788646683, 550, 550, 450, 450, 140.1923788646683, 450, 450};
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

int main() {
    const int g_nNumberOfThreads = 20;
    omp_set_num_threads(g_nNumberOfThreads);
    for (int i = 700, id = 2; i < 2000; id++, i += 10) {
        programm(id, i);
    }
    return 0;
}