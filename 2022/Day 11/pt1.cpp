#include "helper.hpp"
#include <regex>

class Monkey
{
public:
    std::vector<int> items;
    char op_symbol;
    std::string op_val;
    std::string test_op;
    int test_val;
    int monkey_id_true, monkey_id_false;
    int inspect_count;

    static bool sort_desc(const Monkey &m1, const Monkey &m2) { return m1.inspect_count > m2.inspect_count; }
};

void handle_item_line(std::string line, Monkey &monkey)
{
    std::regex rgx("Starting items: (.*)");
    std::smatch matches;

    if (std::regex_search(line, matches, rgx))
    {
        std::string item_str = matches[1];
        std::stringstream items_ss(item_str);

        for (int i; items_ss >> i;)
        {
            monkey.items.push_back(i);
            if (items_ss.peek() == ',' || items_ss.peek() == ' ')
                items_ss.ignore();
        }
    }
}

void handle_operation_line(std::string line, Monkey &monkey)
{
    std::regex rgx("Operation: new = old ([\\+*]{1}) ((old)+|\\d+)");
    std::smatch matches;

    if (std::regex_search(line, matches, rgx))
    {
        std::string op_symbol = matches[1];
        std::string op_val = matches[2];

        monkey.op_symbol = op_symbol.at(0);
        monkey.op_val = op_val;
    }
}

void handle_test_line(std::string line, Monkey &monkey)
{
    std::regex rgx("Test: (\\w+) by (\\d+)");
    std::smatch matches;

    if (std::regex_search(line, matches, rgx))
    {
        std::string test_op = matches[1];
        std::string test_val = matches[2];

        monkey.test_op = test_op;
        monkey.test_val = atoi(test_val.c_str());
    }
}

void handle_bool_line(std::string line, Monkey &monkey, bool test_success)
{
    std::string rgx_str = (test_success) ? "If true: throw to monkey (\\d+)" : "If false: throw to monkey (\\d+)";
    std::regex rgx(rgx_str);
    std::smatch matches;

    if (std::regex_search(line, matches, rgx))
    {
        if (test_success)
            monkey.monkey_id_true = atoi(matches.str(1).c_str());
        else
            monkey.monkey_id_false = atoi(matches.str(1).c_str());
    }
}

Monkey parse_monkey(std::vector<std::string> &lines, int i)
{
    Monkey monkey;
    monkey.inspect_count = 0;

    for (int j = 1; j < 6; j++)
    {
        std::string line = Helper::trim(lines[i + j]);

        if (j == 1)
            handle_item_line(line, monkey);
        else if (j == 2)
            handle_operation_line(line, monkey);
        else if (j == 3)
            handle_test_line(line, monkey);
        else if (j == 4)
            handle_bool_line(line, monkey, true);
        else if (j == 5)
            handle_bool_line(line, monkey, false);
    }

    return monkey;
}

void run_round(std::vector<Monkey> &monkeys)
{
    for (int i = 0; i < monkeys.size(); i++)
    {
        Monkey monkey = monkeys[i];
        char op_symbol = monkeys[i].op_symbol;

        for (int item : monkey.items)
        {
            monkeys[i].inspect_count++;
            int op_val = (monkey.op_val == "old") ? item : atoi(monkey.op_val.c_str());

            if (op_symbol == '*')
                item *= op_val;
            else if (op_symbol == '+')
                item += op_val;

            item /= 3;

            if (monkey.test_op == "divisible")
            {
                int remainder = item % monkey.test_val;
                if (remainder == 0)
                    monkeys[monkey.monkey_id_true].items.push_back(item);
                else
                    monkeys[monkey.monkey_id_false].items.push_back(item);
            }
        }

        monkeys[i].items.clear();
    }
}

int get_monkey_business(std::vector<std::string> &lines)
{
    std::vector<Monkey> monkeys;

    for (int i = 0; i < lines.size(); i += 7)
    {
        Monkey monkey = parse_monkey(lines, i);
        monkeys.push_back(monkey);
    }

    for (int i = 0; i < 20; i++)
    {
        run_round(monkeys);
    }

    std::sort(monkeys.begin(), monkeys.end(), Monkey::sort_desc);
    return monkeys[0].inspect_count * monkeys[1].inspect_count;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int monkey_business = get_monkey_business(lines);
    std::cout << "Monkey business: " << monkey_business << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}