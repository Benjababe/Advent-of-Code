#include "helper.hpp"

int get_rucksack_priority(std::string line)
{
    std::string l = line.substr(0, line.size() / 2);
    std::string r = line.substr(line.size() / 2, line.size());

    std::vector<char> l_vector, r_vector, lr_intersect;
    std::copy(l.begin(), l.end(), std::back_inserter(l_vector));
    std::copy(r.begin(), r.end(), std::back_inserter(r_vector));
    lr_intersect = Helper::intersect_vectors(l_vector, r_vector);

    char priority = lr_intersect[0];
    if (priority > 'a')
        return priority - 'a' + 1;
    return priority - 'A' + 27;
}

int get_priority_sum(std::vector<std::string> lines)
{
    int priority = 0;

    for (std::string line : lines)
    {
        priority += get_rucksack_priority(line);
    }

    return priority;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int output = get_priority_sum(lines);
    std::cout << "Output: " << output << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}