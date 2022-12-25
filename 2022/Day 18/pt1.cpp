#include "helper.hpp"
#include <set>
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
    std::set<Coord3D> droplets;

    for (std::string line : lines)
    {
        int x, y, z;
        if (sscanf(line.c_str(), "%d,%d,%d", &x, &y, &z) == 3)
        {
            droplets.insert(std::make_tuple(x, y, z));
            surface_area += 6;
        }
    }

    for (Coord3D droplet : droplets)
    {
        std::vector<Coord3D> neighbours = get_neighbours(droplet);
        for (Coord3D neighbour : neighbours)
        {
            if (droplets.find(neighbour) != droplets.end())
                surface_area--;
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