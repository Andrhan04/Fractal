#pragma once

struct Wall
{
    double left = 0.0;
    double right = 50000.0;
    double up = 1000.0;
    double down = 0.0;
    Wall() {}
};

class Trap {
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
    bool Cath(Point& pt) {
        return ((pt.X - X) * (pt.X - X) + (pt.Y - Y) * (pt.Y - Y) < Range * Range);
    }
};