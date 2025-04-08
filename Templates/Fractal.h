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
};

class Line {
private:
	double a, b, c;
	const double EPS = 1E-9;
	void norm() {
		double z = sqrt(a * a + b * b);
		if (abs(z) > EPS)
			a /= z, b /= z, c /= z;
	}
public:
	void get_param() {
		std::cout << "(" << a << ")x + (" << b << ")y + (" << c << ") = 0" << std::endl;
	}
	double dist(pt p) const {
		return a * p.x + b * p.y + c;
	}
	Line() {
		a = 1;
		b = 1;
		c = 0;
	}
	Line(pt p, pt q) {
		a = p.y - q.y;
		b = q.x - p.x;
		c = -a * p.x - b * p.y;
		norm();
	}
	Line operator = (const Line& l) {
		a = l.a;
		b = l.b;
		c = l.c;
		return (*this);
	}
};

class Figure{
public:
	int id = 0;
	void get_param() {
		std::cout << "left  ";
		left.get_param();
		std::cout << "right ";
		right.get_param();
		std::cout << "up    ";
		up.get_param();
		std::cout << "down  ";
		down.get_param();
	}
	Figure(pt a, pt b, pt c, pt d, int i) {
		left = Line(a, b);
		up = Line(b, c);
		right = Line(c, d);
		down = Line(d, a);
		id = i;
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
	}
	Figure* next = nullptr;
	Figure* prev = nullptr;
private:
	Line left = Line();
	Line right = Line();
	Line up = Line();
	Line down = Line();
	double eps = 1e-9;
};