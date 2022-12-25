#include "helper.hpp"
#include <regex>
#include <stdlib.h>

#define X_DEC 0

typedef std::vector<std::vector<char>> Grid;

void print_grid(Grid &grid)
{
    for (size_t y = 0; y < grid.size(); y++)
    {
        for (size_t x = 0; x < grid[y].size(); x++)
        {
            std::cout << grid[y][x];
        }
        std::cout << std::endl;
        std::cout << std::endl;
    }
}

void populate_grid(Grid &grid, std::vector<std::string> &lines)
{
    std::regex line_rgx("(\\d+,\\d+)");
    std::smatch matches;

    int max_y = 0;

    for (std::string line : lines)
    {
        line = Helper::trim(line);
        std::vector<std::pair<int, int>> coords;

        while (std::regex_search(line, matches, line_rgx))
        {
            std::string coord_str = matches[0].str();
            line = matches.suffix().str();
            int x, y;
            if (sscanf(coord_str.c_str(), "%d,%d", &x, &y) == 2)
            {
                coords.push_back(std::make_pair(x - X_DEC, y));
            }
        }

        for (size_t i = 0; i < coords.size() - 1; i++)
        {
            std::pair<int, int> c1 = coords[i],
                                c2 = coords[i + 1];
            int x1 = __min(c1.first, c2.first),
                x2 = __max(c1.first, c2.first),
                y1 = __min(c1.second, c2.second),
                y2 = __max(c1.second, c2.second);

            if (y2 > max_y)
                max_y = y2;

            if (x1 == x2)
            {
                for (size_t y = y1; y < y2 + 1; y++)
                    grid[y][x1] = '#';
            }
            else if (y1 == y2)
            {
                for (size_t x = x1; x < x2 + 1; x++)
                    grid[y1][x] = '#';
            }
        }
    }

    for (size_t x = 0; x < grid[max_y + 2].size(); x++)
        grid[max_y + 2][x] = '#';
    grid.erase(grid.begin() + max_y + 3, grid.end());
}

int simulate_sand_fall(Grid &grid)
{
    bool cond = true;
    int sand_count = 0;

    while (cond)
    {
        int sx = 500 - X_DEC,
            sy = 0;

        while (grid[sy][sx] == '+' || grid[sy][sx] == '.')
        {
            if (sy == grid.size() - 1 || grid[0][500] == 'O')
            {
                cond = false;
                break;
            }

            if (grid[sy + 1][sx] == '.')
                sy += 1;
            else if (grid[sy + 1][sx - 1] == '.')
            {
                sy += 1;
                sx -= 1;
            }
            else if (grid[sy + 1][sx + 1] == '.')
            {
                sy += 1;
                sx += 1;
            }
            else
            {
                grid[sy][sx] = 'O';
                sand_count += 1;
                break;
            }
        }

        if (grid[0][500 - X_DEC] == 'O')
        {
            cond = false;
            break;
        }
    }

    return sand_count;
}

int get_still_sand(std::vector<std::string> &lines)
{
    Grid grid(300, std::vector<char>(1000 - X_DEC, '.'));
    grid[0][500 - X_DEC] = '+';

    populate_grid(grid, lines);
    int sand_count = simulate_sand_fall(grid);

    return sand_count;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int still_sand = get_still_sand(lines);
    std::cout << "Still sand: " << still_sand << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}