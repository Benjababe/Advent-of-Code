#include "helper.hpp"

#define TARGET_Y 2000000

typedef long long long long;

int get_non_beacon_count(std::vector<std::string> lines)
{
    std::vector<std::pair<long long, long long>> x_intervals;

    for (std::string line : lines)
    {
        int x0, y0, x1, y1;
        if (sscanf(
                line.c_str(),
                "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d",
                &x0, &y0, &x1, &y1) == 4)
        {
            // sensor range = manhattan distance to the beacon detected
            int dx = abs(x0 - x1),
                dy = abs(y0 - y1),
                sensor_distance = dx + dy;

            // for each sensor, get the range of x coordinates where there can't be a beacon
            // retrieve x offset range by deduction the y travel needed to reach 2000000
            long long diff_y = abs(y0 - TARGET_Y),
                  dist_x_left = sensor_distance - diff_y;

            if (dist_x_left < 0)
                continue;

            // process the intervals later after sorting
            std::pair<long long, long long> interval = std::make_pair(
                x0 - dist_x_left,
                x0 + dist_x_left);
            x_intervals.push_back(interval);
        }
    }

    // sort the intervals so we can check them in order
    std::sort(x_intervals.begin(), x_intervals.end());
    std::pair<long long, long long> cur_interval = x_intervals[0];
    x_intervals.erase(x_intervals.begin());

    long long non_beacon_count = 0;

    for (std::pair<long long, long long> x_interval : x_intervals)
    {
        // if interval is completely inside the current interval, skip
        // eg. [20, 25] is completely inside [15, 30]
        if (cur_interval.first <= x_interval.first &&
            x_interval.second <= cur_interval.second)
            continue;

        // if interval extends the current interval, extend current interval
        // eg. [20, 25] extends [15, 22] -> [15, 25]
        else if (cur_interval.first <= x_interval.first &&
                 cur_interval.second <= x_interval.second &&
                 x_interval.first <= cur_interval.second)
            cur_interval.second = x_interval.second;

        // if interval is out of bounds of the current interval, use the interval next
        // eg. [40, 50] is out of bounds of [20, 35]
        else
        {
            // and add the old interval to the count
            non_beacon_count += (cur_interval.second - cur_interval.first) + 1;
            cur_interval = x_interval;
        }
    }

    // add remaining interval to the count
    non_beacon_count += (cur_interval.second - cur_interval.first);
    return non_beacon_count;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    int count = get_non_beacon_count(lines);
    std::cout << "Non beacon count: " << count << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}