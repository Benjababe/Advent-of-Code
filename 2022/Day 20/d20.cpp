#include "helper.hpp"

typedef long long long long;

struct Node
{
    size_t id;
    long long val;
    Node *prev, *next;

    static void swap(Node *n1, Node *n2)
    {
        long long tmp_val = n1->val;
        size_t tmp_id = n1->id;

        n1->val = n2->val;
        n1->id = n2->id;

        n2->val = tmp_val;
        n2->id = tmp_id;
    }
};

class CircularDoublyLinkedList
{
public:
    Node *head, *tail;
    long long size;

    CircularDoublyLinkedList()
    {
        this->head = NULL;
        this->tail = NULL;
        this->size = 0;
    }

    void push(size_t id, long long val)
    {
        Node *new_node = new Node;
        new_node->id = id;
        new_node->val = val;
        new_node->next = this->head;

        // if linked list is populated,
        // make previous of current head the new node
        if (this->head != NULL)
            this->head->prev = new_node;
        // if it's not populated,
        // new node will be the tail of the linked list
        else
            this->tail = new_node;

        // make the new node the head
        this->head = new_node;

        // link the head and tail together
        this->head->prev = this->tail;
        this->tail->next = this->head;

        this->size++;
    }

    void print()
    {
        Node *node = this->head;
        while (true)
        {
            std::cout << node->val << ", ";
            if (node == this->tail)
                break;
            node = node->next;
        }
        std::cout << std::endl;
    }
};

long long get_coordinate_sum(std::vector<std::string> lines, bool pt2_flag)
{
    CircularDoublyLinkedList cd_linked_list;
    std::reverse(lines.begin(), lines.end());
    std::vector<size_t> ids;
    size_t id = 0,
           r_count = (pt2_flag) ? 10 : 1;

    for (std::string line : lines)
    {
        line = Helper::trim(line);
        long long node_val = (long long)atoi(line.c_str()) * ((pt2_flag) ? 811589153 : 1);

        cd_linked_list.push(id, node_val);
        ids.insert(ids.begin(), id++);
    }

    for (size_t r = 0; r < r_count; r++)
    {
        for (size_t id : ids)
        {
            Node *node = cd_linked_list.head;
            while (node->id != id)
                node = node->next;

            int steps = abs(node->val) % (cd_linked_list.size - 1);

            for (int i = 0; i < steps; i++)
            {
                if (node->val < 0)
                {
                    Node::swap(node, node->prev);
                    node = node->prev;
                }
                if (node->val > 0)
                {
                    Node::swap(node, node->next);
                    node = node->next;
                }
            }
        }
    }

    long long sum = 0;
    Node *node = cd_linked_list.head;
    while (node->val != 0)
        node = node->next;

    for (size_t i = 0; i < 3; i++)
    {
        for (size_t j = 0; j < 1000; j++)
            node = node->next;
        sum += node->val;
    }

    return sum;
}

int main()
{
    std::vector<std::string> lines = Helper::get_lines("input.txt");

    auto t1 = Helper::get_current_time();

    long long s1 = get_coordinate_sum(lines, false);
    std::cout << "Pt1 coordinate sum: " << s1 << std::endl;

    long long s2 = get_coordinate_sum(lines, true);
    std::cout << "Pt2 coordinate sum: " << s2 << std::endl;

    auto t2 = Helper::get_current_time();
    Helper::get_time_taken(t1, t2);

    return 0;
}