#include "helper.hpp"
#include <cmath>
#include <set>
#include <tuple>

#define KNOT_COUNT 10
#define knot std::pair<int, int>

double get_dist(knot k1, knot k2)
{
    double x_sq = pow((k1.first - k2.first), 2),
           y_sq = pow((k1.second - k2.second), 2);
    return sqrt(x_sq + y_sq);
}

void check_knot(std::vector<knot> &knots, int i1, int i2)
{
    knot k1 = knots[i1], k2 = knots[i2];
    double dist = get_dist(k1, k2);

    int dx = k1.first - k2.first,
        dy = k1.second - k2.second;

    if (dist >= 2.0)
    {
        if (dx != 0)
            knots[i2].first += (dx / abs(dx));
        if (dy != 0)
            knots[i2].second += (dy / abs(dy));
    }
}

int move_rope(std::vector<std::string> lines)
{
    std::set<knot> tail_coordinates;

    std::vector<knot> knots;
    for (int i = 0; i < KNOT_COUNT; i++)
        knots.push_back(std::make_pair(0, 0));

    for (std::string line : lines)
    {
        char dir;
        int amt;
        sscanf(line.c_str(), "%c %d", &dir, &amt);

        for (int i = 0; i < amt; i++)
        {
            if (dir == 'R')
                knots[0].first += 1;
            else if (dir == 'L')
                knots[0].first -= 1;
            else if (dir == 'U')
                knots[0].second += 1;
            else if (dir == 'D')
                knots[0].second -= 1;

            for (int k = 0; k < KNOT_COUNT - 1; k++)
            {
                check_knot(knots, k, k + 1);
            }

            tail_coordinates.insert(knots[KNOT_COUNT - 1]);
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