#include "helper.hpp"
#include <set>
#include <queue>
#include <tuple>

typedef std::tuple<int, int, int> Coord3D;

std::vector<Coord3D> get_neighbours(Coord3D droplet)
{
    std::vector<Coord3D> neighbours;
    int x = std::get<0>(droplet),
        y = std::get<1>(droplet),
        z = std::get<2>(droplet);

    neighbours.push_back(std::make_tuple(x - 1, y, z));
    neighbours.push_back(std::make_tuple(x + 1, y, z));
    neighbours.push_back(std::make_tuple(x, y - 1, z));
    neighbours.push_back(std::make_tuple(x, y + 1, z));
    neighbours.push_back(std::make_tuple(x, y, z - 1));
    neighbours.push_back(std::make_tuple(x, y, z + 1));

    return neighbours;
}

int get_surface_area(std::vector<std::string> lines)
{
    int surface_area = 0;
    int min_vals[] = {INT32_MAX, INT32_MAX, INT32_MAX};
    int max_vals[] = {0, 0, 0};
    std::set<Coord3D> droplets;
    std::set<Coord3D> boundary;
    std::set<Coord3D> outside_air;
    std::queue<Coord3D> queue;
    queue.push(std::make_tuple(0, 0, 0));

    for (std::string line : lines)
    {
        int x, y, z;
        if (sscanf(line.c_str(), "%d,%d,%d", &x, &y, &z) == 3)
        {
            droplets.insert(std::make_tuple(x, y, z));

            if (x < min_vals[0])
                min_vals[0] = x;
            if (y < min_vals[1])
                min_vals[1] = y;
            if (z < min_vals[2])
                min_vals[2] = z;

            if (x > max_vals[0])
                max_vals[0] = x;
            if (y > max_vals[1])
                max_vals[1] = y;
            if (z > max_vals[2])
                max_vals[2] = z;
        }
    }

    for (int x = min_vals[0] - 2; x < max_vals[0] + 2; x++)
    {
        for (int y = min_vals[1] - 2; y < max_vals[1] + 2; y++)
        {
            for (int z = min_vals[2] - 2; z < max_vals[2] + 2; z++)
            {
                boundary.insert(std::make_tuple(x, y, z));
            }
        }
    }

    while (!queue.empty())
    {
        Coord3D air = queue.front();
        queue.pop();

        if (boundary.find(air) != boundary.end() &&
            outside_air.find(air) == outside_air.end())
        {
            outside_air.insert(air);
            std::vector<Coord3D> neighbours = get_neighbours(air);
            for (Coord3D neighbour : neighbours)
            {
                if (droplets.find(neighbour) != droplets.end())
                    surface_area += 1;
                else
                    queue.push(neighbour);
            }
        }
    }

    return surface_area;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int surface_area = get_surface_area(lines);
    std::cout << "Surface area: " << surface_area << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}