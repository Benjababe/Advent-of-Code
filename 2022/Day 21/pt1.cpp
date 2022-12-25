#include "helper.hpp"
#include <map>
#include <variant>

typedef long long llong;

#define MonkeyMap std::map<std::string, std::variant<Combination, double>>

struct Combination
{
    std::string m1, m2;
    char op;
};

void setup_monkey(std::string line, MonkeyMap &monkeys)
{
    std::string m(4, ' '), l(4, ' '), r(4, ' ');
    double val;
    char op;

    const char *s1 = "%4s: %4s %c %4s";
    const char *s2 = "%4s: %lf";

    int c1 = sscanf(line.c_str(), s1, &m[0], &l[0], &op, &r[0]);
    int c2 = sscanf(line.c_str(), s2, &m[0], &val);

    if (c1 == 4)
        monkeys[m] = Combination{l, r, op};
    else if (c2 == 2)
        monkeys[m] = (double)val;
}

double get_monkey_val(MonkeyMap &monkeys, std::string name)
{
    std::variant<Combination, double> m_val = monkeys[name];

    if (m_val.index() == 1)
    {
        double val = std::get<double>(monkeys[name]);
        return val;
    }
    else if (m_val.index() == 0)
    {
        Combination m_comb = std::get<Combination>(monkeys[name]);

        double m1_val = get_monkey_val(monkeys, m_comb.m1),
               m2_val = get_monkey_val(monkeys, m_comb.m2);

        if (m_comb.op == '+')
            return m1_val + m2_val;
        else if (m_comb.op == '-')
            return m1_val - m2_val;
        else if (m_comb.op == '*')
            return m1_val * m2_val;
        else if (m_comb.op == '/')
            return m1_val / m2_val;
    }

    return 0;
}

double get_root_val(std::vector<std::string> lines)
{
    MonkeyMap monkeys;

    for (std::string line : lines)
        setup_monkey(line, monkeys);

    double root_val = get_monkey_val(monkeys, "root");
    return root_val;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    double val = get_root_val(lines);
    long long l_val = (long long)val;
    std::cout << "Root value: " << l_val << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}