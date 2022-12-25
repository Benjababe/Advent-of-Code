#include "helper.hpp"

#define WHITESPACE " \n\r\t\f\v"

std::vector<std::string> Helper::get_lines(std::string filename)
{
    std::vector<std::string> lines;

    std::ifstream file;
    file.open(filename.c_str(), std::ios::in);

    if (file.is_open())
    {
        std::string line;
        while (getline(file, line))
        {
            lines.push_back(line);
        }

        file.close();
    }

    return lines;
}

std::vector<std::string> Helper::split_string(std::string s, char sep)
{
    std::stringstream ss(s);
    std::string tmp;
    std::vector<std::string> out;

    while (std::getline(ss, tmp, sep))
    {
        out.push_back(tmp);
    }

    return out;
}

std::string Helper::ltrim(const std::string &s)
{
    size_t start = s.find_first_not_of(WHITESPACE);
    return (start == std::string::npos) ? "" : s.substr(start);
}

std::string Helper::rtrim(const std::string &s)
{
    size_t end = s.find_last_not_of(WHITESPACE);
    return (end == std::string::npos) ? "" : s.substr(0, end + 1);
}

std::string Helper::trim(const std::string &s)
{
    return Helper::rtrim(Helper::ltrim(s));
}

std::string Helper::replace_all(std::string &s, const std::string &from, const std::string &to)
{
    size_t start_pos = 0;
    while ((start_pos = s.find(from, start_pos)) != std::string::npos)
    {
        s.replace(start_pos, from.length(), to);
        start_pos += to.length();
    }
    return s;
}

std::string Helper::join(const std::vector<std::string> v, const std::string &delim)
{
    std::string out;
    if (std::vector<std::string>::const_iterator i = v.begin(), e = v.end(); i != e)
    {
        out += *i++;
        for (; i != e; ++i)
            out.append(delim).append(*i);
    }
    return out;
}

TimeUnit Helper::get_current_time()
{
    return std::chrono::high_resolution_clock::now();
}

void Helper::get_time_taken(TimeUnit start, TimeUnit stop)
{
    std::vector<std::string> units = {"", "milli", "micro", "nano"};
    size_t u_index = 0;

    std::chrono::duration<double> diff = stop - start;
    double time_taken = diff.count();

    while (time_taken < 1.0)
    {
        time_taken *= 1000;
        u_index++;
    }

    std::cout << "Program running time: " << time_taken << " " << units[u_index] << "seconds" << std::endl;
}