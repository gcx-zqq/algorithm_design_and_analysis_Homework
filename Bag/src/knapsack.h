
#ifndef KNAPSACK_H
#define KNAPSACK_H

#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;
#include &lt;string.h&gt;
#include &lt;time.h&gt;
#include &lt;math.h&gt;

#define MAX_ITEMS 1000000

typedef struct {
    int id;
    int weight;
    double value;
} Item;

typedef struct {
    int* selected;
    int num_selected;
    double total_value;
    int total_weight;
    double time_ms;
    size_t space_used;
} Result;

Result brute_force(Item* items, int n, int capacity);
Result dynamic_programming(Item* items, int n, int capacity);
Result greedy(Item* items, int n, int capacity);
Result backtracking(Item* items, int n, int capacity);

void print_result(Result* res, Item* items);
void free_result(Result* res);

#endif
