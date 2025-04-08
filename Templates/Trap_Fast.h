#pragma once
#include "struct_pt.h"

class Trap {
private:
    bool cath(pt p) {
        if ((p.x - X) * (p.y - X) + (p.y - Y) * (p.y - Y) < Range * Range) {
            Alive = false;
            return true;
        }
        else {
            return false;
        }
    }
public:
    double X, Y, Range;
    bool Alive;
    Trap(double x, double y) {
        X = x;
        Y = y;
        Range = 0.5;
        Alive = true;
    }
    Trap() {
        X = 0;
        Y = 0;
        Range = 0.5;
        Alive = true;
    }
    bool Cath(double x, double y) {
        pt p = pt(x, y);
        return cath(p);
    }
};