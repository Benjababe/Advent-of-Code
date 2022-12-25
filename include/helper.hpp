#include <algorithm>
#include <chrono>
#include <fstream>
#include <math.h>
#include <iostream>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

typedef std::chrono::time_point<std::chrono::high_resolution_clock> TimeUnit;

namespace Helper
{
    std::vector<std::string> get_lines(std::string);
    std::vector<std::string> split_string(std::string, char);

    std::string ltrim(const std::string &);
    std::string rtrim(const std::string &);
    std::string trim(const std::string &);
    std::string replace_all(std::string &, const std::string &, const std::string &);
    std::string join(const std::vector<std::string>, const std::string &);

    TimeUnit get_current_time();
    void get_time_taken(TimeUnit, TimeUnit);

    template <class T>
    std::vector<T> intersect_vectors(std::vector<T> v1, std::vector<T> v2)
    {
        std::vector<T> v3;

        std::sort(v1.begin(), v1.end());
        std::sort(v2.begin(), v2.end());

        std::set_intersection(
            v1.begin(), v1.end(),
            v2.begin(), v2.end(),
            back_inserter(v3));
        return v3;
    }

    template <class T>
    std::vector<T> plus_vectors(std::vector<T> v1, std::vector<T> v2)
    {
        std::vector<T> tmp_v = v1;
        for (size_t i = 0; i < v1.size(); i++)
        {
            tmp_v[i] += v2[i];
        }
        return tmp_v;
    }

    template <class T>
    std::vector<T> minus_vectors(std::vector<T> v1, std::vector<T> v2)
    {
        std::vector<T> tmp_v = v1;
        for (size_t i = 0; i < v1.size(); i++)
        {
            tmp_v[i] -= v2[i];
        }
        return tmp_v;
    }
};