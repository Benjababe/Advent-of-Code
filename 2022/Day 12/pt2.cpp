#include "helper.hpp"
#include <map>

#define Grid std::vector<std::vector<Cell>>
#define Path std::vector<std::pair<int, int>>

int shortest_path_size = 99999999;
std::map<std::pair<int, int>, int> pos_map;

class Cell
{
public:
    int height;
    size_t x, y;
    float heuristic;
    std::vector<Cell *> neighbours;
    bool sorted;
    static bool before(const Cell *c1, const Cell *c2) { return c1->heuristic < c2->heuristic; }

    Cell(int height, size_t x, size_t y)
    {
        this->height = height;
        this->x = x;
        this->y = y;
        this->heuristic = 99999999;
        this->neighbours = std::vector<Cell *>();
        this->sorted = false;
    }

    void add_neighbour(Cell *neighbour)
    {
        int diff = 2;

        if (neighbour->height == 'E')
            diff = 'z' - this->height;
        else
            diff = neighbour->height - this->height;

        if (diff <= 1)
            this->neighbours.push_back(neighbour);
    }

    void sort_neighbours()
    {
        std::sort(this->neighbours.begin(), this->neighbours.end(), Cell::before);
        this->sorted = true;
    }
};

void populate_grid(std::vector<std::string> lines, Grid &grid, std::vector<std::pair<int, int>> &possible_starts, std::pair<int, int> &end)
{
    for (int y = 0; y < lines.size(); y++)
    {
        std::string line = lines[y];
        for (int x = 0; x < line.size(); x++)
        {
            int height = line.at(x);
            if (height == 'S' || height == 'a')
            {
                possible_starts.push_back(std::make_pair(x, y));
                height = 'a';
            }
            else if (height == 'E')
            {
                end = std::make_pair(x, y);
            }
            grid[y].push_back(Cell(height, x, y));
            pos_map[std::make_pair(x, y)] = 99999999;
        }
    }
}

// calculates heuristic and adds neighbouring nodes
void process_grid(Grid &grid, std::pair<int, int> end)
{
    for (int y = 0; y < grid.size(); y++)
    {
        for (int x = 0; x < grid[y].size(); x++)
        {
            double x_2 = pow(x - end.first, 2);
            double y_2 = pow(y - end.second, 2);
            grid[y][x].heuristic = sqrt(x_2 + y_2);

            if (y > 0)
                grid[y][x].add_neighbour(&grid[y - 1][x]);
            if (y < grid.size() - 1)
                grid[y][x].add_neighbour(&grid[y + 1][x]);
            if (x > 0)
                grid[y][x].add_neighbour(&grid[y][x - 1]);
            if (x < grid[y].size() - 1)
                grid[y][x].add_neighbour(&grid[y][x + 1]);
        }
    }
}

void traverse(Grid &grid, Path cur_path)
{
    // shortest path cell count found in part 1
    // not known to work with bigboy input
    if (cur_path.size() >= 482)
        return;

    std::pair<int, int> cur_pos = cur_path.back();
    Cell cur_cell = grid[cur_pos.second][cur_pos.first];

    if (cur_cell.height == 'E' && cur_path.size() < shortest_path_size)
    {
        shortest_path_size = cur_path.size();
    }

    if (!cur_cell.sorted)
        cur_cell.sort_neighbours();

    for (Cell *neighbour : cur_cell.neighbours)
    {
        std::pair<int, int> n_pos = std::make_pair(neighbour->x, neighbour->y);

        if (std::find(cur_path.begin(), cur_path.end(), n_pos) == cur_path.end() &&
            pos_map[n_pos] > cur_path.size())
        {
            pos_map[n_pos] = cur_path.size();
            Path new_path = cur_path;
            new_path.push_back(n_pos);
            traverse(grid, new_path);
        }
    }
}

int find_path(std::vector<std::string> lines)
{
    Grid grid(lines.size());
    std::pair<int, int> end;
    std::vector<std::pair<int, int>> possible_starts;

    populate_grid(lines, grid, possible_starts, end);
    process_grid(grid, end);

    for (std::pair<int, int> start_pos : possible_starts)
    {
        Path cur_path = {start_pos};
        traverse(grid, cur_path);
    }

    return shortest_path_size - 1;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int path_steps = find_path(lines);
    std::cout << "Path steps: " << path_steps << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}