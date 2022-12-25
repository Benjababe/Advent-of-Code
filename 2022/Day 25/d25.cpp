#include "helper.hpp"

typedef long long llong;

llong snafu_to_decimal(std::string snafu)
{
    llong sum = 0, multiplier = 1;
    std::reverse(snafu.begin(), snafu.end());

    for (char c : snafu)
    {
        if (c == '0' || c == '1' || c == '2')
            sum += multiplier * (c - '0');
        else if (c == '-')
            sum -= multiplier;
        else if (c == '=')
            sum -= (2 * multiplier);

        multiplier *= 5;
    }

    return sum;
}

std::string decimal_to_snafu(llong num)
{
    std::string snafu_chars = "012=-";
    if (num != 0)
    {
        llong rem = num % 5,
              t_num;

        if (rem == 0 || rem == 1 || rem == 2)
            t_num = (num - rem) / 5;
        else if (rem == 3)
            t_num = (num + 2) / 5;
        else if (rem == 4)
            t_num = (num + 1) / 5;

        return decimal_to_snafu(t_num) + snafu_chars.at(rem);
    }

    return "";
}

std::string get_snafu_num(std::vector<std::string> lines)
{
    llong decimal_num = 0;
    std::string snafu_num;

    for (std::string line : lines)
        decimal_num += snafu_to_decimal(line);

    snafu_num = decimal_to_snafu(decimal_num);
    return snafu_num;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    std::string snafu_num = get_snafu_num(lines);
    std::cout << "SNAFU num: " << snafu_num << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}