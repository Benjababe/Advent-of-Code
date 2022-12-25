#include "helper.hpp"
#include <set>
#include <tuple>

typedef std::vector<std::vector<std::vector<char>>> Grid;
typedef std::pair<int, int> Coord;

void setup_grid(Grid &grid, std::vector<std::string> &lines)
{
    for (size_t y = 0; y < lines.size(); y++)
    {
        std::string line = lines[y];
        for (size_t x = 0; x < line.size(); x++)
        {
            char c = line.at(x);
            grid[y][x].push_back(c);
        }
    }
}

void update_blizzard_cell(Grid &grid, Grid &next_grid, size_t x, size_t y)
{
    for (char blizzard : grid[y][x])
    {
        size_t t_x = x,
               t_y = y;

        if (blizzard == '^')
        {
            if (t_y == 1)
                t_y = next_grid.size() - 2;
            else
                t_y--;
        }
        else if (blizzard == 'v')
        {
            if (t_y == next_grid.size() - 2)
                t_y = 1;
            else
                t_y++;
        }
        else if (blizzard == '>')
        {
            if (t_x == next_grid[y].size() - 2)
                t_x = 1;
            else
                t_x++;
        }
        else if (blizzard == '<')
        {
            if (t_x == 1)
                t_x = next_grid[y].size() - 2;
            else
                t_x--;
        }

        next_grid[t_y][t_x].push_back(blizzard);
    }
}

Grid update_grid(Grid grid)
{
    Grid next_grid{grid.size(), std::vector<std::vector<char>>(grid[0].size(), std::vector<char>())};

    for (size_t y = 0; y < grid.size(); y++)
    {
        for (size_t x = 0; x < grid[y].size(); x++)
        {
            // copy wall directly
            if (grid[y][x][0] == '#')
                next_grid[y][x] = {'#'};
            else
            {
                // if cell contains blizzards, update them
                std::vector<char> isect = Helper::intersect_vectors(grid[y][x], {'^', '>', '<', 'v'});
                if (isect.size() > 0)
                    update_blizzard_cell(grid, next_grid, x, y);
            }
        }
    }

    // fill empty cells with '.' for ground
    for (size_t y = 0; y < next_grid.size(); y++)
    {
        for (size_t x = 0; x < next_grid[y].size(); x++)
        {
            if (next_grid[y][x].size() == 0)
                next_grid[y][x].push_back('.');
        }
    }

    return next_grid;
}

int traverse(Grid &grid, Coord start, Coord end, int trip)
{
    std::vector<std::tuple<Coord, int>> queue = {std::make_tuple(start, 0)};
    std::set<std::tuple<Coord, int>> visited;
    int cur_time = 0;

    while (!queue.empty())
    {
        Coord cur_coord = std::get<0>(queue[0]);
        int x = cur_coord.first,
            y = cur_coord.second;
        int time = std::get<1>(queue[0]);
        queue.erase(queue.begin());

        // if reached end, check if more trips are needed
        // else return time taken for the current trip
        if (cur_coord == end)
        {
            if (trip == 1)
                std::cout << "Time taken for first trip: " << time << std::endl;
            if (trip < 3)
                return time + traverse(grid, end, start, trip + 1);
            else
                return time;
        }

        // next time instance is reached
        if (time > cur_time)
        {
            cur_time++;
            grid = update_grid(grid);
        }

        // if current cell is blizzard, skip
        if (grid[y][x].size() != 1 || grid[y][x][0] != '.')
            continue;

        time++;

        std::vector<Coord> possible_coords;
        std::vector<Coord> offsets = {std::make_pair(-1, 0),
                                      std::make_pair(1, 0),
                                      std::make_pair(0, 0),
                                      std::make_pair(0, -1),
                                      std::make_pair(0, 1)};

        for (Coord offset : offsets)
        {
            int t_x = x + offset.first,
                t_y = y + offset.second;

            // check if coord is within bounds and is not a wall
            if (t_y >= 0 && t_y < grid.size() &&
                t_x >= 0 && t_x <= grid[t_y].size() &&
                grid[t_y][t_x][0] != '#')
                possible_coords.push_back(std::make_pair(t_x, t_y));
        }

        for (Coord coord : possible_coords)
        {
            // skip coord if we've already visited it at the current time (duplicate visit)
            std::tuple<Coord, int> key = std::make_tuple(coord, time);
            if (visited.find(key) == visited.end())
            {
                visited.insert(key);
                queue.push_back(key);
            }
        }
    }

    return 0;
}

int get_path_time(std::vector<std::string> lines)
{
    Grid grid{lines.size(), std::vector<std::vector<char>>(lines[0].size(), std::vector<char>())};
    setup_grid(grid, lines);

    Coord start = std::make_pair(1, 0),
          end = std::make_pair(grid[0].size() - 2, grid.size() - 1);
    int time = traverse(grid, start, end, 1);

    return time;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();

    int time = get_path_time(lines);
    std::cout << "Time taken for 3 trips: " << time << std::endl;

    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}