#include "helper.hpp"

int get_full_overlaps(std::vector<std::string> lines)
{
    int full_overlaps = 0;

    for (std::string line : lines)
    {
        int l0, l1, r0, r1;
        sscanf(line.c_str(), "%d-%d,%d-%d", &l0, &l1, &r0, &r1);
        full_overlaps += ((l0 <= r0 && l1 >= r1) || (r0 <= l0 && r1 >= l1));
    }

    return full_overlaps;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("bigboy.txt");

    auto t1 = Helper::get_current_time();
    int full_overlaps = get_full_overlaps(lines);
    std::cout << "Full Overlaps: " << full_overlaps << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}