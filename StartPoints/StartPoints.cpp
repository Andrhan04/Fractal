#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <string>
#include <unordered_map>
#include <fstream>
#include <math.h>
#include <random>

using namespace std;
#define all(v) (v).begin(),(v).end()

class Point {
private:
    double eps = 1e-4;
    mt19937 random_generator_;
    int returnRandom(int min, int max) {
        if (max < min) swap(max, min);
        std::uniform_int_distribution<int> range(min, max);
        return range(random_generator_);
    }

    void CreateCoord(int left, int rigth, int up, int down) {
        X = returnRandom(left, rigth);
        Y = returnRandom(down, up);
    }

public:
    double X, Y; // 0 - 1000 координата Х, координата Y,
    //double Speed; // 0.1 - 1 скорость,
    //int Direction; // 0 - 359 направление.

    bool Same(Point* other) {
        return ((abs(other->X - X) < eps) && (abs(other->Y - Y) < eps));
    }

    void Create(int left, int rigth, int up, int down) {
        CreateCoord(left, rigth, up, down);
    }

    Point(int left, int rigth, int up, int down) {
        random_device device;
        random_generator_.seed(device());
        Create(left, rigth, up, down);
    }
};

int main() {
    int id = 0;
    int left = 0, up = 550, right = 100, down = 450;
    ofstream Start("..\\Sowing\\Points\\Points_" + to_string(id) + ".txt");
    if (!Start.is_open()) return 0;
    int n = 1000, r = 0;
    vector<Point*> v;
    Start << n << endl;
    Start << left << ' ' << up << ' ' << right << ' ' << down << endl;
    for (int i = 0; i < n; i++) {
        Point* p = new Point(left,right,up,down);
        bool unic = true;
        bool repeat = true;
        while (repeat) {
            for (auto i : v) {
                if (p->Same(i)) {
                    unic = false;
                    break;
                }
            }
            if (!unic) {
                p->Create(left, right, up, down);
                unic = true;
                r++;
            }
            else {
                repeat = false;
            }
        }
        v.push_back(p);

        Start << setprecision(3) << fixed << setw(10) << p->X << setw(10) << p->Y << setw(8) << endl;
        cout << setprecision(3) << fixed << setw(10) << p->X << setw(10) << p->Y << setw(8) << endl;

    }
    cout << r << endl;
    return 0;
}
