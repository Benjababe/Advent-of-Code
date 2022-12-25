#include "helper.hpp"
#include <map>
#include <regex>

class Directory
{
public:
    std::string name;
    int size;
    std::map<std::string, Directory> children;

    Directory() {}
    Directory(std::string name)
    {
        this->name = name;
        this->size = 0;
    }

    void add_size(int filesize)
    {
        this->size += filesize;
    }

    void add_child(std::string folder)
    {
        this->children[folder] = Directory(folder);
    }

    Directory *get_child_ptr(std::string folder)
    {
        return &this->children[folder];
    }
};

/**
 * @brief Inserts file into current path
 *
 * @param root_dir Root Directory object
 * @param current_path Vector of current path
 * @param filesize
 * @param filename
 */
void handle_file_input(
    Directory &root_dir, std::vector<std::string> &current_path,
    int filesize, std::string filename)
{
    Directory *current_dir = &root_dir;
    for (std::string folder : current_path)
        current_dir = current_dir->get_child_ptr(folder);

    current_dir->add_size(filesize);
}

/**
 * @brief Inserts directory into current path
 *
 * @param root_dir Root Directory object
 * @param current_path Vector of current path
 * @param dir_name Name of the directory in the current path
 */
void handle_dir_input(
    Directory &root_dir, std::vector<std::string> &current_path,
    std::string dir_name)
{
    Directory *current_dir = &root_dir;
    for (std::string folder : current_path)
        current_dir = current_dir->get_child_ptr(folder);

    current_dir->add_child(dir_name);
}

/**
 * @brief handles ls commands, reads following lines for directories or files
 *
 * @param lines Lines of input file
 * @param i Current line index
 * @param root_dir Root Directory object
 * @param current_path Vector of current path
 * @return int Number of lines to skip
 */
int handle_list_dir(
    std::vector<std::string> &lines, int i,
    Directory &root_dir, std::vector<std::string> &current_path)
{
    std::regex file_rgx("(\\d+) (.*)");
    std::regex dir_rgx("dir (.*)");
    std::smatch matches;

    int inc = 1;
    if ((i + inc) >= lines.size())
        return 0;

    std::string new_line = lines[i + inc];
    while (new_line.at(0) != '$')
    {
        if (std::regex_search(new_line, matches, file_rgx))
        {
            std::string filesize = matches[1];
            handle_file_input(root_dir, current_path, atoi(filesize.c_str()), matches[2]);
        }

        else if (std::regex_search(new_line, matches, dir_rgx))
            handle_dir_input(root_dir, current_path, matches[1]);

        inc++;
        if ((i + inc) >= lines.size())
            return inc - 1;
        new_line = lines[i + inc];
    }

    return inc;
}

/**
 * @brief Handles ls commands, goes down or up from the current path
 *
 * @param current_path Vector of current path
 * @param new_dir New directory to enter from relative path, ".." to go up 1 level
 */
void handle_directory_change(std::vector<std::string> &current_path, std::string new_dir)
{
    if (new_dir == "..")
        current_path.pop_back();
    else
    {
        current_path.push_back(new_dir);
    }
}

/**
 * @brief Creates the directory structure based on input
 *
 * @param lines Input lines
 * @param root_dir Root Directory object
 */
void populate_directory(std::vector<std::string> lines, Directory &root_dir)
{
    std::vector<std::string> current_path = {};

    for (int i = 0; i < lines.size(); i++)
    {
        std::string line = lines[i];

        std::regex ls_rgx("\\$ ls");
        std::regex cd_rgx("\\$ cd (.*)");
        std::smatch matches;

        if (std::regex_match(line, ls_rgx))
        {
            int inc = handle_list_dir(lines, i, root_dir, current_path);
            i += inc - 1;
        }

        else if (std::regex_search(line, matches, cd_rgx))
        {
            handle_directory_change(current_path, matches[1]);
        }
    }
}

/**
 * @brief Finds the sizes for each directory in the structure
 *
 * @param dir Current working directory
 * @param dir_sizes Map to store all directory sizes
 * @param current_path Current path of the working directory
 * @return int Size of the current working directory
 */
int calculate_dir_size(
    Directory &dir, std::map<std::string, int> &dir_sizes,
    std::string current_path)
{
    int dir_size = dir.size;
    std::map<std::string, Directory> children = dir.children;

    for (std::pair<std::string, Directory> it : children)
    {
        Directory child_dir = it.second;
        int child_size = calculate_dir_size(child_dir, dir_sizes, current_path + child_dir.name + "/");
        dir_size += child_size;
    }

    dir_sizes[current_path] = dir_size;
    return dir_size;
}

/**
 * @brief Get the smallest possible directory to delete
 *
 * @param dir_sizes Map to store all directory sizes
 * @return int
 */
int get_smallest_dir_size(std::map<std::string, int> &dir_sizes)
{
    int available_space = 70000000 - dir_sizes["/"],
        space_needed = 30000000 - available_space,
        min_dir_size = 30000000;

    for (std::pair<std::string, int> it : dir_sizes)
    {
        int dir_size = it.second;
        if (dir_size > space_needed && dir_size < min_dir_size)
            min_dir_size = dir_size;
    }

    return min_dir_size;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();

    Directory root_dir = Directory("/");
    populate_directory(lines, root_dir);

    std::map<std::string, int> dir_sizes;
    calculate_dir_size(root_dir, dir_sizes, "/");

    int size = get_smallest_dir_size(dir_sizes);
    std::cout << "Directories size sum: " << size << std::endl;

    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}