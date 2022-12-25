#include <algorithm>
#include "helper.hpp"

int get_top_3_calories(std::vector<std::string> lines)
{
    std::vector<int> elves;
    int current_calories = 0;

    for (std::string line : lines)
    {
        if (line == "")
        {
            elves.push_back(current_calories);
            current_calories = 0;
        }
        else
        {
            current_calories += std::atoi(line.c_str());
        }
    }

    // sort in descending order
    std::sort(elves.begin(), elves.end(), std::greater<int>());
    return elves[0] + elves[1] + elves[2];
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int calories = get_top_3_calories(lines);
    std::cout << "Max Calories: " << calories << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}