#include "helper.hpp"

void check_strength(int &strength, int cycle_count, int x)
{
    if (cycle_count == 20 || cycle_count == 60 ||
        cycle_count == 100 || cycle_count == 140 ||
        cycle_count == 180 || cycle_count == 220)
        strength += (cycle_count * x);
}

int print_crt_monitor(std::vector<std::string> lines)
{
    int strength = 0,
        cycle_count = 0,
        x = 1;

    for (std::string line : lines)
    {
        if (line == "noop")
        {
            cycle_count++;
            check_strength(strength, cycle_count, x);
        }
        else
        {
            std::string instruction(4, ' ');
            int val;
            if (sscanf(line.c_str(), "%s %d", &instruction[0], &val) == 2)
            {
                if (instruction == "addx")
                {
                    cycle_count++;
                    check_strength(strength, cycle_count, x);
                    cycle_count++;
                    check_strength(strength, cycle_count, x);
                    x += val;
                }
            }
        }
    }

    return strength;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int strength = print_crt_monitor(lines);
    std::cout << "Signal strength: " << strength << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}