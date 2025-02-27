#pragma once
#include <random>
#include "Fractal.h"

class Point
{
public:
    Point(double X, double Y, Figure& f) {
        std::random_device device; // ��� ������� !!!! �� ������� !!!!
        random_generator_.seed(device());// ��� ������� !!!! �� ������� !!!!
        this->X = X;
        old_x = X;
        old_y = Y;
        this->Y = Y;
        Alive = true;
        Work = false;
        Speed = 1;
        fig = f;
        //returnRandom(10, 100) / 100.0; // ��������� ��������
    }
    double X, Y, Speed; // ���������� �, ���������� Y, 0.1 - 1 ��������,
    int Angle; // 0 - 359 �����������.
    bool Alive; // ���� �� �������
    bool Work; // � ������� ����
    Figure fig;
    void Step() { // �����������
        Angle = returnRandom(0, 359);
        if (!Work && Angle > 90 && Angle < 270) {
            if (Angle > 180) {
                Angle += 90;
            }
            else {
                Angle -= 90;
            }
        }
        auto [dx, dy] = Dif();
        double new_x = X + dx, new_y = Y + dy;
        old_x = X;
        old_y = Y;
        if (Work) {
            stepInWork(X, Y, new_x, new_y);
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

    void Reset() { // ������� ������ ���������
        X = old_x;
        Y = old_y;
    }

private:
    std::mt19937 random_generator_;
    double old_x, old_y;

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

    char InBuferZone(double x, double y) {
        if (x < -100.0) {
            Work = true;
            // �����
            return 1;
        }
        if (x > 0.0) {
            Work = true;
            // �����
            return 2;
        }
        if (y < 0.0) {
            // ������
            return 3;
        }
        if (y > 100.0) {
            // �������
            return 4;
        }
        return 0;

    }

    void stepInWork(double old_x, double old_y, double new_x, double new_y) {
        // �������� ����� ��������� 
        pt p = pt(new_x, new_y);
        auto wall = fig.In_Figure(p);
        if (wall == 0) {
            X = new_x;
            Y = new_y;
            return;
        }
        
    }

    void stepInBufer(double new_x, double new_y, bool deep = false) {
        // �������� ����� ���������� 
        char flag = InBuferZone(new_x, new_y);
        // ��������� ��
        if (flag == 0) {
            //�� �� ������
            X = new_x;
            Y = new_y;
            return;
        }
        //�� ����� ������� ����� � ���������
        if (flag == 1) {
            new_x = -100.0 - (new_x + 100.0);
        }
        if (flag == 2) {
            X = new_x + 1; Y = new_y;
            stepInWork(new_x, new_y, X, Y);
        }
        if (flag == 3) {
            new_y = abs(new_y);
        }
        if (flag == 4) {
            new_y = 100.0 - (new_y - 100.0);
        }
        if (!deep) { // ����� 2-� ��� �� ����� ����
            stepInBufer(new_x, new_y, true);
        }
    }

};
