#pragma once
#include <random>
#include <vector>
#include "Trap_Fast.h"
#include "Fractal_Fast.h"

struct BuferZone{
    double left;
    double right;
    double up;
    double down;
    BuferZone(double gran_right,double gran_up, double gran_down, double gran_left) {
        right = gran_right;
        left = gran_left;
        up = gran_up;
        down = gran_down;
    }
    BuferZone() :left(-1000), right(0), up(1000), down(0) {}
};

class Point
{
public:
    Point(double X, double Y, Figure* f, double up, double down, double left, double right) {
        std::random_device device; // ��� ������� !!!! �� ������� !!!!
        random_generator_.seed(device());// ��� ������� !!!! �� ������� !!!!
        this->X = X;
        this->Y = Y;
        Alive = true;
        Work = false;
        Speed = 1;
        fig = f;
        buf = BuferZone(right, up, down, left);
        //std::cerr << buf.up << ' ' << buf.down << ' ' << buf.left << ' ' << buf.right << std::endl;
        //returnRandom(10, 100) / 100.0; // ��������� ��������
    }
    double X, Y, Speed; // ���������� �, ���������� Y, 0.1 - 1 ��������,
    int Angle = 0; // 0 - 359 �����������.
    bool Alive; // ���� �� �������
    bool Work; // � ������� ����
    Figure* fig;

    void Step() { // �����������
        Angle = returnRandom(0, 359);
        if (!Work && Angle > 90 && Angle < 270) {
            if (Angle > 180) {
                Angle += 90;
            }
            else {
                if (Angle == 180) {
                    Angle = 0;
                }
                else
                {
                    Angle -= 90;
                }
            }
        }
        auto [dx, dy] = Dif();
        double new_x = X + dx, new_y = Y + dy;
        if (Work) {
            stepInWork(new_x, new_y);
        }
        else {
            stepInBufer(new_x, new_y);
        }
    }

    bool Same(Point* other) {
        return ((abs(other->X - X) < 0) && (abs(other->Y - Y) < 0));
    }

    bool Same(Point& other) {
        return ((abs(other.X - X) < 0) && (abs(other.Y - Y) < 0));
    }

    bool try_cath(std::vector<Trap>& Traps) {
        auto f = fig->need_cath(X, Y);
        if (f != 0) {
            if (f == 1) {
                for (auto& i : fig->up_trap) {
                    if (Traps[i].Cath(X,Y)) {
                        std::cerr << "Ctach\n";
                        fig->up_trap.erase(i);
                        Alive = false;
                        return true;
                    }
                }
            }
            if (f == 2) {
                for (auto& i : fig->down_trap) {
                    if (Traps[i].Cath(X,Y)) {
                        fig->down_trap.erase(i);
                        std::cerr << "Ctach\n";

                        Alive = false;
                        return true;
                    }
                }
            }
            if (f == 3) {
                for (auto& i : fig->right_trap) {
                    if (Traps[i].Cath(X,Y)) {
                        fig->right_trap.erase(i);
                        std::cerr << "Ctach\n";

                        Alive = false;
                        return true;
                    }
                }
            }
            return false;
        }
        else {
            return false;
        }
    }

private:
    std::mt19937 random_generator_;
    BuferZone buf = BuferZone();
    int returnRandom(int min, int max) {
        if (max < min) std::swap(max, min);
        std::uniform_int_distribution<int> range(min, max);
        return range(random_generator_);
    }

    std::pair <double, double> Dif() {
        double Angle = this->Angle * acos(-1) / 180;
        double x = (cos(Angle) * Speed);
        double y = (sin(Angle) * Speed);
        return { x,y };
    }

    char InBufer(int x, int y) {
        if (y > buf.up) {
            return 4; // up
        }
        if (y < buf.down) {
            return 3; // down
        }
        if (x > buf.right) {
            return 2; // right
        }
        if (x < buf.left) {
            return 1; // left
        }
        return 0;
    }

    void stepInBufer(double new_x, double new_y, bool deep = false) {
        // �������� ����� ���������� 
        char flag = InBufer(new_x, new_y);
        // ��������� ��
        if (flag == 0) {
            //�� �� ������
            X = new_x;
            Y = new_y;
            return;
        }
        //�� ����� ������� ����� � ���������
        if (flag == 1) { // left
            new_x = buf.left - abs(new_x - buf.left);
        }
        if (flag == 2) { // right
            X = new_x + 1; Y = new_y;
            (*this).Work = true;
            stepInWork(new_x + 1, new_y);
        }
        if (flag == 3) { // down
            new_y = buf.down + abs(new_y - buf.down);
        }
        if (flag == 4) { // up
            new_y = buf.up - abs(new_y - buf.up);
        }
        if (!deep) { // ����� 2-� ��� �� ����� ����
            stepInBufer(new_x, new_y, true);
        }
    }

    void stepInWork(double x, double y) {
        auto f = fig->In_Figure(x,y);
        if (f == 0) {
            X = x;
            Y = y;
        }
        if (f == 1) {
            if (fig->prev != nullptr) {
                fig = fig->prev;
                f = fig->In_Figure(x, y);
                if (f == 0) {
                    X = x;
                    Y = y;
                }
                else {
                    fig = fig->next;
                }
            }
        }
        if (f == 2) {
            if (fig->next != nullptr) {
                fig = fig->next;
                f = fig->In_Figure(x, y);
                if (f == 0) {
                    X = x;
                    Y = y;
                }
                else {
                    fig = fig->prev;
                }
            }
        }
    }
};
