#include "helper.hpp"

int get_partial_overlaps(std::vector<std::string> lines)
{
    int partial_overlaps = 0;

    for (std::string line : lines)
    {
        int l0, l1, r0, r1;
        sscanf(line.c_str(), "%d-%d,%d-%d", &l0, &l1, &r0, &r1);
        partial_overlaps += ((l0 <= r0 && l1 >= r0) || (r0 <= l0 && r1 >= l0));
    }

    return partial_overlaps;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int partial_overlaps = get_partial_overlaps(lines);
    std::cout << "Partial Overlaps: " << partial_overlaps << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}