#include <string>
class Line {
private:
	double a, b, c;
	pt st = pt(0,0);
	const double EPS = 1E-9;
	void norm() {
		double z = sqrt(a * a + b * b);
		if (abs(z) > EPS)
			a /= z, b /= z, c /= z;
	}
public:
	std::string get_param() {
		std::cout << "(" << a << ")x + (" << b << ")y + (" << c << ") = 0" << std::endl;
		return ("(" + std::to_string(a) + ")x + (" + std::to_string(b) + ")y + (" + std::to_string(c) + ") = 0");
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
		st = p;
		norm();
	}
	Line operator = (const Line& l) {
		a = l.a;
		b = l.b;
		c = l.c;
		return (*this);
	}
};