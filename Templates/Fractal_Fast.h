#pragma once
#include "struct_pt.h"
#include "Line.h"
#include <string>
#include <set>

class Figure{
private:
	int need_cath(pt& p) {
		// wall
		//std::cerr << '\t' << down.dist(p) << std::endl;
		if (abs(down.dist(p)) > 0.5) {
			return 2; // down
		}
		//std::cerr << '\t' << up.dist(p) << std::endl;
		if (abs(up.dist(p)) > 0.5) {
			return 1; // up
		}
		if (next == nullptr && abs(right.dist(p)) > 0.5) {
			return 3; // right
		}
		return 0; // not need
	}
	int In_Figure(pt& p) {
		// wall
		//std::cerr << '\t' << down.dist(p) << std::endl;
		if (down.dist(p) > 0) {
			return 4; // �� down
		}
		//std::cerr << '\t' << up.dist(p) << std::endl;
		if (up.dist(p) > 0) {
			return 3; // �� up
		}
		//std::cerr << '\t' << right.dist(p) << std::endl;
		if (right.dist(p) > 0) {
			return 2; // �� right
		}
		/*std::cerr << '\t' << left.dist(p) << std::endl;*/
		if (left.dist(p) > 0) {
			return 1; // �� left
		}
		return 0; // �� ������
	}
	Line left = Line();
	Line right = Line();
	Line up = Line();
	Line down = Line();
	double eps = 1e-9;
public:
	std::string get_info() {
		return "left :" + left.get_param() + "\nright :" + right.get_param() + "\nup :" + up.get_param() +"\ndown :" + down.get_param() + "\n";
	}
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
	std::set<int> up_trap;
	std::set<int> down_trap;
	std::set<int> right_trap;
	void add_trap(int id, int wall) {
		if (wall == 1) {
			up_trap.insert(id);
		}
		if (wall == 2) {
			down_trap.insert(id);
		}
		if (wall == 3) {
			right_trap.insert(id);
		}
	}
	int need_cath(double x, double y) {
		pt p = pt(x, y);
		return need_cath(p);
	}
};