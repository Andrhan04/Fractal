#pragma once
#include <string>
using namespace std;

struct pt {
	const double EPS = 1E-9;
	pt(double x, double y) : x(x), y(y) {};
	pt() : x(0), y(0) {};
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
		x = p.x;
		y = p.y;
		return *(this);
	}
};

class Line {
private:
	double a, b, c;
	pt st;
	pt end;
	const double EPS = 1E-9;
	void norm() {
		double z = sqrt(a * a + b * b);
		if (abs(z) > EPS)
			a /= z, b /= z, c /= z;
	}
public:
	string get_point() {
		std::cout << st.x << ' ' << st.y << '\n' << end.x << ' ' << end.y << '\n';
		return to_string(st.x) + ' ' + to_string(st.y) + '\n' + to_string(end.x) + ' ' + to_string(end.y);
	}
	string get_param() {
		std::cout << "(" << a << ")x + (" << b << ")y + (" << c << ") = 0" << std::endl;
		return to_string(a) + ' ' + to_string(b) + ' ' + to_string(c);
	}
	double dist(pt p) const {
		return a * p.x + b * p.y + c;
	}
	double get_y(double x) {
		return (a * x + c)/(-b);
	}
	Line() {
		st = pt(-1,0);
		end = pt(0,0);
		a = 1;
		b = 1;
		c = 0;
	}
	Line(pt p, pt q) {
		st = p;
		end = q;
		a = p.y - q.y;
		b = q.x - p.x;
		c = -a * p.x - b * p.y;
		norm();
	}
	Line operator = (const Line& l) {
		st = l.st;
		end = l.end;
		a = l.a;
		b = l.b;
		c = l.c;
		return (*this);
	}
};

class Figure{
private:
	Line left = Line();
	Line right = Line();
	Line up = Line();
	Line down = Line();
	double eps = 1e-9;
public:
	pair<double, double> get_y_points(double x) {
		return {up.get_y(x), down.get_y(x)};
	}
	vector<string> get_param() {
		vector<string> s;
		std::cout << "left  ";
		s.push_back(left.get_param());
		std::cout << "right ";
		s.push_back(right.get_param());
		std::cout << "up    ";
		s.push_back(up.get_param());
		std::cout << "down  ";
		s.push_back(down.get_param());
		return s;
	}
	string get_up_point() {
		return up.get_point();
	}
	string get_down_point() {
		return down.get_point();
	}
	Figure(pt a, pt b, pt c, pt d) {
		left = Line(a, b);
		up = Line(b, c);
		right = Line(c, d);
		down = Line(d, a);
	}
	Figure() {
		left = Line();
		up = Line();
		right = Line();
		down = Line();
	}
	int In_Figure(int x, int y) {
		pt p = pt(x, y);
		return In_Figure(p);
	}
	int In_Figure(pt& p) {
		// wall
		//std::cerr << '\t' << down.dist(p) << std::endl;
		if (down.dist(p) > 0) {
			return 4; // об down
		}
		//std::cerr << '\t' << up.dist(p) << std::endl;
		if (up.dist(p) > 0) {
			return 3; // об up
		}
		//std::cerr << '\t' << right.dist(p) << std::endl;
		if (right.dist(p) > 0) {
			return 2; // об right
		}
		/*std::cerr << '\t' << left.dist(p) << std::endl;*/
		if (left.dist(p) > 0) {
			return 1; // об left
		}
		return 0; // Всё хорошо
	}

	Figure operator = (const Figure& f) {
		left = f.left;
		right = f.right;
		up = f.up;
		down = f.down;
		next = f.next;
		prev = f.prev;
		return *(this);
	}

	Figure* next = nullptr;
	Figure* prev = nullptr;
};