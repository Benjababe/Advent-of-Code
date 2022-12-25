#include "helper.hpp"

struct State
{
    std::vector<int> resources, bots;
    static bool cmp_sort_state(const State &s1, const State &s2)
    {
        std::vector<int> s1_res = s1.resources,
                         s1_bots = s1.bots,
                         s2_res = s2.resources,
                         s2_bots = s2.bots;

        if ((s1_res[0] + s1_bots[0]) > (s2_res[0] + s2_bots[0]))
            return true;
        else if ((s1_res[0] + s1_bots[0]) < (s2_res[0] + s2_bots[0]))
            return false;

        if ((s1_res[1] + s1_bots[1]) > (s2_res[1] + s2_bots[1]))
            return true;
        else if ((s1_res[1] + s1_bots[1]) < (s2_res[1] + s2_bots[1]))
            return false;

        if ((s1_res[2] + s1_bots[2]) > (s2_res[2] + s2_bots[2]))
            return true;
        else if ((s1_res[2] + s1_bots[2]) < (s2_res[2] + s2_bots[2]))
            return false;

        if ((s1_res[3] + s1_bots[3]) > (s2_res[3] + s2_bots[3]))
            return true;

        return false;
    }
};

struct Bot
{
    std::vector<int> cost, create;
};

struct Blueprint
{
    int id;
    std::vector<Bot> bots;
};

std::vector<Blueprint> get_blueprints(std::vector<std::string> lines)
{
    std::vector<Blueprint> blueprints;

    for (std::string line : lines)
    {
        int id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs;
        const char *sample = "Blueprint %d: Each ore robot costs %d ore. Each clay robot costs %d ore. Each obsidian robot costs %d ore and %d clay. Each geode robot costs %d ore and %d obsidian.";
        int count = sscanf(line.c_str(), sample, &id, &ore_ore, &clay_ore, &obs_ore, &obs_clay, &geo_ore, &geo_obs);

        if (count == 7)
        {
            blueprints.push_back({id, {
                                          {{0, 0, 0, ore_ore}, {0, 0, 0, 1}},
                                          {{0, 0, 0, clay_ore}, {0, 0, 1, 0}},
                                          {{0, 0, obs_clay, obs_ore}, {0, 1, 0, 0}},
                                          {{0, geo_obs, 0, geo_ore}, {1, 0, 0, 0}},
                                      }});
        }
    }

    return blueprints;
}

bool cmp_resource_cost(std::vector<int> resources, std::vector<int> cost)
{
    for (size_t i = 0; i < resources.size(); i++)
    {
        if (resources[i] < cost[i])
            return false;
    }
    return true;
}

int find_max_geode(std::vector<State> states)
{
    int max = 0;

    for (State state : states)
    {
        if (state.resources[0] > max)
            max = state.resources[0];
    }

    return max;
}

int run_simulation(Blueprint blueprint, int time)
{
    State init_state = {std::vector<int>({0, 0, 0, 0}), std::vector<int>({0, 0, 0, 1})};
    std::vector<State> queue = {init_state};

    for (size_t i = 0; i < time; i++)
    {
        std::vector<State> tmp_queue;
        for (State state : queue)
        {
            std::vector<int> cur_resources = state.resources,
                             cur_bots = state.bots,
                             post_collect = Helper::plus_vectors(cur_resources, cur_bots);
            for (Bot bot : blueprint.bots)
            {
                if (cmp_resource_cost(cur_resources, bot.cost))
                {
                    std::vector<int> final_resources = Helper::minus_vectors(post_collect, bot.cost);
                    std::vector<int> final_bots = Helper::plus_vectors(cur_bots, bot.create);
                    State new_state{final_resources, final_bots};
                    tmp_queue.push_back(new_state);
                }
            }
            State new_state{post_collect, cur_bots};
            tmp_queue.push_back(new_state);
        }
        queue = tmp_queue;
        std::sort(queue.begin(), queue.end(), State::cmp_sort_state);
        if (queue.size() > 1500)
            queue.resize(1500);
    }

    return find_max_geode(queue);
}

void iterate_blueprints(std::vector<Blueprint> blueprints)
{
    int p1 = 0,
        p2 = 1;
    for (Blueprint blueprint : blueprints)
    {
        std::cout << "Starting blueprint #" << blueprint.id << std::endl;
        int max_geo = run_simulation(blueprint, 24);
        p1 += (max_geo * blueprint.id);

        max_geo = run_simulation(blueprint, 32);
        p2 *= (blueprint.id < 4) ? max_geo : 1;
    }

    std::cout << "Quality level: " << p1 << std::endl;
    std::cout << "Geode multiple: " << p2 << std::endl;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();
    std::vector<Blueprint> blueprints = get_blueprints(lines);
    iterate_blueprints(blueprints);
    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}