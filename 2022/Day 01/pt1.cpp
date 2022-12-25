#include "helper.hpp"

int get_max_calories(std::vector<std::string> lines)
{
    int max_calories = 0;
    int current_calories = 0;

    for (std::string line : lines)
    {
        if (line == "")
        {
            if (current_calories > max_calories)
                max_calories = current_calories;
            current_calories = 0;
        }
        else
        {
            current_calories += std::atoi(line.c_str());
        }
    }

    return max_calories;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int calories = get_max_calories(lines);
    std::cout << "Max Calories: " << calories << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}