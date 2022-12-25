#include "helper.hpp"

typedef std::vector<std::vector<char>> Grid;
typedef std::vector<char> GridRow;

struct Rock
{
    int id, height;
    Grid pattern;
};

std::vector<Rock> get_rocks()
{
    std::vector<Rock> rocks;
    Grid pattern;

    pattern = {
        {'.', '.', '.', '.'},
        {'.', '.', '.', '.'},
        {'.', '.', '.', '.'},
        {'@', '@', '@', '@'}};
    rocks.push_back({1, 1, pattern});

    pattern = {
        {'.', '.', '.', '.'},
        {'.', '@', '.', '.'},
        {'@', '@', '@', '.'},
        {'.', '@', '.', '.'}};
    rocks.push_back({2, 3, pattern});

    pattern = {
        {'.', '.', '.', '.'},
        {'.', '.', '@', '.'},
        {'.', '.', '@', '.'},
        {'@', '@', '@', '.'}};
    rocks.push_back({3, 3, pattern});

    pattern = {
        {'@', '.', '.', '.'},
        {'@', '.', '.', '.'},
        {'@', '.', '.', '.'},
        {'@', '.', '.', '.'}};
    rocks.push_back({4, 4, pattern});

    pattern = {
        {'.', '.', '.', '.'},
        {'.', '.', '.', '.'},
        {'@', '@', '.', '.'},
        {'@', '@', '.', '.'}};
    rocks.push_back({5, 2, pattern});

    return rocks;
}

void print_grid(Grid &grid)
{
    // for (GridRow grid_row : grid)
    // {
    //     for (char c : grid_row)
    //     {
    //         std::cout << c;
    //     }
    //     std::cout << std::endl;
    // }
    // std::cout << std::endl;
}

void clear_grid(Grid &grid, std::vector<std::pair<int, int>> &rock_coords)
{
    for (std::pair<int, int> coord : rock_coords)
    {
        grid[coord.second][coord.first] = '.';
    }
    rock_coords.clear();
}

int highest_rock_index(Grid &grid)
{
    for (int y = 0; y < grid.size(); y++)
    {
        for (char c : grid[y])
        {
            if (c == '-' || c == '#')
                return y;
        }
    }
    return 0;
}

void draw_rock(Grid &grid, Rock rock,
               std::vector<std::pair<int, int>> &rock_coords, std::pair<int, int> &rock_offset)
{
    // find y position to start falling from
    int initial_y = highest_rock_index(grid) - 3;

    // if rock hasn't started falling yet
    bool initial = (rock_coords.size() == 0 || rock_offset.second == 0);

    // clear previously drawn rocks from the grid
    for (std::pair<int, int> coord : rock_coords)
    {
        grid[coord.second][coord.first] = '.';
    }
    rock_coords.clear();

    for (int i = 1; i <= rock.height; i++)
    {
        // go in reverse order
        Grid tmp = rock.pattern;
        std::reverse(tmp.begin(), tmp.end());
        GridRow rock_row = tmp[i - 1];

        for (int x = 0; x < rock_row.size(); x++)
        {
            if (rock_row[x] == '@')
            {
                // x + 3 because it will be 2 units from the wall
                int x_pos = x + 3 + rock_offset.first,
                    y_pos = initial_y - i + ((initial) ? 0 : rock_offset.second);

                rock_coords.push_back(std::make_pair(x_pos, y_pos));
                grid[y_pos][x_pos] = '@';
            }
        }
    }
}

int get_tower_height(Grid &grid)
{
    int highest_rock = highest_rock_index(grid);
    int height = grid.size() - highest_rock - 1;
    return height;
}

bool check_left(Grid &grid, std::vector<std::pair<int, int>> &rock_coords)
{
    for (std::pair<int, int> coord : rock_coords)
    {
        char left_cell = grid[coord.second][coord.first - 1];
        if (left_cell == '#' || left_cell == '|')
            return false;
    }
    return true;
}

bool check_right(Grid &grid, std::vector<std::pair<int, int>> &rock_coords)
{
    for (std::pair<int, int> coord : rock_coords)
    {
        char right_cell = grid[coord.second][coord.first + 1];
        if (right_cell == '#' || right_cell == '|')
            return false;
    }
    return true;
}

bool check_btm(Grid &grid, std::vector<std::pair<int, int>> &rock_coords)
{
    for (std::pair<int, int> coord : rock_coords)
    {
        char btm_cell = grid[coord.second + 1][coord.first];
        if (btm_cell == '#' || btm_cell == '-')
            return false;
    }
    return true;
}

bool check_rock_stopped(Grid &grid, std::vector<std::pair<int, int>> &rock_coords)
{
    int x = 0;
    for (std::pair<int, int> coord : rock_coords)
    {
        char btm_cell = grid[coord.second + 1][coord.first];
        if (btm_cell == '#' || btm_cell == '-')
            return true;
    }
    return false;
}

void land_rock(Grid &grid, std::vector<std::pair<int, int>> &rock_coords)
{
    for (std::pair<int, int> coord : rock_coords)
    {
        grid[coord.second][coord.first] = '#';
    }
    rock_coords.clear();
}

int get_final_tower_height(std::vector<std::string> lines)
{
    std::string jet_patterns = lines[0];
    int highest_rock = 0,
        jet_pattern_len = jet_patterns.size(),
        jet_index = 0,
        rock_index = 0,
        rock_count = 2022;

    std::vector<Rock> rocks = get_rocks();

    Grid grid = {{'+', '-', '-', '-', '-', '-', '-', '-', '+'}};

    for (rock_index; rock_index < rock_count; rock_index++)
    {
        Rock rock = rocks[rock_index % rocks.size()];
        std::vector<std::pair<int, int>> rock_coords;
        std::pair<int, int> rock_offset = std::make_pair(0, 0);
        bool rock_falling = true,
             initial = true;

        highest_rock = highest_rock_index(grid);

        for (int i = 0; i < (3 - highest_rock + rock.height); i++)
            grid.insert(grid.begin(), {'|', '.', '.', '.', '.', '.', '.', '.', '|'});

        while (rock_falling)
        {
            if (initial)
            {
                draw_rock(grid, rock, rock_coords, rock_offset);
                print_grid(grid);
                initial = false;
            }

            char jet = jet_patterns[jet_index % jet_pattern_len];
            jet_index++;

            if (jet == '<' && check_left(grid, rock_coords))
            {
                rock_offset.first--;
                draw_rock(grid, rock, rock_coords, rock_offset);
                print_grid(grid);
            }

            if (jet == '>' && check_right(grid, rock_coords))
            {
                rock_offset.first++;
                draw_rock(grid, rock, rock_coords, rock_offset);
                print_grid(grid);
            }

            if (check_rock_stopped(grid, rock_coords))
            {
                land_rock(grid, rock_coords);
                print_grid(grid);
                rock_falling = false;
            }

            if (rock_falling)
            {
                rock_offset.second++;
                draw_rock(grid, rock, rock_coords, rock_offset);
                print_grid(grid);
            }
        }
    }

    int height = get_tower_height(grid);
    return height;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int tower_height = get_final_tower_height(lines);
    std::cout << "Tower height: " << tower_height << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}