#include "helper.hpp"
#include <cmath>
#include <set>
#include <tuple>

#define knot std::pair<int, int>

double get_dist(knot k1, knot k2)
{
    double x_sq = pow((k1.first - k2.first), 2),
           y_sq = pow((k1.second - k2.second), 2);
    return sqrt(x_sq + y_sq);
}

void check_tail(knot &head, knot &tail)
{
    double dist = get_dist(head, tail);

    int dx = head.first - tail.first,
        dy = head.second - tail.second;

    if (dist >= 2.0)
    {
        if (dx != 0)
            tail.first += (dx / abs(dx));
        if (dy != 0)
            tail.second += (dy / abs(dy));
    }
}

int move_rope(std::vector<std::string> lines)
{
    std::set<knot> tail_coordinates;

    knot head = {0, 0},
         tail = {0, 0};

    for (std::string line : lines)
    {
        char dir;
        int amt;
        sscanf(line.c_str(), "%c %d", &dir, &amt);

        for (int i = 0; i < amt; i++)
        {
            if (dir == 'R')
                head.first += 1;
            else if (dir == 'L')
                head.first -= 1;
            else if (dir == 'U')
                head.second += 1;
            else if (dir == 'D')
                head.second -= 1;

            check_tail(head, tail);
            tail_coordinates.insert(tail);
        }
    }
    return tail_coordinates.size();
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int positions = move_rope(lines);
    std::cout << "Tail positions: " << positions << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}