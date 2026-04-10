
#include "knapsack.h"

Result brute_force(Item* items, int n, int capacity) {
    Result res;
    res.selected = (int*)malloc(n * sizeof(int));
    res.num_selected = 0;
    res.total_value = 0;
    res.total_weight = 0;
    res.space_used = sizeof(int) * n;

    clock_t start = clock();

    if (n &gt; 20) {
        res.time_ms = 0;
        res.total_value = -1;
        clock_t end = clock();
        res.time_ms = ((double)(end - start)) * 1000.0 / CLOCKS_PER_SEC;
        return res;
    }

    long long max_mask = 1LL &lt;&lt; n;
    double best_value = 0;
    int best_weight = 0;
    long long best_mask = 0;

    for (long long mask = 0; mask &lt; max_mask; mask++) {
        double current_value = 0;
        int current_weight = 0;

        for (int i = 0; i &lt; n; i++) {
            if (mask &amp; (1LL &lt;&lt; i)) {
                current_weight += items[i].weight;
                current_value += items[i].value;
            }
        }

        if (current_weight &lt;= capacity &amp;&amp; current_value &gt; best_value) {
            best_value = current_value;
            best_weight = current_weight;
            best_mask = mask;
        }
    }

    res.total_value = best_value;
    res.total_weight = best_weight;
    res.num_selected = 0;
    for (int i = 0; i &lt; n; i++) {
        if (best_mask &amp; (1LL &lt;&lt; i)) {
            res.selected[res.num_selected++] = items[i].id;
        }
    }

    clock_t end = clock();
    res.time_ms = ((double)(end - start)) * 1000.0 / CLOCKS_PER_SEC;

    return res;
}
