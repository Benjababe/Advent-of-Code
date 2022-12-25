#include "helper.hpp"
#include <map>

#define SIZE 4

bool check_unique(std::string substring)
{
    std::map<char, int> char_map;
    for (char c : substring)
    {
        if (char_map[c] == 1)
            return false;
        char_map[c] = 1;
    }
    return true;
}

int get_start_of_packet(std::string line)
{
    for (int i = SIZE; i <= line.size(); i++)
    {
        std::string substring = line.substr(i - SIZE, SIZE);
        if (check_unique(substring))
            return i;
    }

    return -1;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");
    std::string line = lines[0];

    auto t1 = Helper::get_current_time();
    int start_of_packet = get_start_of_packet(line);
    std::cout << "Start of Packet: " << start_of_packet << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}