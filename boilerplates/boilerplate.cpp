#include "helper.hpp"

int func(std::vector<std::string> lines)
{
    return 0;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int output = func(lines);
    std::cout << "Output: " << output << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}