
#include "knapsack.h"

int compare_items(const void* a, const void* b) {
    Item* itemA = (Item*)a;
    Item* itemB = (Item*)b;
    double ratioA = itemA-&gt;value / itemA-&gt;weight;
    double ratioB = itemB-&gt;value / itemB-&gt;weight;
    if (ratioB &gt; ratioA) return 1;
    if (ratioB &lt; ratioA) return -1;
    return 0;
}

Result greedy(Item* items, int n, int capacity) {
    Result res;
    res.selected = (int*)malloc(n * sizeof(int));
    res.num_selected = 0;
    res.total_value = 0;
    res.total_weight = 0;
    res.space_used = sizeof(int) * n;

    clock_t start = clock();

    Item* sorted_items = (Item*)malloc(n * sizeof(Item));
    memcpy(sorted_items, items, n * sizeof(Item));
    res.space_used += n * sizeof(Item);

    qsort(sorted_items, n, sizeof(Item), compare_items);

    int remaining = capacity;
    for (int i = 0; i &lt; n; i++) {
        if (sorted_items[i].weight &lt;= remaining) {
            res.selected[res.num_selected++] = sorted_items[i].id;
            res.total_value += sorted_items[i].value;
            res.total_weight += sorted_items[i].weight;
            remaining -= sorted_items[i].weight;
        }
    }

    free(sorted_items);

    clock_t end = clock();
    res.time_ms = ((double)(end - start)) * 1000.0 / CLOCKS_PER_SEC;

    return res;
}
