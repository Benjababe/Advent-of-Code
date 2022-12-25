#include "helper.hpp"

#define MAX_VAL 4000000
#define MULT_VAL 4000000

typedef long long long long;

struct Sensor
{
    long long x, y, distance;
};

long long get_tuning_frequency(std::vector<std::string> lines)
{
    std::vector<Sensor> sensors;

    for (std::string line : lines)
    {
        int x0, y0, x1, y1;
        if (sscanf(
                line.c_str(),
                "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d",
                &x0, &y0, &x1, &y1) == 4)
        {
            int dx = abs(x0 - x1),
                dy = abs(y0 - y1),
                sensor_distance = dx + dy;

            sensors.push_back(Sensor{x0, y0, sensor_distance});
        }
    }

    for (long long cur_y = 0; cur_y <= MAX_VAL; cur_y++)
    {
        std::vector<std::pair<long long, long long>> x_intervals;

        for (Sensor sensor : sensors)
        {
            // for each sensor, get the range of x coordinates where there can't be a beacon
            // retrieve x offset range by deduction the y travel needed to reach the current y coordinate
            long long diff_y = abs(sensor.y - cur_y),
                  dist_x_left = sensor.distance - diff_y;

            if (dist_x_left < 0)
                continue;

            // limit intervals to [0, 4000000]
            std::pair<long long, long long> interval = std::make_pair(
                __max(sensor.x - dist_x_left, 0),
                __min(sensor.x + dist_x_left, MAX_VAL));
            x_intervals.push_back(interval);
        }

        // sort the intervals so we can check them in order
        std::sort(x_intervals.begin(), x_intervals.end());
        std::pair<long long, long long> cur_interval = x_intervals[0];
        x_intervals.erase(x_intervals.begin());

        // after processing the intervals, all but 1 will end up with [0, 4000000]
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
            // eg. [40, 50] is out of bounds of [52, 65]
            // this indicates that (51, cur_y) is the only possible coordinate
            else
            {
                long long distress_x = cur_interval.second + 1;
                long long frequency = cur_y + (MULT_VAL * distress_x);
                return frequency;
            }
        }
    }

    return -1;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    long long frequency = get_tuning_frequency(lines);
    std::cout << "Tuning frequency: " << frequency << std::endl;
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}