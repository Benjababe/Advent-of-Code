#include "helper.hpp"

int get_group_rucksack_priority(std::string l0, std::string l1, std::string l2)
{
    std::vector<char> l0_vector, l1_vector, l2_vector;
    std::copy(l0.begin(), l0.end(), std::back_inserter(l0_vector));
    std::copy(l1.begin(), l1.end(), std::back_inserter(l1_vector));
    std::copy(l2.begin(), l2.end(), std::back_inserter(l2_vector));

    std::vector<char> l01_intersect = Helper::intersect_vectors(l0_vector, l1_vector);
    std::vector<char> l012_intersect = Helper::intersect_vectors(l01_intersect, l2_vector);

    char priority = l012_intersect[0];
    if (priority > 'a')
        return priority - 'a' + 1;
    return priority - 'A' + 27;
}

int get_priority_sum(std::vector<std::string> lines)
{
    int priority = 0;

    for (int i = 0; i < lines.size(); i += 3)
    {
        priority += get_group_rucksack_priority(lines[i], lines[i + 1], lines[i + 2]);
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