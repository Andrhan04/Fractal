#pragma once
struct pt {
    const double EPS = 1E-9;
    pt(double x, double y) : x(x), y(y) {};
    double x, y;
    bool operator < (const pt& p) const {
        return x < p.x - EPS || abs(x - p.x) < EPS && y < p.y - EPS;
    }
    bool operator == (const pt& p) const {
        return abs(x - p.x) < EPS && abs(y - p.y) < EPS;
    }
    bool operator > (const pt& p) const {
        return (p < *this);
    }
    pt operator = (const pt& p) {
        return pt(p.x, p.y);
    }
};