#include "helper.hpp"

#define M_WIDTH 40
#define M_HEIGHT 6

typedef std::vector<char> PixelRow;
typedef std::vector<PixelRow> Monitor;

void draw_monitor(Monitor &monitor, int cycle_count, int x)
{
    int cursor_x = cycle_count % M_WIDTH,
        cursor_y = cycle_count / M_WIDTH,
        dx = abs(cursor_x - x);

    monitor[cursor_y][cursor_x] = (dx <= 1) ? '#' : ' ';
}

void print_crt_monitor(std::vector<std::string> lines)
{
    Monitor monitor(M_HEIGHT, PixelRow(M_WIDTH));
    int cycle_count = 0,
        x = 1;

    for (std::string line : lines)
    {
        if (line == "noop")
        {
            draw_monitor(monitor, cycle_count, x);
            cycle_count++;
        }
        else
        {
            std::string instruction(4, ' ');
            int val;
            if (sscanf(line.c_str(), "%s %d", &instruction[0], &val) == 2)
            {
                if (instruction == "addx")
                {
                    draw_monitor(monitor, cycle_count, x);
                    cycle_count++;
                    draw_monitor(monitor, cycle_count, x);
                    cycle_count++;
                    x += val;
                }
            }
        }
    }

    for (PixelRow row : monitor)
    {
        for (char pixel : row)
        {
            std::cout << pixel;
        }
        std::cout << std::endl;
    }
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    print_crt_monitor(lines);
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}