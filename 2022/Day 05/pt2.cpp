#include "helper.hpp"
#include <regex>

void parse_stack_input(std::vector<std::string> &lines, std::vector<std::vector<char>> &stacks)
{
    int no_of_stacks = ((lines[0].size() + 1) / 4) + 1;

    for (int i = 0; i < no_of_stacks; i++)
        stacks.push_back({});
    stacks[0].push_back(' ');

    std::regex rgx("\\[(\\w+)\\]");
    std::smatch matches;

    for (std::string line : lines)
    {
        if (line.size() == 0)
            break;

        for (int i = 0; i < line.size(); i += 4)
        {
            std::string stack_str = line.substr(i, 3);
            if (std::regex_search(stack_str, matches, rgx))
            {
                std::string x = matches[1];
                char stack_val = x.at(0);

                int stack_no = (i / 4) + 1;
                stacks[stack_no].insert(stacks[stack_no].begin(), stack_val);
            }
        }
    }
}

std::string get_crate_top(std::vector<std::string> lines)
{
    std::vector<std::vector<char>> stacks;
    parse_stack_input(lines, stacks);

    for (std::string line : lines)
    {
        int crates_to_move, source, dest;
        if (sscanf(line.c_str(), "move %d from %d to %d", &crates_to_move, &source, &dest) == 3)
        {
            // get crates to be taken out in bulk
            std::vector<char> crates(crates_to_move);
            crates.assign(stacks[source].end() - crates_to_move, stacks[source].end());

            // inserts crates taken out to the back of destination stack
            std::copy(crates.begin(), crates.end(), std::back_inserter(stacks[dest]));

            // removes crates taken out from source stack
            stacks[source].resize(stacks[source].size() - crates_to_move);
        }
    }

    std::string crate_top = "";

    for (std::vector<char> stack : stacks)
    {
        crate_top += stack.back();
    }

    return crate_top;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    std::string crate_top = get_crate_top(lines);
    std::cout << "Crate Top: " << crate_top << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}