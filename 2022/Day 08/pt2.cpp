#include "helper.hpp"

int scan_tree_left(std::vector<std::vector<int>> &grid, int x, int y)
{
    int visible = 0;
    for (int tmp_x = x - 1; tmp_x >= 0; tmp_x--)
    {
        visible++;
        if (grid[y][tmp_x] >= grid[y][x])
            break;
    }
    return visible;
}

int scan_tree_right(std::vector<std::vector<int>> &grid, int x, int y)
{
    int visible = 0;
    for (int tmp_x = x + 1; tmp_x < grid[y].size(); tmp_x++)
    {
        visible++;
        if (grid[y][tmp_x] >= grid[y][x])
            break;
    }
    return visible;
}

int scan_tree_top(std::vector<std::vector<int>> &grid, int x, int y)
{
    int visible = 0;
    for (int tmp_y = y - 1; tmp_y >= 0; tmp_y--)
    {
        visible++;
        if (grid[tmp_y][x] >= grid[y][x])
            break;
    }
    return visible;
}

int scan_tree_bottom(std::vector<std::vector<int>> &grid, int x, int y)
{
    int visible = 0;
    for (int tmp_y = y + 1; tmp_y < grid.size(); tmp_y++)
    {
        visible++;
        if (grid[tmp_y][x] >= grid[y][x])
            break;
    }
    return visible;
}

int get_scenic_score(std::vector<std::vector<int>> &grid, int x, int y)
{
    int l = scan_tree_left(grid, x, y);
    int r = scan_tree_right(grid, x, y);
    int u = scan_tree_top(grid, x, y);
    int d = scan_tree_bottom(grid, x, y);
    return l * r * u * d;
}

int get_visible_trees(std::vector<std::string> lines)
{
    std::vector<std::vector<int>> grid(lines.size());

    for (int i = 0; i < lines.size(); i++)
    {
        std::string line = lines[i];
        for (char c : line)
            grid[i].push_back(c - '0');
    }

    int score = 0;

    for (int y = 1; y < grid.size() - 1; y++)
    {
        for (int x = 1; x < grid[y].size() - 1; x++)
        {
            int tmp = get_scenic_score(grid, x, y);
            if (tmp > score)
                score = tmp;
        }
    }

    return score;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int visible_trees = get_visible_trees(lines);
    std::cout << "Visible Trees: " << visible_trees << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}