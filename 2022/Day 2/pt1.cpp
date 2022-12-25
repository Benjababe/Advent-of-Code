#include <helper.hpp>
#include <map>

// standardise using just "A, B, C"
std::map<char, char> decoder_map{{'X', 'A'}, {'Y', 'B'}, {'Z', 'C'}};
std::map<char, int> score_map{{'A', 1}, {'B', 2}, {'C', 3}};
std::map<char, std::map<char, int>> round_score_map;

void populate_round_score_map()
{
    round_score_map['A'] = {{'A', 3}, {'B', 6}, {'C', 0}};
    round_score_map['B'] = {{'A', 0}, {'B', 3}, {'C', 6}};
    round_score_map['C'] = {{'A', 6}, {'B', 0}, {'C', 3}};
}

int get_total_score(std::vector<std::string> lines)
{
    int total_score = 0;

    for (std::string line : lines)
    {
        char opnt, your;
        sscanf(line.c_str(), "%c %c", &opnt, &your);
        your = decoder_map[your];

        total_score += round_score_map[opnt][your] + score_map[your];
    }

    return total_score;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();

    populate_round_score_map();
    int score = get_total_score(lines);
    std::cout << "Output: " << score << std::endl;

    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}