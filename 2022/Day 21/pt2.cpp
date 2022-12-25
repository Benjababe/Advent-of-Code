#include "helper.hpp"
#include <map>
#include <variant>

typedef long long llong;

#define MonkeyMap std::map<std::string, std::variant<Combination, double>>

bool neg = false;

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

double get_monkey_val(MonkeyMap &monkeys, std::string name, llong h_val)
{
    if (name == "humn")
        return (double)h_val;

    std::variant<Combination, double> m_val = monkeys[name];

    if (m_val.index() == 1)
    {
        double val = std::get<double>(monkeys[name]);
        return val;
    }
    else if (m_val.index() == 0)
    {
        Combination m_comb = std::get<Combination>(monkeys[name]);

        double m1_val = get_monkey_val(monkeys, m_comb.m1, h_val),
               m2_val = get_monkey_val(monkeys, m_comb.m2, h_val);

        if (name == "root")
            return m1_val - m2_val;

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

llong get_approx_h_val(MonkeyMap &monkeys, size_t samples)
{
    // initial difference of m1 & m2 of root where humn=0
    double base_diff = get_monkey_val(monkeys, "root", 0),
           prev_diff = base_diff;
    double diff_diff_sum;

    // increment humn to see how the difference of m1 & m2 changes
    for (size_t i = 1; i <= samples; i++)
    {
        double diff = get_monkey_val(monkeys, "root", i);
        diff_diff_sum += (prev_diff - diff);
        prev_diff = diff;
    }

    // get the average change in difference for each increment of humn
    double avg_diff = diff_diff_sum / samples;

    // if incrementing increases the difference, we should decrement then (or increment when diff < 0)
    if (avg_diff < 0)
        neg = true;

    // our approx humn will be initial difference divided by average diff for each increment
    llong h_val = base_diff / avg_diff;
    return h_val;
}

llong get_human_val(std::vector<std::string> lines)
{
    MonkeyMap monkeys;

    for (std::string line : lines)
        setup_monkey(line, monkeys);

    llong h_val = get_approx_h_val(monkeys, 10);
    while (true)
    {
        double root_difference = get_monkey_val(monkeys, "root", h_val);

        if (root_difference == 0)
            break;

        if (root_difference > 0 && !neg)
            h_val++;
        else
            h_val--;
    }
    return h_val;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    double val = get_human_val(lines);
    llong l_val = (llong)val;
    std::cout << "Human value: " << l_val << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}